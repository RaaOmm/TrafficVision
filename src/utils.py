import cv2 as cv

# this file contains utility functions used in the main video tracking script





# the functions include getting the center of a bounding box
def get_center(box):
    x1, y1, x2, y2 = box

    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)

    return center_x, center_y


def get_traffic_status(vehicle_count):
    if vehicle_count < 5:
        return 'LOW'
    elif vehicle_count < 10:
        return 'MODERATE'
    else:
        return 'HIGH'


def draw_statistics(frame, vehicle_count, vehicle_counts, traffic_status):

    cv.putText(
        frame,
        f'Total Vehicles: {vehicle_count}',
        (30, 50),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv.putText(
        frame,
        f"Cars: {vehicle_counts['car']}",
        (30, 90),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv.putText(
        frame,
        f"Trucks: {vehicle_counts['truck']}",
        (30, 125),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv.putText(
        frame,
        f"Buses: {vehicle_counts['bus']}",
        (30, 160),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv.putText(
        frame,
        f"Motorcycles: {vehicle_counts['motorcycle']}",
        (30, 195),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv.putText(
        frame,
        f'Traffic: {traffic_status}',
        (30, 240),
        cv.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )