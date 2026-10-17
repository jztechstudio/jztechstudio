import cv2
import numpy as np
from pathlib import Path
from detector.model import DetectionModel
from detector.tracker import VehicleTracker
from src.utils import compute_speed_kmh, export_csv_report

class VideoRunner:
    def __init__(self, model_path=None):
        self.model = DetectionModel(model_path=model_path)
        self.tracker = VehicleTracker()
        self.line_y = 300
        self.previous_frame = None

    def process_video(self, video_path: str, output_path: str = None):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        frame_count = 0
        detections = []
        vehicle_counts = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            results = self.model.predict_frame(frame)
            result = results[0]

            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cls_id = int(box.cls[0].item())
                    cls_name = result.names.get(cls_id, "unknown")
                    conf = float(box.conf[0].item())

                    if cls_name in self.model.get_vehicle_classes():
                        track_id = self.tracker.update_track(
                            (x1, y1, x2, y2), cls_name, frame_count
                        )
                        detections.append({
                            "frame": frame_count,
                            "class": cls_name,
                            "track_id": track_id,
                            "bbox": [x1, y1, x2, y2],
                            "confidence": conf,
                        })

                        vehicle_counts[cls_name] = vehicle_counts.get(cls_name, 0) + 1

            # Example line crossing logic
            cv2.line(frame, (0, self.line_y), (frame.shape[1], self.line_y), (0, 255, 0), 2)

            if output_path:
                cv2.imwrite(output_path, frame)

        cap.release()

        report = {
            "frames_processed": frame_count,
            "vehicle_counts": vehicle_counts,
            "total_detections": len(detections),
        }

        export_csv_report(report, "output/report.csv")
        return report
