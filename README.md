# Traffic Video Analyzer

A Python-based traffic monitoring MVP for:
- vehicle detection from uploaded video
- counting vehicles
- speed estimation
- overspeed evaluation
- basic event logs
- future ALPR integration

## Features
- Upload traffic video
- Detect vehicles using YOLO
- Count vehicles crossing a virtual line
- Export report to CSV
- FastAPI backend for API access
- Configurable streams and camera calibration

## Tech Stack
- Python
- FastAPI
- OpenCV
- Ultralytics YOLOv8
- NumPy
- PyYAML

## Project Structure
- `app/` — FastAPI backend
- `detector/` — detection, tracking, OCR
- `src/` — utility logic
- `config/` — stream and calibration config
- `output/` — uploads and reports

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Run
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API
- `GET /health`
- `POST /api/upload-video`
- `GET /api/streams`
- `GET /api/events`
- `GET /api/stats`

## Notes
This is an MVP scaffold. Real-world production-grade features like:
- RTSP multi-camera support
- accurate speed calibration
- plate recognition
- database persistence
- dashboard UI
- alerting system

are planned for the next stage.
