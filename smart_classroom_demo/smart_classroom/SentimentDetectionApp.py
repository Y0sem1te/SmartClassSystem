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
from ui.sentiment_analysis import Ui_SentimentDetection as Ui_SentimentAnalysis
from utils.common import second2str, OffsetList
import torch
from PyQt5 import QtGui
from utils.VideoThread import VideoThread
from models.behavior_detectot import BehaviorDectector
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# model weights
device = "cuda" if torch.cuda.is_available() else "cpu"

class SentimentDetectionApp(QWidget, Ui_SentimentAnalysis):
    def __init__(self, parent=None):
        super(SentimentDetectionApp, self).__init__(parent)
        self.setup(self)
        self.setWindowTitle("智慧课堂“亿”点通-情绪检测")
        

    def open(self):
        pass

