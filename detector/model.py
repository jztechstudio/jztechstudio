from ultralytics import YOLO
from pathlib import Path
import os

MODEL_PATH = Path("models/yolov8n.pt")

class DetectionModel:
    def __init__(self, model_path: str = None):
        if model_path:
            self.model_path = model_path
        else:
            self.model_path = str(MODEL_PATH)

        if not os.path.exists(self.model_path):
            self.model_path = "yolov8n.pt"

        self.model = YOLO(self.model_path)

    def predict_frame(self, frame, conf: float = 0.25):
        results = self.model(frame, conf=conf, verbose=False)
        return results

    def get_vehicle_classes(self):
        return {
            "car", "bus", "truck", "motorcycle", "bicycle", "person"
        }
