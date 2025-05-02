from PyQt5 import QtCore, QtGui
import cv2
from datetime import datetime

class VideoThread(QtCore.QThread):
    # change_pixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    # log_signal = QtCore.pyqtSignal(str)
    # photo_signal = QtCore.pyqtSignal(object, object, str)
    change_pixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    log_signal    = QtCore.pyqtSignal(str)
    # (full_frame:numpy, crops:list[numpy], bboxes:list[tuple], label:str)
    photo_signal  = QtCore.pyqtSignal(object, list, list, str)
    def __init__(self, detector,source=0,):
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
            now_time = datetime.now()
            if (now_time - pre_time).total_seconds() >= 5:
                full_frame = frame.copy()
                rgb_detect, crops, bboxes, labels = self.detector.detect(rgb)
                # 按标签分组
                from collections import defaultdict
                grouped = defaultdict(lambda: {'crops': [], 'bboxes': []})
                for crop, bbox, label in zip(crops, bboxes, labels):
                    grouped[label]['crops'].append(crop)
                    grouped[label]['bboxes'].append(bbox)

                # 发日志和截图信号
                self.log_signal.emit(now_time.strftime("%Y-%m-%d %H:%M:%S"))
                for label, data in grouped.items():
                    count = len(data['crops'])
                    self.log_signal.emit(f"Detected {label}: {count} 人")
                    if label in ["Using_phone", "sleep","turn_head"]:
                        self.photo_signal.emit(
                            full_frame,
                            data['crops'],
                            data['bboxes'],
                            label
                        )
                self.log_signal.emit("")  # 空行分隔
                pre_time = now_time

            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qimg = QtGui.QImage(
                rgb.data, w, h, bytes_per_line,
                QtGui.QImage.Format_RGB888
            )
            self.change_pixmap.emit(QtGui.QPixmap.fromImage(qimg))
            self.msleep(10)
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
