from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit, QWidget

class Ui_SentimentDetection(object):
    def setup(self, SentimentDetection):
        # 整体
        SentimentDetection.setObjectName("SentimentDetection")
        SentimentDetection.resize(1252, 735)
        self.tot_verlay = QtWidgets.QVBoxLayout(SentimentDetection)
        self.tot_verlay.setContentsMargins(0, 0, 0, 0)

        # 顶部
        self.topbar_verlay = QtWidgets.QVBoxLayout()
        # 1
        self.labelTitle = QtWidgets.QLabel("智慧课堂“亿”点通-情感分析", SentimentDetection)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setFixedHeight(40)
        self.topbar_verlay.addWidget(self.labelTitle)  #加到topbar

        # 2
        self.lineEditSource = QtWidgets.QLineEdit(SentimentDetection)
        self.lineEditSource.setPlaceholderText("如需分析视频，请传入视频源地址；如需实时监控，记得清空路径")
        self.topbar_verlay.addWidget(self.lineEditSource) #加到topbar

        # 3
        self.playbtn_horlay = QtWidgets.QHBoxLayout()
        self.btnPlay = QtWidgets.QPushButton("播放", SentimentDetection)
        self.playbtn_horlay.addWidget(self.btnPlay)
        self.btnPause = QtWidgets.QPushButton("暂停播放", SentimentDetection)
        self.playbtn_horlay.addWidget(self.btnPause)
        self.btnStop = QtWidgets.QPushButton("恢复播放", SentimentDetection)
        self.playbtn_horlay.addWidget(self.btnStop)
        self.topbar_verlay.addLayout(self.playbtn_horlay)
        self.tot_verlay.addLayout(self.topbar_verlay)  # 顶部加到整体

        #主体
        self.main_horlay = QtWidgets.QHBoxLayout()
        
        # 1 视频
        self.videoContainer = QtWidgets.QLabel(SentimentDetection)
        self.videoContainer.setStyleSheet("background-color: black;")
        self.videoContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoContainer.setMinimumSize(QtCore.QSize(640, 480))
        self.videoContainer.setScaledContents(True)
        self.main_horlay.addWidget(self.videoContainer, 5)

        # 2 结果
        self.res_verlay = QtWidgets.QVBoxLayout()

        # 2.1 文本结果
        self.res_frame = QtWidgets.QFrame(SentimentDetection)
        self.res_frame.setStyleSheet("background-color: #2E2E2E;")
        self.res_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.res_verlay.addWidget(self.res_frame, 3)
        layout = QtWidgets.QVBoxLayout(self.res_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        self.logEdit = QTextEdit(self.res_frame)
        self.logEdit.setReadOnly(True)
        layout.addWidget(self.logEdit)
        
        # 2.2 折线图
        self.line_frame = QtWidgets.QFrame(SentimentDetection)
        self.line_frame.setStyleSheet("background-color: #2E2E2E;")
        self.line_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.res_verlay.addWidget(self.line_frame, 3)
        self.line_frame.setLayout(QtWidgets.QVBoxLayout())
        self.line_plot = QtWidgets.QLabel(self.line_frame)
        self.line_plot.setMinimumSize(QtCore.QSize(750, 250))  # 设置最小尺寸
        self.line_plot.setScaledContents(False)
        self.line_plot.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.line_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.line_frame.layout().addWidget(self.line_plot)
        self.line_plot.setStyleSheet("background-color: #2E2E2E;")

        # 2.3 饼状图
        self.bing_frame = QtWidgets.QFrame(SentimentDetection)
        self.bing_frame.setStyleSheet("background-color: #2E2E2E;")
        self.bing_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.res_verlay.addWidget(self.bing_frame, 6)
        self.bing_frame.setLayout(QtWidgets.QVBoxLayout())
        self.bing_plot = QtWidgets.QLabel(self.bing_frame)
        self.bing_plot.setMinimumSize(QtCore.QSize(750, 350))  # 设置最小尺寸
        self.bing_plot.setStyleSheet("background-color: #2E2E2E;")

        # self.bing_plot.setScaledContents(True)
        # self.bing_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.bing_plot.setScaledContents(False)
        # 水平和垂直都可扩展
        self.bing_plot.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        # QLabel 内部内容居中
        self.bing_plot.setAlignment(QtCore.Qt.AlignCenter)

        self.main_horlay.addLayout(self.res_verlay, 5)
        self.tot_verlay.addLayout(self.main_horlay)
