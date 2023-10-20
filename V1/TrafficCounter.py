'''
This file is used to count the number of cars in a video stream
Runs on YOLO Server
Written by: Robbie Baiou
'''

import threading
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *
import numpy as np

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class TrafficCounter:
    # Initialize the TrafficCounter object
    def __init__(self, model_path=basedir+"/Yolo-Weights/ToyCar.pt"):
        self.model = YOLO(model_path)
        self.classNames = ["car"]
        self.tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
        self.cap = None  # Initialize VideoCapture as None
        self.frame_width = 0
        self.frame_height = 0
        self.middle_y = 0
        self.limits = [0, 0, 0, 0]
        self.totalCount = []
        self.is_running = False
        self.thread = None

    # This method is used to initialize the VideoCapture
    def initialize_capture(self):
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.middle_y = self.frame_height // 2
        self.limits = [0, self.middle_y, self.frame_width, self.middle_y]

    # This method is used to count cars
    def counter(self):
        self.initialize_capture()  # Initialize VideoCapture
        while self.is_running:
            # Read the image from the VideoCapture
            success, img = self.cap.read()
            imgGraphics = cv2.imread("Images/graphics.png", cv2.IMREAD_UNCHANGED)

            # Resize the image
            if imgGraphics is not None:
                imgGraphics = cv2.resize(imgGraphics, (100, 100))
                img = cvzone.overlayPNG(img, imgGraphics, (10, 10))

            # sys.stdout = open(os.devnull, 'w')
            results = self.model(img, stream=True)
            # sys.stdout = sys.__stdout__
            detections = np.empty((0, 5))

            # Loop through the results
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Get the coordinates, width, height, confidence, and class of the box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    currentClass = self.classNames[cls]
                    # Only count cars
                    if currentClass == "car" and conf > 0.3:
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))
            
            # Update the tracker
            resultsTracker = self.tracker.update(detections)

            # Draw the boxes and count the cars
            cv2.line(img, (self.limits[0], self.limits[1]), (self.limits[2], self.limits[3]), (0, 0, 255), 5)
            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                # Draw the box
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                                   scale=0.8, thickness=1, offset=10)
                cx, cy = x1 + w // 2, y1 + h // 2

                # Draw the center point
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # Count the cars when it crosses the line
                if self.limits[0] < cx < self.limits[2] and self.limits[1] - 30 < cy < self.limits[1] + 30:
                    if id not in self.totalCount:
                        self.totalCount.append(id)
                        cv2.line(img, (self.limits[0], self.limits[1]), (self.limits[2], self.limits[3]), (0, 255, 0), 5)

            # Display the total count
            cv2.putText(img, str(len(self.totalCount)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 255), 4)
            cv2.imshow("Image", img)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the VideoCapture and close all OpenCV windows
        if self.cap is not None:
            self.cap.release()  # Release VideoCapture
        cv2.destroyAllWindows()  # Close OpenCV windows

    # This method is used to count objects for a specified time
    def count_cars_for_time(self, run_time=60):
        self.is_running = True
        self.totalCount = []
        self.thread = threading.Thread(target=self.counter)
        self.thread.start()
        # Use threading.Timer to stop the counting after the specified run_time
        timer = threading.Timer(run_time, self.stop_counting)
        timer.start()

        # Wait for the thread to finish
        self.thread.join()

        # Cancel the timer
        timer.cancel()

        return len(self.totalCount)

    def stop_counting(self):
        self.is_running = False
