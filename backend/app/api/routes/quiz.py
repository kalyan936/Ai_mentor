"""
AI Mentor - Quiz API Routes.

Handles quiz generation, submission, and scoring.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.quiz import QuizGenerateRequest, QuizSubmitRequest, QuizResultResponse
from ...agents.evaluator_agent import generate_quiz, score_quiz
from ...agents.memory_agent import MemoryAgent
from ...models.quiz import QuizResult
from ...services.progress_service import update_progress

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/generate")
async def generate_quiz_endpoint(request: QuizGenerateRequest):
    """Generate a quiz using the Evaluator Agent."""
    questions = await generate_quiz(
        topic=request.topic,
        subtopic=request.subtopic,
        difficulty=request.difficulty,
        num_questions=request.num_questions,
        question_types=request.question_types,
    )
    return {"questions": questions, "topic": request.topic, "subtopic": request.subtopic}


@router.post("/submit")
async def submit_quiz(request: QuizSubmitRequest, db: Session = Depends(get_db)):
    """Submit quiz answers for scoring."""
    # Score via AI agent
    results = await score_quiz(request.questions, request.answers)

    # Store in database
    quiz_record = QuizResult(
        user_id=request.user_id,
        topic=request.topic,
        subtopic=request.subtopic,
        questions_json=json.dumps(request.questions),
        answers_json=json.dumps(request.answers),
        score=results.get("total_score", 0),
        total_questions=len(request.questions),
        correct_count=results.get("correct_count", 0),
        feedback=results.get("feedback", ""),
        weak_areas=json.dumps(results.get("weak_areas", [])),
        time_taken_seconds=request.time_taken_seconds,
    )
    db.add(quiz_record)
    db.commit()
    db.refresh(quiz_record)

    # Update progress
    score = results.get("total_score", 0)
    update_progress(db, request.user_id, request.topic, request.subtopic or request.topic, score=score)

    # Store in memory if weak areas found
    memory_agent = MemoryAgent(db)
    weak_areas = results.get("weak_areas", [])
    if weak_areas:
        for weak in weak_areas:
            memory_agent.store_weakness(
                request.user_id, request.topic,
                f"Struggled with: {weak} (quiz score: {score}%)"
            )

    if score >= 80:
        memory_agent.store_achievement(
            request.user_id, request.topic,
            f"Scored {score}% on {request.subtopic or request.topic} quiz"
        )

    return {
        "quiz_id": quiz_record.id,
        "score": results.get("total_score", 0),
        "total_questions": len(request.questions),
        "correct_count": results.get("correct_count", 0),
        "results": results.get("results", []),
        "feedback": results.get("feedback", ""),
        "weak_areas": weak_areas,
        "recommendations": results.get("recommendations", []),
    }

