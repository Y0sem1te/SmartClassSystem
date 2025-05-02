import csv
from datetime import datetime
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
from utils.SentimentThread import SentimentThread

# model weights
device = "cuda" if torch.cuda.is_available() else "cpu"

class SentimentDetectionApp(QWidget, Ui_SentimentAnalysis):
    def __init__(self, parent=None):
        super(SentimentDetectionApp, self).__init__(parent)
        self.setup(self)
        self.setWindowTitle("智慧课堂“亿”点通-情绪检测")

        # 初始化数据结构用于存储情绪历史
        self.emotion_history = []
        self.time_history = []
        self.max_history_length = 20  # 最多保存20个历史点

        # ——— 初始化线程 ———
        self.thread = SentimentThread(source=0)
        # 视频帧更新
        self.thread.change_pixmap.connect(self.update_video_frame)    # turn0search5
        # 日志与饼图信号
        self.thread.log_signal.connect(self.append_log)              # 自定义信号
        self.thread.result_signal.connect(self.update_charts)     # 自定义信号

        # 绑定按钮
        self.btnPlay.clicked.connect(self.thread.start)              # 启动线程 :contentReference[oaicite:0]{index=0}
        self.btnPause.clicked.connect(self.thread.pause)             # 暂停处理 :contentReference[oaicite:1]{index=1}
        self.btnStop.clicked.connect(self.thread.resume)             # 恢复处理 :contentReference[oaicite:2]{index=2}

    def update_video_frame(self, pixmap: QPixmap):
        """将线程中发过来的视频帧显示在 QLabel 上"""  
        self.videoContainer.setPixmap(pixmap)                      # 使用 QLabel.setPixmap :contentReference[oaicite:3]{index=3}

    def append_log(self, text: str):
        """追加日志到 QTextEdit"""
        self.logEdit.append(text)

    def update_charts(self, data: dict):
        """更新所有图表：饼图和折线图"""
        self.update_pie_chart(data)
        self.update_line_chart(data)

    def update_pie_chart(self, data: dict):
        if not data:
            self.bing_plot.clear()
            return

        # 获取标签尺寸
        w_label = self.bing_plot.width()
        h_label = self.bing_plot.height()
        
        # 创建更大的图形
        fig, ax = plt.subplots(figsize=(10, 10), dpi=100)  # 增大尺寸
        
        # 设置黑色背景
        fig.patch.set_facecolor('#2E2E2E')
        ax.set_facecolor('#2E2E2E')
        
        # 调整边距，给饼图更多空间
        fig.subplots_adjust(left=0.1, right=0.7, top=0.95, bottom=0.1)
        
        # 绘制饼图
        labels = list(data.keys())
        sizes = list(data.values())
        explode = [0.05] * len(labels)
        
        # 创建颜色列表，使用鲜艳的色彩在黑色背景上更明显
        colors = plt.cm.tab10(np.linspace(0, 1, len(labels)))
        
        wedges, _, autotexts = ax.pie(
            sizes,
            labels=None,  # 不在饼图旁显示标签
            explode=explode,
            autopct='%1.1f%%',
            pctdistance=0.75,
            shadow=True,
            startangle=90,
            radius=0.8,  # 稍微减小半径确保完全显示
            colors=colors,
            textprops={'color': 'white', 'fontsize': 16}  # 统一设置文本属性
        )
        
        # 确保饼图是圆形的
        # ax.axis('equal')
        
        # 增强百分比文本可见性
        for txt in autotexts:
            txt.set_fontsize(16)
            txt.set_fontweight('bold')
            txt.set_color('white')
        
        # 添加图例到右侧(白色文字)
        legend = ax.legend(
            wedges, 
            labels,
            title="情绪类型",
            loc="center right",
            bbox_to_anchor=(1.4, 0.5),  # 放在更靠右的位置
            fontsize=20,
            frameon=True,  # 显示图例边框
            facecolor='#2E2E2E',  # 图例背景色
            edgecolor='white'   # 图例边框色
        )
        
        # 设置图例标题和文本为白色
        legend.get_title().set_color('white')
        for text in legend.get_texts():
            text.set_color('white')
        
        # 渲染图形
        fig.canvas.draw()
        
        # 转换为QPixmap
        buf = fig.canvas.tostring_rgb()
        w, h = fig.canvas.get_width_height()
        qimg = QImage(buf, w, h, w * 3, QImage.Format_RGB888)
        
        # 创建像素图并使用更大的固定尺寸
        pixmap = QPixmap.fromImage(qimg)
        
        # 使用固定的大尺寸，不受限于容器当前大小
        fixed_size = max(w_label, h_label, 350)  # 最小为600像素
        pixmap = pixmap.scaled(
            fixed_size, fixed_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        
        # 显示图像，确保居中
        self.bing_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.bing_plot.setPixmap(pixmap)
        
        # 关闭matplotlib图形以释放内存
        plt.close(fig)

    def update_line_chart(self, data: dict):
        """更新情绪变化折线图"""
        if not data:
            return
        
        # 找出当前数量最多的情绪
        max_emotion = max(data, key=data.get)
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # 更新历史数据
        self.emotion_history.append(max_emotion)
        self.time_history.append(current_time)
        
        # 限制历史数据长度
        if len(self.emotion_history) > self.max_history_length:
            self.emotion_history.pop(0)
            self.time_history.pop(0)
        
        # 创建折线图 - 增加宽度
        fig, ax = plt.subplots(figsize=(12, 4), dpi=100)  # 宽度从8改为12
        
        # 设置黑色背景
        fig.patch.set_facecolor('#2E2E2E')
        ax.set_facecolor('#2E2E2E')
        
        # 设置网格和边框颜色
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        for spine in ax.spines.values():
            spine.set_color('white')
        
        # 使用分类坐标轴，因为情绪是分类变量
        unique_emotions = list(set(self.emotion_history))
        emotion_indices = [unique_emotions.index(e) for e in self.emotion_history]
        
        # 绘制折线 - 增加线条粗细和标记点大小
        line = ax.plot(range(len(self.emotion_history)), emotion_indices, 'o-', 
                    color='#1E90FF', linewidth=3, markersize=10)
        
        # 设置坐标轴标签和颜色 - 增大字体
        ax.set_yticks(range(len(unique_emotions)))
        ax.set_yticklabels(unique_emotions, fontsize=14)  # 增大Y轴标签字体
        ax.set_xticks(range(len(self.time_history)))
        ax.set_xticklabels(self.time_history, rotation=45, fontsize=12)  # 增大X轴标签字体
        
        ax.tick_params(axis='x', colors='white', labelsize=12)  # 增大刻度标签
        ax.tick_params(axis='y', colors='white', labelsize=14)  # 增大刻度标签
        
        # 设置标题和轴标签 - 增大字体
        ax.set_title('主要情绪变化趋势', color='white', fontsize=18)  # 增大标题字体
        ax.set_xlabel('时间', color='white', fontsize=14)  # 增大X轴标题字体
        ax.set_ylabel('情绪类型', color='white', fontsize=14)  # 增大Y轴标题字体
        
        # 调整布局 - 给下方X轴留出更多空间
        fig.tight_layout(pad=2.0)  # 增加内边距
        fig.subplots_adjust(bottom=0.2)  # 为底部X轴标签留出更多空间
        
        # 渲染图形
        fig.canvas.draw()
        
        # 转换为QPixmap
        buf = fig.canvas.tostring_rgb()
        w, h = fig.canvas.get_width_height()
        qimg = QImage(buf, w, h, w * 3, QImage.Format_RGB888)
        
        # 创建像素图，使用宽屏比例
        pixmap = QPixmap.fromImage(qimg)
        
        # 调整大小并保持原比例 - 不再限制在控件大小内
        w_label = self.line_plot.width()
        h_label = self.line_plot.height()
        pixmap = pixmap.scaled(
            max(w_label, 800),  # 确保至少800像素宽
            h_label,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        
        # 显示图像
        self.line_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.line_plot.setPixmap(pixmap)
        
        # 关闭matplotlib图形以释放内存
        plt.close(fig)

    def open(self):
        pass