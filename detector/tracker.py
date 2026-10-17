from collections import defaultdict

class VehicleTracker:
    def __init__(self):
        self.track_history = defaultdict(list)
        self.next_id = 1

    def update_track(self, bbox, class_name, frame_count):
        track_id = self.next_id
        self.next_id += 1
        self.track_history[track_id].append({
            "frame": frame_count,
            "bbox": bbox,
            "class": class_name,
        })
        return track_id
