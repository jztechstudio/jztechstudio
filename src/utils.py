import csv
from pathlib import Path

def compute_speed_kmh(distance_meters: float, time_seconds: float) -> float:
    if time_seconds <= 0:
        return 0.0
    speed_ms = distance_meters / time_seconds
    return speed_ms * 3.6

def export_csv_report(report: dict, path: str):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["frames_processed", "total_detections"]
    row = {
        "frames_processed": report.get("frames_processed", 0),
        "total_detections": report.get("total_detections", 0),
    }

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)

    # Additional class counts:
    counts = report.get("vehicle_counts", {})
    if counts:
        with output_path.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([])
            writer.writerow(["class", "count"])
            for key, value in counts.items():
                writer.writerow([key, value])
