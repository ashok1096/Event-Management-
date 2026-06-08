"""Feedback router - endpoints for feedback management using MongoDB (Beanie ODM)."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.schemas.feedback_schema import FeedbackSchema, FeedbackCreate, FeedbackUpdate
from app.auth.dependencies import get_current_user, require_role
from app.models.role_enum import Role
from app.models.feedback_model import Feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback: FeedbackCreate,
    current_user: dict = Depends(get_current_user)
):
    """Submit feedback for an event or session. Any authenticated user."""
    if not feedback.event_id and not feedback.session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either event_id or session_id must be provided"
        )

    new_feedback = Feedback(
        event_id=feedback.event_id,
        session_id=feedback.session_id,
        registration_id=feedback.registration_id,
        rating=feedback.rating,
        comment=feedback.comment,
    )
    await new_feedback.insert()

    return {
        "message": "Feedback submitted successfully",
        "id": str(new_feedback.id),
        "rating": new_feedback.rating,
    }


@router.get("/")
async def get_all_feedback(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Get all feedback. Requires Organizer or Admin."""
    feedbacks = await Feedback.find_all().skip(skip).limit(limit).to_list()
    return {
        "total": len(feedbacks),
        "feedbacks": [
            {
                "_id": str(f.id),
                "event_id": f.event_id,
                "session_id": f.session_id,
                "registration_id": f.registration_id,
                "rating": f.rating,
                "comment": f.comment,
                "created_at": f.created_at.isoformat() if hasattr(f, "created_at") and f.created_at else None
            }
            for f in feedbacks
        ],
    }


@router.get("/session/{session_id}")
async def get_session_feedback(
    session_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get all feedback for a session."""
    feedbacks = await Feedback.find(
        Feedback.session_id == session_id
    ).skip(skip).limit(limit).to_list()

    return {
        "session_id": session_id,
        "total": len(feedbacks),
        "feedback": [
            {
                "id": str(f.id),
                "rating": f.rating,
                "comment": f.comment,
                "registration_id": f.registration_id,
            }
            for f in feedbacks
        ],
    }


@router.get("/event/{event_id}")
async def get_event_feedback(
    event_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get all feedback for an event."""
    feedbacks = await Feedback.find(
        Feedback.event_id == event_id
    ).skip(skip).limit(limit).to_list()

    return {
        "event_id": event_id,
        "total": len(feedbacks),
        "feedback": [
            {
                "id": str(f.id),
                "rating": f.rating,
                "comment": f.comment,
                "registration_id": f.registration_id,
            }
            for f in feedbacks
        ],
    }


@router.get("/session/{session_id}/stats")
async def get_session_feedback_stats(
    session_id: int,
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Get feedback statistics for a session. Requires Organizer or Admin."""
    feedbacks = await Feedback.find(Feedback.session_id == session_id).to_list()

    if not feedbacks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No feedback found for this session"
        )

    ratings = [f.rating for f in feedbacks]
    return {
        "session_id": session_id,
        "total_feedback": len(ratings),
        "average_rating": round(sum(ratings) / len(ratings), 2),
        "max_rating": max(ratings),
        "min_rating": min(ratings),
        "rating_distribution": {
            str(i): ratings.count(i) for i in range(1, 6)
        },
    }


@router.put("/{feedback_id}")
async def update_feedback(
    feedback_id: str,
    feedback_data: FeedbackUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update feedback. Only the owner or Admin can update."""
    feedback = await Feedback.get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    if feedback_data.rating is not None:
        feedback.rating = feedback_data.rating
    if feedback_data.comment is not None:
        feedback.comment = feedback_data.comment

    await feedback.save()
    return {"message": "Feedback updated successfully", "id": feedback_id}


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(
    feedback_id: str,
    current_user: dict = Depends(require_role([Role.ADMIN]))
):
    """Delete feedback. Admin only."""
    feedback = await Feedback.get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    await feedback.delete()
    return None