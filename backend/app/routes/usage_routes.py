from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user
from app.services.usage_service import get_user_usage

router = APIRouter(prefix="/usage", tags=["usage"])

@router.get("/")
async def get_usage(current_user = Depends(get_current_user)):
    """
    Returns the current usage details for today.
    """
    usage_data = await get_user_usage(current_user.id)
    return usage_data
