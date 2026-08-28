

# Vehicle detection settings

VEHICLE_CLASSES = ['car', 'truck', 'bus', 'motorcycle']

LINE_Y = 600

CONFIDENCE_THRESHOLD = 0.5

# YOLO model settings
MODEL_PATH = 'yolo11n.pt'

# Input and output paths
INPUT_VIDEO = 'videos/traffic.mp4'
OUTPUT_VIDEO = 'output/traffic_counted.mp4'
OUTPUT_CSV = 'output/traffic_data.csv'