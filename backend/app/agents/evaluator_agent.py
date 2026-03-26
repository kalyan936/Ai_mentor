"""
AI Mentor - Evaluator Agent.

Handles quiz generation, scoring, and code evaluation.
Identifies weak areas and provides actionable feedback.
"""

import json
from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import invoke_agent
from .prompts.evaluator import (
    EVALUATOR_QUIZ_GENERATE_PROMPT,
    EVALUATOR_SCORE_PROMPT,
    EVALUATOR_CODE_PROMPT,
)


async def generate_quiz(
    topic: str,
    subtopic: Optional[str] = None,
    difficulty: str = "medium",
    num_questions: int = 5,
    question_types: List[str] = None,
    level: str = "beginner"
) -> List[Dict[str, Any]]:
    """
    Generate a quiz with diverse question types.

    Returns:
        List of question objects
    """
    if question_types is None:
        question_types = ["mcq", "true_false", "short_answer"]

    user_message = EVALUATOR_QUIZ_GENERATE_PROMPT.format(
        topic=topic,
        subtopic=subtopic or topic,
        difficulty=difficulty,
        num_questions=num_questions,
        question_types=", ".join(question_types),
        level=level,
    )

    logger.info(f"Generating {num_questions} questions for {topic}/{subtopic}")
    result = await invoke_agent("You are an expert quiz generator.", user_message, parse_json=True)

    # Handle both direct array and wrapped responses
    if isinstance(result, list):
        return result
    elif isinstance(result, dict) and "questions" in result:
        return result["questions"]
    elif isinstance(result, dict) and not result.get("error"):
        return [result]

    # Fallback quiz
    logger.warning("Quiz generation failed, using fallback")
    return _generate_fallback_quiz(topic, subtopic, num_questions)


async def score_quiz(
    questions: List[Dict[str, Any]],
    answers: List[str],
) -> Dict[str, Any]:
    """
    Score a quiz submission and provide feedback.

    Returns:
        Score results with feedback and weak areas
    """
    # Build Q&A pairs for evaluation
    qa_pairs = []
    for i, (q, a) in enumerate(zip(questions, answers)):
        qa_pairs.append({
            "question_id": q.get("question_id", i + 1),
            "question": q.get("question", ""),
            "question_type": q.get("question_type", "mcq"),
            "correct_answer": q.get("correct_answer", ""),
            "user_answer": a,
            "points": q.get("points", 10),
        })

    user_message = EVALUATOR_SCORE_PROMPT.format(qa_pairs=json.dumps(qa_pairs, indent=2))
    result = await invoke_agent("You are an expert quiz scorer.", user_message, parse_json=True)

    # Calculate score if AI doesn't
    if "total_score" not in result or result.get("error"):
        result = _score_manually(qa_pairs)

    return result


async def evaluate_code(
    prompt: str,
    code: str,
    output: Optional[str] = None,
    status: str = "unknown",
    errors: Optional[str] = None,
    language: str = "python"
) -> Dict[str, Any]:
    """
    Evaluate a code submission.

    Returns:
        Evaluation results with score and feedback
    """
    user_message = EVALUATOR_CODE_PROMPT.format(
        prompt=prompt,
        code=code,
        language=language,
        output=output or "Not executed",
        status=status,
        errors=errors or "None",
    )

    result = await invoke_agent("You are an expert code reviewer.", user_message, parse_json=True)
    return result


def _score_manually(qa_pairs: list) -> Dict[str, Any]:
    """Fallback manual scoring for MCQ and true/false."""
    results = []
    correct = 0
    total_points = 0
    max_points = 0

    for qa in qa_pairs:
        points = qa.get("points", 10)
        max_points += points
        user_ans = str(qa["user_answer"]).strip().lower()
        correct_ans = str(qa["correct_answer"]).strip().lower()

        is_correct = user_ans == correct_ans
        if is_correct:
            correct += 1
            total_points += points

        results.append({
            "question_id": qa["question_id"],
            "correct": is_correct,
            "score": points if is_correct else 0,
            "feedback": "Correct!" if is_correct else f"Incorrect. The correct answer is: {qa['correct_answer']}"
        })

    score_pct = (total_points / max_points * 100) if max_points > 0 else 0

    return {
        "results": results,
        "total_score": round(score_pct, 1),
        "correct_count": correct,
        "feedback": f"You answered {correct}/{len(qa_pairs)} correctly ({score_pct:.0f}%)",
        "weak_areas": [],
        "recommendations": ["Review the questions you got wrong."]
    }


def _generate_fallback_quiz(topic: str, subtopic: str, num: int) -> list:
    """Generate basic fallback quiz questions."""
    return [{
        "question_id": i + 1,
        "question": f"Sample question {i + 1} about {subtopic or topic}",
        "question_type": "mcq",
        "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
        "correct_answer": "A",
        "explanation": "This is a fallback question.",
        "difficulty": "medium",
        "points": 10
    } for i in range(min(num, 3))]
