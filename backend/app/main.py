from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.gemini_logger import logger
from app.api.api import api_router

app = FastAPI(
    title="US Stock Analyst Ver2",
    description="S-Class Financial Analysis Backend",
    version="2.0.0",
)

# CORS (Allow Frontend)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.log("system", "Backend Server Starting...", "main")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "US Stock Analyst Ver2 API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend"}
