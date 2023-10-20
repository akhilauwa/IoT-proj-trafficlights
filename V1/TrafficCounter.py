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
import time
from sort import *
import numpy as np

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class TrafficCounter:
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

    def initialize_capture(self):
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.middle_y = self.frame_height // 2
        self.limits = [0, self.middle_y, self.frame_width, self.middle_y]

    def counter(self):
        self.initialize_capture()  # Initialize VideoCapture
        while self.is_running:
            success, img = self.cap.read()
            imgGraphics = cv2.imread("Images/graphics.png", cv2.IMREAD_UNCHANGED)

            if imgGraphics is not None:
                imgGraphics = cv2.resize(imgGraphics, (100, 100))
                img = cvzone.overlayPNG(img, imgGraphics, (10, 10))

            # sys.stdout = open(os.devnull, 'w')
            results = self.model(img, stream=True)
            # sys.stdout = sys.__stdout__
            detections = np.empty((0, 5))

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    currentClass = self.classNames[cls]

                    if currentClass == "car" and conf > 0.3:
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))

            resultsTracker = self.tracker.update(detections)

            cv2.line(img, (self.limits[0], self.limits[1]), (self.limits[2], self.limits[3]), (0, 0, 255), 5)
            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                                   scale=0.8, thickness=1, offset=10)
                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if self.limits[0] < cx < self.limits[2] and self.limits[1] - 30 < cy < self.limits[1] + 30:
                    if id not in self.totalCount:
                        self.totalCount.append(id)
                        cv2.line(img, (self.limits[0], self.limits[1]), (self.limits[2], self.limits[3]), (0, 255, 0), 5)

            cv2.putText(img, str(len(self.totalCount)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 255), 4)
            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if self.cap is not None:
            self.cap.release()  # Release VideoCapture
        cv2.destroyAllWindows()  # Close OpenCV windows
    
    # This method is used to count cars (NOT WORKING)
    def count_cars(self, run_time=60):
        self.is_running = True
        self.thread = threading.Thread(target=self.counter)
        self.thread.start()

    # This method is used to get the car count (NOT WORKING)
    def get_count(self, run_time=60):    
        self.totalCount = []
        start_time = time.time()
        while (time.time() - start_time) < run_time:
            continue
        return len(self.totalCount)
    
    # This method is used to stop counting cars (NOT WORKING)
    def stop_counting(self):
        self.is_running = False
        self.thread.join()
        self.totalCount = []

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

if __name__ == "__main__":
    counter = TrafficCounter()
    while True:
        command = input("Enter 'start' to count objects for a specified time or 'exit' to quit: ")
        if command == 'start':
            run_time = int(input("Enter the run time (in seconds): "))
            total_count = counter.count_cars_for_time(run_time)
            print(f"Total Count: {total_count}")
        elif command == 'exit':
            break
