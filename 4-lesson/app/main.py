from fastapi import FastAPI
from app.core.redis import lifespan
from app.core.logging import setup_logging
from app.routers.news import router as news_router

app = FastAPI(lifespan=lifespan)
setup_logging()
app.include_router(news_router)
