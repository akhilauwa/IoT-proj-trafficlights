# from ultralytics import YOLO
# import cv2
# import cvzone
# import math
# import time
# from sort import *
# import numpy as np

# cap = cv2.VideoCapture(0)  # For Webcam
# cap.set(3, 1280)
# cap.set(4, 720)

# model = YOLO("Yolo-Weights/ToyCar.pt")

# classNames = ["car"]

# # Tracking
# tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))

# # Extend the limit across the middle of the screen
# middle_y = frame_height // 2
# limits = [0, middle_y, frame_width, middle_y]
# totalCount = []

# while True:
#     success, img = cap.read()

#     imgGraphics = cv2.imread("Images/graphics.png", cv2.IMREAD_UNCHANGED)
#     imgGraphics = cv2.resize(imgGraphics, (100, 100))  # Resize graphic
#     img = cvzone.overlayPNG(img, imgGraphics, (10, 10))  # Adjust position
#     results = model(img, stream=True)

#     detections = np.empty((0, 5))

#     for r in results:
#         boxes = r.boxes
#         for box in boxes:
#             # Bounding Box
#             x1, y1, x2, y2 = box.xyxy[0]
#             x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#             w, h = x2 - x1, y2 - y1

#             # Confidence
#             conf = math.ceil((box.conf[0] * 100)) / 100
#             # Class Name
#             cls = int(box.cls[0])
#             currentClass = classNames[cls]

#             if currentClass == "car" or currentClass == "truck" or currentClass == "bus" \
#                     or currentClass == "motorbike" and conf > 0.3:
#                 currentArray = np.array([x1, y1, x2, y2, conf])
#                 detections = np.vstack((detections, currentArray))

#     resultsTracker = tracker.update(detections)

#     cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
#     for result in resultsTracker:
#         x1, y1, x2, y2, id = result
#         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#         w, h = x2 - x1, y2 - y1
#         cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
#         cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
#                            scale=0.8, thickness=1, offset=10)  # Adjust scale

#         cx, cy = x1 + w // 2, y1 + h // 2
#         cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

#         if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
#             if totalCount.count(id) == 0:
#                 totalCount.append(id)
#                 cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

#     cv2.putText(img, str(len(totalCount)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 255), 4)  # Adjust position and size

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


# This version quits after pressing q and print the total count 


from ultralytics import YOLO
import cv2
import cvzone
import math
import time
from sort import *
import numpy as np

cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("Yolo-Weights/ToyCar.pt")

classNames = ["car"]

# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Extend the limit across the middle of the screen
middle_y = frame_height // 2
limits = [0, middle_y, frame_width, middle_y]
totalCount = []

while True:
    success, img = cap.read()

    imgGraphics = cv2.imread("Images/graphics.png", cv2.IMREAD_UNCHANGED)
    imgGraphics = cv2.resize(imgGraphics, (100, 100))  # Resize graphic
    img = cvzone.overlayPNG(img, imgGraphics, (10, 10))  # Adjust position
    results = model(img, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "car" and conf > 0.3:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultsTracker = tracker.update(detections)

    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                           scale=0.8, thickness=1, offset=10)  # Adjust scale

        cx, cy = x1 + w // 2, y1 + h // 2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:
            if totalCount.count(id) == 0:
                totalCount.append(id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

    cv2.putText(img, str(len(totalCount)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 255), 4)  # Adjust position and size

    cv2.imshow("Image", img)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Print the total count after the program finishes
print(f"Total Count: {len(totalCount)}")

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
