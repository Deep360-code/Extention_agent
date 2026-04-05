from fastapi import Depends
from app.middleware.auth_middleware import get_current_user
from app.services.usage_service import check_and_increment_usage
from app.database.prisma_client import db

async def rate_limit(user=Depends(get_current_user)):
    """
    Dependency to check if the user has reached their daily usage limit.
    This also increments their request usage.
    """
    # Assuming user.plan_type exists
    plan_type = getattr(user, "plan_type", "free")
    
    # We call check_and_increment_usage with 0 tokens. Tokens will be updated
    # at the time of the LLM call using the specific route if needed,
    # but for simplicity, we count 1 request here. If tokens are needed later,
    # we can update the usage record again or just do it all at once during the LLM call.
    # We'll increment the request right away.
    await check_and_increment_usage(user.id, plan_type=plan_type, required_tokens=0)
    return user
