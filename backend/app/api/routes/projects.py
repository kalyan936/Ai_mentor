"""
AI Mentor - Project API Routes.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.project import (
    ProjectSuggestionRequest, ProjectSubmitRequest, ProjectReviewResponse
)
from ...agents.project_mentor_agent import suggest_project, review_project
from ...models.project import ProjectSubmission

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/suggest")
async def suggest_project_endpoint(request: ProjectSuggestionRequest):
    """Get a project suggestion from the Project Mentor."""
    project = await suggest_project(
        topic=request.topic,
        level=request.difficulty or "intermediate",
    )
    return project


@router.post("/submit")
async def submit_project(request: ProjectSubmitRequest, db: Session = Depends(get_db)):
    """Submit a project for AI review."""
    # Store submission
    submission = ProjectSubmission(
        user_id=request.user_id,
        project_title=request.project_title,
        topic=request.topic,
        description=request.description,
        submitted_code=request.submitted_code,
        repo_link=request.repo_link,
        status="submitted",
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Get AI review
    review = await review_project(
        title=request.project_title,
        topic=request.topic,
        description=request.description,
        code=request.submitted_code,
    )

    # Update submission with feedback
    submission.feedback = review.get("feedback", "")
    submission.score = review.get("score", 0)
    submission.skills_demonstrated = json.dumps(review.get("skills_demonstrated", []))
    submission.status = "reviewed"
    db.commit()

    return {
        "submission_id": submission.id,
        **review
    }


@router.get("/{user_id}")
def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    """Get all projects for a user."""
    projects = db.query(ProjectSubmission).filter(
        ProjectSubmission.user_id == user_id
    ).order_by(ProjectSubmission.created_at.desc()).all()

    return [{
        "id": p.id,
        "title": p.project_title,
        "topic": p.topic,
        "status": p.status,
        "score": p.score,
        "created_at": str(p.created_at),
    } for p in projects]

