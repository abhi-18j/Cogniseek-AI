from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import setup_logging, get_logger
from app.middleware.exceptions import register_exception_handlers

setup_logging()
logger = get_logger(__name__)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application")
    try:
        from app.database.database import try_connect
        await try_connect(retries=5, delay=1)
        logger.info("Database connectivity confirmed")
    except Exception as exc:
        logger.warning("Database connectivity check failed at startup: %s", exc)


@app.get("/", response_class=JSONResponse)
async def root():
    return {"message": f"{settings.APP_NAME} is running"}


@app.get("/health", response_class=JSONResponse)
async def health():
    return {"status": "healthy"}


# Register global exception handlers (logs + JSON)
register_exception_handlers(app)
