from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes_query import router as query_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)


@app.get("/health")
def health():
    return {"status": "ok"}
    
@app.get("/debug-openai-key")
def debug_openai_key():
    from app.core.config import settings
    key = settings.OPENAI_API_KEY or ""
    return {"prefix": key[:15], "length": len(key)}
