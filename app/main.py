from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import os
import uuid

from app.routes import router

app = FastAPI(
    title="Traffic Video Analyzer",
    description="Vehicle detection, counting, speed estimation, and event reporting from uploaded videos or live streams.",
    version="0.1.0",
)

# CORS for browser-based dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Traffic Video Analyzer is running",
        "status": "ok",
        "version": "0.1.0",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

ALLOWED_VIDEO_TYPES = {".mp4", ".avi", ".mov", ".mkv"}

UPLOAD_DIR = Path("output/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/api/upload-video")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="Only video files are allowed")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / unique_name

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(exc)}")

    return {
        "message": "Video uploaded successfully",
        "filename": file.filename,
        "saved_as": unique_name,
        "path": str(save_path),
    }
