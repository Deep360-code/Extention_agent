from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.middleware.rate_limiter import rate_limit
from app.services.llm_service import get_groq_response
from app.database.prisma_client import db

router = APIRouter(prefix="/llm", tags=["llm"])

class LLMQuery(BaseModel):
    prompt: str
    model: str = "llama3-70b-8192"

@router.post("/query")
async def query_llm(query_data: LLMQuery, user = Depends(rate_limit)):
    """
    Endpoint protected by rate_limit (which verifies JWT and checks daily usage).
    Fetches response from Groq LLM service.
    """
    try:
        response_data = await get_groq_response(
            prompt=query_data.prompt,
            model=query_data.model
        )
        
        # After successful call, optionally update the token count directly
        # Since rate_limit already bumped request_count by 1
        from datetime import datetime, timezone
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        await db.api_usage.update_many(
            where={
                "user_id": user.id,
                "date": {"gte": today}
            },
            data={
                "tokens_used": {"increment": response_data["tokens_used"]}
            }
        )
            
        return {"response": response_data["content"]}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error communicating with LLM service: {str(e)}"
        )
