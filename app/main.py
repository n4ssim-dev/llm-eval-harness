from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings

app = FastAPI(title=get_settings().app_name)
app.include_router(api_router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
