"""
AI Mentor - Code Challenge & Debug API Routes.

Handles coding challenge generation, code submission, execution, evaluation, and debugging.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.code_submission import (
    CodingChallengeRequest, CodeSubmitRequest, CodeResultResponse,
    DebugRequest, DebugResponse
)
from ...agents.evaluator_agent import evaluate_code
from ...agents.debugger_agent import debug_code
from ...agents.base_agent import invoke_agent
from ...evaluation.code_executor import execute_python_code
from ...models.code_submission import CodeSubmission
from ...services.progress_service import update_progress

router = APIRouter(prefix="/code", tags=["Code Challenges"])


CODING_CHALLENGE_PROMPT = """Generate a coding challenge for:
Topic: {topic}
Subtopic: {subtopic}
Difficulty: {difficulty}

Return JSON:
{{
    "challenge_id": "unique_id",
    "title": "Challenge Title",
    "description": "Detailed problem description",
    "requirements": ["req1", "req2"],
    "starter_code": "# Starter code here\\n",
    "test_cases": [{{"input": "test input", "expected": "expected output"}}],
    "hints": ["hint1"],
    "difficulty": "{difficulty}",
    "estimated_minutes": 15,
    "topic": "{topic}",
    "subtopic": "{subtopic}"
}}

Return ONLY valid JSON."""


@router.post("/challenge")
async def generate_challenge(request: CodingChallengeRequest):
    """Generate a coding challenge using AI."""
    prompt = CODING_CHALLENGE_PROMPT.format(
        topic=request.topic,
        subtopic=request.subtopic or request.topic,
        difficulty=request.difficulty,
    )

    result = await invoke_agent(
        "You are an expert coding challenge designer.",
        prompt,
        parse_json=True
    )

    result.setdefault("challenge_id", f"{request.topic}_{request.difficulty}_1")
    result.setdefault("title", f"{request.topic.title()} Challenge")
    result.setdefault("description", "Complete the coding challenge")

    return result


@router.post("/submit")
async def submit_code(request: CodeSubmitRequest, db: Session = Depends(get_db)):
    """Submit code for execution and evaluation."""
    # Execute the code safely
    exec_result = execute_python_code(request.submitted_code)

    # Evaluate with AI
    eval_result = await evaluate_code(
        prompt=request.prompt,
        code=request.submitted_code,
        output=exec_result.get("output"),
        status=exec_result.get("status"),
        errors=exec_result.get("errors"),
        language=request.language,
    )

    # Store in database
    submission = CodeSubmission(
        user_id=request.user_id,
        topic=request.topic,
        subtopic=request.subtopic,
        prompt=request.prompt,
        submitted_code=request.submitted_code,
        language=request.language,
        execution_output=exec_result.get("output"),
        execution_status=exec_result.get("status"),
        errors=exec_result.get("errors"),
        agent_feedback=eval_result.get("feedback", ""),
        score=eval_result.get("score", 0),
        suggestions=json.dumps(eval_result.get("suggestions", [])),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Update progress
    update_progress(
        db, request.user_id, request.topic,
        request.subtopic or request.topic,
        score=eval_result.get("score", 0)
    )

    return {
        "submission_id": submission.id,
        "execution_output": exec_result.get("output"),
        "execution_status": exec_result.get("status"),
        "errors": exec_result.get("errors"),
        "score": eval_result.get("score", 0),
        "feedback": eval_result.get("feedback", ""),
        "suggestions": eval_result.get("suggestions", []),
        "best_practices": eval_result.get("best_practices", []),
    }


@router.post("/debug", response_model=DebugResponse)
async def debug_code_endpoint(request: DebugRequest, db: Session = Depends(get_db)):
    """Get AI debugging help for code."""
    result = await debug_code(
        code=request.code,
        error_message=request.error_message,
        expected_behavior=request.expected_behavior,
        topic=request.topic,
    )

    return DebugResponse(**result)

