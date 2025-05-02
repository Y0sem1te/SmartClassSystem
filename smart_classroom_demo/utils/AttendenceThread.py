from PyQt5 import QtCore, QtGui
import cv2
from datetime import datetime
import numpy as np


class AttendenceThread(QtCore.QThread):
    change_pixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    frame_signal  = QtCore.pyqtSignal(np.ndarray)
    signin_signal = QtCore.pyqtSignal(list)
    def __init__(self,detector,source=0):
        super().__init__()
        self._running = False
        self._paused = False
        self.source = source
        self.cap = None
        self.detector = detector

    def run(self):
        self._running = True
        self.cap = cv2.VideoCapture(self.source)
        pre_time = datetime.now()
        while self._running and self.cap.isOpened():
            if self._paused:
                self.msleep(100)
                continue
            ret, frame = self.cap.read()     
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locs = self.detector.face_detection.face_location(rgb)
            if not len(locs):
                for (x1, y1, x2, y2) in locs:
                    # 在 RGB 图上画绿框
                    cv2.rectangle(rgb,
                                  (int(x1), int(y1)),
                                  (int(x2), int(y2)),
                                  (0, 255, 0),
                                  2)
            self.frame_signal.emit(rgb)
            ids = self.detector.sign_in(rgb)
            if ids:
                self.signin_signal.emit(ids)
            self.msleep(30)
        self.cap.release()

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._running = False
        self._paused = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.wait()