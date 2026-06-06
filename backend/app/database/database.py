import asyncio
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from app.core.logger import get_logger
from sqlalchemy import text

logger = get_logger(__name__)

Base = declarative_base()

# Create async engine and sessionmaker
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session."""
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        logger.exception("Session rollback because of exception")
        raise
    finally:
        await session.close()

async def try_connect(retries: int = 3, delay: float = 1.0) -> None:
    """Try to acquire a single connection to the DB to validate connectivity."""
    last_exc: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return
        except Exception as exc:
            last_exc = exc
            logger.debug("DB connect attempt %s failed: %s", attempt, exc)
            await asyncio.sleep(delay)
    logger.error("Unable to connect to DB after %s attempts", retries)
    raise last_exc or RuntimeError("Unknown DB connectivity error")
