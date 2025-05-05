from PyQt5 import QtCore, QtGui
import cv2
from models.sentiment_detector import SentimentDetector
from datetime import datetime


class SentimentThread(QtCore.QThread):
    change_pixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    log_signal    = QtCore.pyqtSignal(str)     # 用于传日志文本 :contentReference[oaicite:6]{index=6}
    result_signal = QtCore.pyqtSignal(dict)    # 用于传情绪统计字典
    source_change = QtCore.pyqtSignal(str)
    def __init__(self,source=0):
        super().__init__()
        self._running = False
        self._paused = False
        self.source = source
        self.cap = None
        self.detector = SentimentDetector()

    def deal(self, source):
        self.source = source

    def run(self):
        self._running = True
        if self.source == "":
            self.source=int(0)
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
            sentiment_dict,rgb = self.detector.detect(rgb)
            if (now_time - pre_time).total_seconds() >= 2:
                self.log_signal.emit(now_time.strftime("%Y-%m-%d %H:%M:%S"))
                for sentiment, number in sentiment_dict.items():
                    self.log_signal.emit(f"Detected {sentiment}: {number} 人")
                self.log_signal.emit("")
                self.result_signal.emit(sentiment_dict)            # turn0search0
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