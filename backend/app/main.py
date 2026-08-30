import sys
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.routes import health, dashboard, demo, alerts, analyze, graph, cases, dataset, ml_info

# Setup logging
setup_logging()

docs_url = "/docs" if settings.ENABLE_DOCS else None
redoc_url = "/redoc" if settings.ENABLE_DOCS else None
openapi_url = "/openapi.json" if settings.ENABLE_DOCS else None

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Explainable, Read-Only Bitcoin Transaction Risk Analysis Platform (SIH26146)",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} -> status {response.status_code} ({duration_ms}ms)")
    return response

# Root health check endpoint for cloud probes
@app.get("/health", tags=["Health"])
def root_health():
    return health.get_health()

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.seed.seed_users import seed_demo_user
from app.api.routes import health, dashboard, demo, alerts, analyze, graph, cases, dataset, ml_info, auth

# Initialize DB schema and seed default demo user
try:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db_session:
        seed_demo_user(db_session)
except Exception as e:
    logger.warning(f"DB startup initialization note: {e}")

# Include API v1 routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(demo.router, prefix=f"{settings.API_V1_STR}/demo", tags=["Demo"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_STR}/alerts", tags=["Alerts"])
app.include_router(analyze.router, prefix=f"{settings.API_V1_STR}/analyze", tags=["Analysis"])
app.include_router(graph.router, prefix=f"{settings.API_V1_STR}/graph", tags=["Graph"])
app.include_router(cases.router, prefix=f"{settings.API_V1_STR}/cases", tags=["Cases"])
app.include_router(dataset.router, prefix=f"{settings.API_V1_STR}/dataset", tags=["Dataset Generator"])
app.include_router(ml_info.router, prefix=f"{settings.API_V1_STR}/ml", tags=["Machine Learning"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
