import csv
import os
import time
from itertools import islice
from threading import Thread, Lock
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget
from matplotlib import ticker
from pipeline_module.classroom_action_module import CheatingActionModule
from pipeline_module.core.task_solution import TaskSolution
from pipeline_module.pose_modules import AlphaPoseModule
from pipeline_module.video_modules import VideoModule
from pipeline_module.vis_modules import CheatingDetectionVisModule
from pipeline_module.yolo_modules import YoloV5Module
from smart_classroom.list_items import VideoSourceItem, RealTimeCatchItem, FrameData
from ui.behavior_detection import Ui_BehaviorDetection
from ui.behavior_detection_item import RecordWidget
from ui.cheating_detection import Ui_CheatingDetection
from utils.common import second2str, OffsetList
import torch
from PyQt5 import QtGui
from utils.VideoThread import VideoThread
from models.behavior_detectot import BehaviorDectector
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# model weights
device = "cuda" if torch.cuda.is_available() else "cpu"

class BehaviorDetectionApp(QWidget, Ui_BehaviorDetection):
    def __init__(self, parent=None):
        super(BehaviorDetectionApp, self).__init__(parent)
        self.setup(self)
        self.setWindowTitle("智慧课堂“亿”点通-行为检测")
        self.timer = QtCore.QTimer()
        self.vd_thread = VideoThread(BehaviorDectector())
        self.vd_thread.log_signal.connect(self.log_append)
        self.vd_thread.change_pixmap.connect(self.update_image)
        self.vd_thread.photo_signal.connect(self.photoAppend)
        self.btnPlay.clicked.connect(self.button_play_clicked)
        self.btnPause.clicked.connect(self.button_pause_clicked)
        self.btnStop.clicked.connect(self.button_con_clicked)
        
    def add_record(self, description: str, pixmaps: list):
        record = RecordWidget(description, pixmaps, self.photoContainer)
        self.photoLayout.addWidget(record)
        sb = self.photoScroll.verticalScrollBar()
        sb.setValue(sb.maximum())
    
    def numpy_to_pixmap(self, frame_np):
        """把 OpenCV 的 NumPy BGR 图像转换成 QPixmap"""
        # rgb = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
        rgb = frame_np
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def photoAppend(self, photo, locations, text):
        imgs = []
        for pta in locations:
            imgs.append(pta)
        pm_list = [self.numpy_to_pixmap(img_np) for img_np in imgs]
        self.add_record(text, pm_list)

    def log_append(self, text):
        self.logEdit.append(text)

    def button_pause_clicked(self):
        if self.vd_thread:
            self.vd_thread.pause()
    
    def button_con_clicked(self):
        if self.vd_thread:
            self.vd_thread.resume()

    def button_play_clicked(self):
        if hasattr(self, 'vd_thread') and self.vd_thread.isRunning():
            self.vd_thread.stop()
        text = self.lineEditSource.text() or 0
        if text != 0:
            if not os.path.exists(text):
                self.lineEditSource.setText("视频源不存在，请检查路径")
                return
            cap = cv2.VideoCapture(text)
            if not cap.isOpened():
                self.lineEditSource.setText("视频文件格式错误")
                cap.release()
                return
            cap.release()
        self.vd_thread.text = text

        if self.vd_thread and self.vd_thread.isRunning():
            self.vd_thread.stop()

        self.vd_thread = VideoThread(BehaviorDectector(),source=text)
        self.vd_thread.photo_signal.connect(self.photoAppend)
        self.vd_thread.log_signal.connect(self.log_append)
        self.vd_thread.change_pixmap.connect(self.update_image)
        self.vd_thread.start()
        pass

    def update_image(self, qt_img):
        pixmap = qt_img
        pixmap = pixmap.scaled(self.videoContainer.size(), QtCore.Qt.KeepAspectRatio)
        self.videoContainer.setPixmap(pixmap)

    def open(self):
        pass

