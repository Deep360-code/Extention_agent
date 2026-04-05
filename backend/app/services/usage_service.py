from datetime import datetime, timezone
import logging
from app.database.prisma_client import db
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

FREE_PLAN_LIMIT = 50

async def check_and_increment_usage(user_id: str, plan_type: str, required_tokens: int = 0) -> bool:
    """
    Checks if the user has exceeded their daily limit.
    If not, increments the request count and token count.
    """
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get or create today's usage record
    usage = await db.api_usage.find_first(
        where={
            "user_id": user_id,
            "date": {"gte": today}
        }
    )
    
    if not usage:
        usage = await db.api_usage.create(
            data={
                "user_id": user_id,
                "request_count": 0,
                "tokens_used": 0,
                # date defaults to today in schema
            }
        )
        
    if plan_type.lower() == "free" and usage.request_count >= FREE_PLAN_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Daily limit of {FREE_PLAN_LIMIT} requests reached for free plan."
        )
        
    # Increment usage
    try:
        await db.api_usage.update(
            where={"id": usage.id},
            data={
                "request_count": {"increment": 1},
                "tokens_used": {"increment": required_tokens}
            }
        )
    except Exception as e:
        logger.error(f"Failed to increment usage for user {user_id}: {str(e)}")
        # We might not want to block the request if the update fails, but typically we do
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track usage"
        )
        
    return True

async def get_user_usage(user_id: str):
    """
    Retrieves the user's current usage for today.
    """
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    usage = await db.api_usage.find_first(
        where={
            "user_id": user_id,
            "date": {"gte": today}
        }
    )
    
    if not usage:
        return {"request_count": 0, "tokens_used": 0, "date": today.isoformat()}
        
    return {
        "request_count": usage.request_count,
        "tokens_used": usage.tokens_used,
        "date": usage.date.isoformat()
    }
