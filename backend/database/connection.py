import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from urllib.parse import urlparse

class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()

async def get_database():
    return db.database


def _extract_db_name(mongo_url: str) -> str:
    try:
        parsed = urlparse(mongo_url)
        # path like "/ai_browser" -> ai_browser
        if parsed.path and len(parsed.path) > 1:
            return parsed.path.lstrip('/')
    except Exception:
        pass
    # Fallback default
    return "ai_browser"


async def connect_to_mongo():
    """Create database connection using only MONGO_URL from environment.
    Database name is derived from the URL path if present (no hardcoding).
    """
    mongo_url = os.environ.get("MONGO_URL")
    if not mongo_url:
        raise RuntimeError("MONGO_URL is not set in environment")

    db.client = AsyncIOMotorClient(
        mongo_url,
        server_api=ServerApi('1')
    )

    # Derive database name from URL, fallback to sensible default
    db_name = _extract_db_name(mongo_url)
    db.database = db.client.get_database(db_name)

    # Test connection
    try:
        await db.client.admin.command('ping')
        print(f"Successfully connected to MongoDB! Using database: {db_name}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")