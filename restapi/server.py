from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging
import os

from restapi.core.config import settings
from restapi.db.models.base import Base, BaseModel
from restapi.db.session import SessionLocal, engine
from restapi.api.v1 import router as v1_router

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
BaseModel.set_session(SessionLocal)

class SessionCleanupMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        finally:
            SessionLocal.remove()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Fleet management REST API",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    logger.error(f"Validation error on {request.method} {request.url.path}: {errors}")
    for error in errors:
        logger.error(f"  - Field: {'.'.join(str(x) for x in error['loc'])}, Error: {error['msg']}, Type: {error['type']}")
    return JSONResponse(
        status_code=422,
        content={"detail": [{"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in errors]},
    )

# Serve dashboard HTML
@app.get("/", include_in_schema=False)
async def serve_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "fleetpulse_dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path, media_type="text/html")
    return JSONResponse({"error": "Dashboard not found"}, status_code=404)

app.add_middleware(SessionCleanupMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")