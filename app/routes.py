from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
from pathlib import Path

router = APIRouter(prefix="/api")

EVENTS_FILE = Path("output/events.json")

def ensure_file():
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not EVENTS_FILE.exists():
        EVENTS_FILE.write_text("[]", encoding="utf-8")

@router.get("/streams")
def get_streams():
    return {
        "streams": [
            {"id": "demo_stream", "name": "Demo Camera", "status": "idle"},
            {"id": "camera_01", "name": "Camera 01", "status": "ready"},
        ]
    }

@router.post("/streams")
def create_stream(payload: Dict[str, Any]):
    if "name" not in payload:
        raise HTTPException(status_code=400, detail="Stream name is required")
    return {
        "message": "Stream created",
        "stream": {
            "id": payload.get("id", "custom_stream"),
            "name": payload["name"],
            "status": "registered",
        }
    }

@router.get("/events")
def get_events():
    ensure_file()
    with EVENTS_FILE.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return {"events": data}

@router.get("/stats")
def get_stats():
    return {
        "total_vehicles": 0,
        "overspeed_events": 0,
        "plates_detected": 0,
        "status": "no data yet",
    }
