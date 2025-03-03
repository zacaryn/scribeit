from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime, timedelta

from ...db.database import get_db
from ...models.user import User
from ...models.summary import Summary
from ...core.auth import get_current_active_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/summaries")
async def get_user_summaries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a list of user's summaries for dashboard
    """
    logger.info(f"Fetching summaries for user: {current_user.email}")
    
    # Query user's summaries
    summaries = db.query(Summary).filter(
        Summary.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # If no summaries found, return empty list
    if not summaries:
        return []
    
    # Format the response
    formatted_summaries = []
    for summary in summaries:
        formatted_summaries.append({
            "id": summary.id,
            "title": summary.title,
            "status": summary.status,
            "created_at": summary.created_at.strftime("%B %d, %Y"),
            "source_type": summary.source_type,
            "duration_minutes": round(summary.duration_seconds / 60) if summary.duration_seconds else None,
            "minutes_charged": summary.minutes_charged
        })
    
    return formatted_summaries

@router.get("/usage")
async def get_user_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user's usage statistics
    """
    logger.info(f"Fetching usage stats for user: {current_user.email}")
    
    # Return user's subscription details
    usage_stats = {
        "tier": current_user.subscription_tier,
        "minutesUsed": current_user.minutes_used,
        "minutesTotal": current_user.minutes_remaining + current_user.minutes_used,
        "minutesRemaining": current_user.minutes_remaining,
        "subscriptionStatus": current_user.subscription_status,
        "renewalDate": current_user.subscription_renewal_date.strftime("%B %d, %Y") if current_user.subscription_renewal_date else None
    }
    
    return usage_stats 