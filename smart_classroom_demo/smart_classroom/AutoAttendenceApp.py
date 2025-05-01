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
from ui.auto_attendence import Ui_AutoAttendence
from utils.common import second2str, OffsetList
import torch
from PyQt5 import QtGui
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# model weights
device = "cuda" if torch.cuda.is_available() else "cpu"

class AutoAttendenceApp(QWidget, Ui_AutoAttendence):
    def __init__(self, parent=None):
        super(AutoAttendenceApp, self).__init__(parent)
        self.setup(self)
        self.setWindowTitle("智慧课堂“亿”点通-情绪检测")
        

    def open(self):
        pass

