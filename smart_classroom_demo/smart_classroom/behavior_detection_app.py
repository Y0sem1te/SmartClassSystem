import os
import cv2
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget
from ui.behavior_detection import Ui_BehaviorDetection
from ui.behavior_detection_item import RecordWidget
import torch
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
        
    # def add_record(self, description: str, pixmaps: list,bboxes: list, frames: list):
    #     record = RecordWidget(description, pixmaps, bboxes,frames,self.photoContainer)
    #     self.photoLayout.addWidget(record)
    #     sb = self.photoScroll.verticalScrollBar()
    #     sb.setValue(sb.maximum())
    
    def numpy_to_pixmap(self, frame_np):
        """把 OpenCV 的 NumPy BGR 图像转换成 QPixmap"""
        # rgb = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
        rgb = frame_np
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    # def photoAppend(self, photo, locations, text):
    #     imgs = []
    #     for pta in locations:
    #         imgs.append(pta)
    #     pm_list = [self.numpy_to_pixmap(img_np) for img_np in imgs]
    #     self.add_record(text, pm_list)
    def photoAppend(self, full_frame, crops, bboxes, label):
        """
        full_frame: np.ndarray 原始 BGR 帧
        crops: list[np.ndarray] 行为裁剪图像列表
        bboxes: list[tuple] 对应框坐标列表
        label: str 行为标签
        """
        pm_list = [self.numpy_to_pixmap(c) for c in crops]
        # 创建 RecordWidget，并传入 full_frame
        record = RecordWidget(label, pm_list, bboxes, full_frame, self.photoContainer)
        record.thumbnailClicked.connect(self.show_popup)
        self.photoLayout.addWidget(record)
        sb = self.photoScroll.verticalScrollBar()
        sb.setValue(sb.maximum())
    
    def show_popup(self, full_frame, bbox):
        """
        点击快照后弹窗显示原始帧并绘制高亮 bbox
        """
        x1, y1, x2, y2 = bbox
        # 在原始 BGR 帧上画框
        frame_copy = full_frame.copy()
        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

        rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)

        dlg = QDialog(self)
        dlg.setWindowTitle("行为截图查看")
        layout = QVBoxLayout(dlg)
        lbl = QLabel(dlg)
        lbl.setPixmap(pix.scaled(800, 600, QtCore.Qt.KeepAspectRatio))
        layout.addWidget(lbl)
        dlg.exec_()

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

    # def update_image(self, qt_img):
    #     pixmap = qt_img
    #     pixmap = pixmap.scaled(self.videoContainer.size(), QtCore.Qt.KeepAspectRatio)
    #     self.videoContainer.setPixmap(pixmap)
    def update_image(self, qt_img):
        pixmap = qt_img.scaled(self.videoContainer.size(), QtCore.Qt.KeepAspectRatio)
        self.videoContainer.setPixmap(pixmap)

    def open(self):
        pass

