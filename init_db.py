import asyncio
from app.db.session import engine, Base
from app.models import User, Lead

async def init_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized!")

if __name__ == "__main__":
    asyncio.run(init_db())
