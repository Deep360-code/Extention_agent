import logging
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_token
from app.database.prisma_client import db

logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)

async def get_current_user(request: Request, creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    auth_header = request.headers.get("Authorization")
    logger.info(f"[Auth Middleware] Raw Authorization Header: {auth_header}")
    
    if not creds or not creds.credentials:
        logger.error("[Auth Middleware] No credentials extracted. Did you send 'Bearer <token>'?")
        raise credentials_exception

    token_str = creds.credentials
    logger.info(f"[Auth Middleware] Extracted Token: {token_str[:15]}... (truncated)")

    # This will raise HTTP 401 directly if invalid/expired due to our updated jwt_handler logic
    payload = decode_token(token_str)
    
    user_id: str = payload.get("sub")
    if not user_id:
        logger.error("[Auth Middleware] JWT payload missing 'sub' subject field.")
        raise credentials_exception

    # Ensure database connection is active before querying
    if not db.is_connected():
        logger.warning("[Auth Middleware] DB was disconnected. Reconnecting now...")
        await db.connect()

    logger.info(f"[Auth Middleware] Looking up user in DB with ID: {user_id}")
    user = await db.user.find_unique(where={"id": user_id})
    if user is None:
        logger.error(f"[Auth Middleware] User ID {user_id} embedded in token no longer exists in DB.")
        raise credentials_exception
        
    user_email = getattr(user, "email", "Unknown")
    logger.info(f"[Auth Middleware] Successfully authenticated full user object: {user_email}")
    return user
