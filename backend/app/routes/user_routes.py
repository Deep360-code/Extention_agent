from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "plan_type": current_user.plan_type,
        "created_at": current_user.created_at
    }
