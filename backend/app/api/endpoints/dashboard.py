from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime, timedelta

from ...db.database import get_db
from ...models.user import User
from ...models.summary import Summary
# In a real app you would have authentication
# from ...core.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/summaries")
async def get_user_summaries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    # In a real app, you would uncomment this:
    # current_user: User = Depends(get_current_user)
):
    """
    Get a list of user's summaries for dashboard
    """
    # For demo purposes, we're using a mock user
    # In a real app, you would use the authenticated user
    mock_user_id = "mock-user-123"
    
    try:
        summaries = db.query(Summary).filter(
            Summary.user_id == mock_user_id
        ).order_by(
            Summary.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return [
            {
                "id": summary.id,
                "title": summary.title,
                "status": summary.status,
                "source_type": summary.source_type,
                "created_at": summary.created_at,
                "minutes_charged": summary.minutes_charged or 0
            }
            for summary in summaries
        ]
        
    except Exception as e:
        logger.error(f"Error getting user summaries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usage")
async def get_user_usage(
    db: Session = Depends(get_db),
    # In a real app, you would uncomment this:
    # current_user: User = Depends(get_current_user)
):
    """
    Get user usage statistics for dashboard
    """
    # For demo purposes, we're using a mock user
    # In a real app, you would use the authenticated user
    mock_user_id = "mock-user-123"
    
    try:
        # Get mock user
        # In a real app, this would be current_user
        user = db.query(User).filter(User.id == mock_user_id).first()
        if not user:
            # Create a mock user for demo purposes
            user = User(
                id=mock_user_id,
                email="demo@example.com",
                first_name="Demo",
                last_name="User",
                subscription_tier="free",
                minutes_used=0,
                minutes_remaining=30
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Calculate usage
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_usage = db.query(Summary).filter(
            Summary.user_id == mock_user_id,
            Summary.created_at >= current_month_start,
            Summary.status == "completed"
        ).all()
        
        total_minutes_used = sum(s.minutes_charged or 0 for s in monthly_usage)
        
        # In a real app, this would be calculated based on subscription tier
        subscription_info = {
            "free": {"limit": 30, "name": "Free Tier"},
            "basic": {"limit": 300, "name": "Basic Plan"},
            "pro": {"limit": 1000, "name": "Pro Plan"}
        }
        
        tier_info = subscription_info.get(user.subscription_tier, subscription_info["free"])
        
        return {
            "subscription": {
                "tier": user.subscription_tier,
                "name": tier_info["name"],
                "minutes_limit": tier_info["limit"],
                "minutes_used": total_minutes_used,
                "minutes_remaining": tier_info["limit"] - total_minutes_used,
                "percentage_used": (total_minutes_used / tier_info["limit"]) * 100 if tier_info["limit"] > 0 else 100
            },
            "recent_usage": [
                {
                    "id": summary.id,
                    "title": summary.title,
                    "minutes_charged": summary.minutes_charged or 0,
                    "created_at": summary.created_at
                }
                for summary in monthly_usage[:5]  # Last 5 completed summaries
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting user usage: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 