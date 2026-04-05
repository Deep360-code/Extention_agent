from prisma import Prisma
from app.config import settings

# Global Prisma client instance
db = Prisma(datasource={'url': settings.DATABASE_URL})

async def connect_db():
    if not db.is_connected():
        await db.connect()

async def disconnect_db():
    if db.is_connected():
        await db.disconnect()
