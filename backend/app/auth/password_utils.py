import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _pre_hash(password: str) -> bytes:
    """
    Pre-hash password with SHA256 to avoid bcrypt's 72 byte limit.
    Using .digest() ensures the output is exactly 32 raw bytes, 
    preventing any truncation issues.
    """
    return hashlib.sha256(password.encode('utf-8')).digest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_pre_hash(plain_password), hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(_pre_hash(password))
