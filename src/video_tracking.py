import cv2 as cv
from ultralytics import YOLO
import csv

from ultralytics import YOLO

from config import (
    VEHICLE_CLASSES,
    LINE_Y,
    CONFIDENCE_THRESHOLD,
    MODEL_PATH,
    INPUT_VIDEO,
    OUTPUT_VIDEO,
    OUTPUT_CSV
)

from utils import (
    get_center,
    get_traffic_status,
    draw_statistics
)

model = YOLO(MODEL_PATH)
video = cv.VideoCapture(INPUT_VIDEO)

# Initialize vehicle tracking and counting
counted_ids = set()
previous_positions = {}
vehicle_count = 0
vehicle_counts = {
    'car': 0,
    'truck': 0,
    'bus': 0,
    'motorcycle': 0
}
fps = int(video.get(cv.CAP_PROP_FPS))
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'mp4v')
writer = cv.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

csv_file = open(OUTPUT_CSV, 'w', newline='')

csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    'Track ID',
    'Type',
    'Confidence'
])

# Process video frame by frame
while True:
    success, frame = video.read()

    if not success:
        break

# Run YOLO detection and tracking
    results = model.track(
        frame,
        persist=True,
        verbose=False
    )
    result = results[0]
    annotated_frame = result.plot()

    cv.line(frame, (0, LINE_Y), (frame.shape[1], LINE_Y), (255, 0, 0), 3)

    if result.boxes.id is not None:
        boxes = result.boxes

        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            track_id = int(box.id[0])

            class_name = model.names[class_id]

            center_x, center_y = get_center(box.xyxy[0])

            if class_name in VEHICLE_CLASSES and confidence >= CONFIDENCE_THRESHOLD:
                cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                # Count each vehicle once when it crosses the line
                if track_id  in previous_positions:
                    previous_y = previous_positions[track_id]

                    if previous_y < LINE_Y and center_y >= LINE_Y:
                        if track_id not in counted_ids:
                            counted_ids.add(track_id)
                            vehicle_count += 1
                            vehicle_counts[class_name] += 1

                            csv_writer.writerow([
                                track_id,
                                class_name,
                                round(confidence, 2)
                            ])

                            # print(f"Vehicle counted! ID: {track_id}")
                            # print("Type:", class_name)
                            # print("Total vehicles:", vehicle_count)
                            # print("Counts:", vehicle_counts)

                previous_positions[track_id] = center_y  

    # Display traffic statistics
    traffic_status = get_traffic_status(vehicle_count)

    draw_statistics(
                annotated_frame,
                vehicle_count,
                vehicle_counts,
                traffic_status
                )
    
    writer.write(annotated_frame)
    cv.imshow('Traffic Video', annotated_frame)

    key = cv.waitKey(20) & 0xFF

    if key == ord('q'):
        break

    if cv.getWindowProperty('Traffic Video', cv.WND_PROP_VISIBLE) < 1:
        break

video.release()
writer.release()
csv_file.close()
cv.destroyAllWindows()