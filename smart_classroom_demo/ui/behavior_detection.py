from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QTextEdit, QWidget

class Ui_BehaviorDetection(object):
    def setup(self, BehaviorDetection):
        BehaviorDetection.setObjectName("BehaviorDetection")
        BehaviorDetection.resize(1252, 735)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(BehaviorDetection)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)

        # 顶部标题栏
        self.topBar = QtWidgets.QHBoxLayout()
        self.labelTitle = QtWidgets.QLabel("智慧课堂“亿”点通-行为检测", BehaviorDetection)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.topBar.addWidget(self.labelTitle)
        self.verticalLayout_13.addLayout(self.topBar)
        self.labelTitle.setFixedHeight(40)
        self.topBar.addWidget(self.labelTitle)
        sourceLayout = QtWidgets.QHBoxLayout()
        self.lineEditSource = QtWidgets.QLineEdit(BehaviorDetection)
        self.lineEditSource.setPlaceholderText("如需分析视频，请传入视频源地址；如需实时监控，记得清空路径")
        sourceLayout.addWidget(self.lineEditSource)
        self.verticalLayout_13.addLayout(sourceLayout)
        self.verticalLayout_13.addLayout(self.topBar)

        # 中间区域：视频在左，结果在右（等分）
        self.middleLayout = QtWidgets.QHBoxLayout()

        # 1. 视频播放区域，左侧，占比1
        self.videoContainer = QtWidgets.QLabel(BehaviorDetection)
        self.videoContainer.setStyleSheet("background-color: black;")
        self.videoContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoContainer.setMinimumSize(QtCore.QSize(640, 480))
        self.middleLayout.addWidget(self.videoContainer, 5)
        self.videoContainer.setScaledContents(True)


        # 2. 结果显示区域，右侧，占比1
        self.resultFrame = QtWidgets.QFrame(BehaviorDetection)
        self.resultFrame.setMinimumSize(QtCore.QSize(200, 480))
        self.resultFrame.setStyleSheet("background-color: #2E2E2E;")
        self.resultFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.middleLayout.addWidget(self.resultFrame, 3)
        # 添加记录
        layout = QtWidgets.QVBoxLayout(self.resultFrame)
        layout.setContentsMargins(5, 5, 5, 5)
        self.logEdit = QTextEdit(self.resultFrame)
        self.logEdit.setReadOnly(True)
        layout.addWidget(self.logEdit)


        # 把中间布局加入主布局
        self.verticalLayout_13.addLayout(self.middleLayout)

        # 控制按钮栏
        self.controlBar = QtWidgets.QHBoxLayout()
        self.btnPlay = QtWidgets.QPushButton("播放", BehaviorDetection)
        self.btnPause = QtWidgets.QPushButton("暂停播放", BehaviorDetection)
        self.btnStop = QtWidgets.QPushButton("恢复播放", BehaviorDetection)
        self.controlBar.addWidget(self.btnPlay)
        self.controlBar.addWidget(self.btnPause)
        self.controlBar.addWidget(self.btnStop)
        self.verticalLayout_13.addLayout(self.controlBar)

        # 捕获照片显示区域
        # self.photoFrame = QtWidgets.QLabel(BehaviorDetection)
        # self.photoFrame.setMinimumSize(QtCore.QSize(320, 240))
        # self.photoFrame.setMaximumHeight(200)
        # self.photoFrame.setStyleSheet("background-color: #404040;")
        # self.photoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.verticalLayout_13.addWidget(self.photoFrame, 1)
        self.photoScroll = QScrollArea(BehaviorDetection)
        self.photoScroll.setWidgetResizable(True)
        self.photoScroll.setMinimumHeight(300)
        self.photoContainer = QWidget()
        self.photoLayout = QtWidgets.QVBoxLayout(self.photoContainer)
        self.photoLayout.setContentsMargins(5, 5, 5, 5)
        self.photoScroll.setWidget(self.photoContainer)
        self.verticalLayout_13.addWidget(self.photoScroll, 2)


    def open(self):
        super(Ui_BehaviorDetection, self).open()
        pass
