from ultralytics import YOLO
from config import MODEL_PATH, VEHICLE_CLASSES, CONFIDENCE_THRESHOLD

# Load the pretrained YOLO model

model = YOLO(MODEL_PATH)

results = model('images/traffic.png')

result = results[0]

result.save('output/traffic_yolo_detected.png')

vehicle_count = 0

# Run object detection on the traffic image
for box in result.boxes:
    class_id = int(box.cls[0])
    confidence = float(box.conf[0])

    class_name = model.names[class_id]

    # Filter detected objects and count vehicles
    if class_name in VEHICLE_CLASSES and confidence >= CONFIDENCE_THRESHOLD:
        vehicle_count += 1

        print(
            f'{class_name} | '
            f'confidence: {confidence:.2f}'
        )

print('Total vehicles:', vehicle_count)