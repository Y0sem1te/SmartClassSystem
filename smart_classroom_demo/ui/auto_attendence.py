from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit, QWidget

class Ui_AutoAttendence(object):
    def setup(self, AutoAttendence):
        AutoAttendence.setObjectName("AutoAttendence")
        AutoAttendence.resize(1252, 735)
        self.tot_verlay = QtWidgets.QVBoxLayout(AutoAttendence)
        self.tot_verlay.setContentsMargins(0, 0, 0, 0)

        # 智慧考勤标签
        self.labelTitle = QtWidgets.QLabel("智慧课堂“亿”点通-注册考勤", AutoAttendence)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setFixedHeight(40)
        self.tot_verlay.addWidget(self.labelTitle, 1)

        self.main_horlay = QtWidgets.QHBoxLayout()

        # 左边的视频
        self.videoContainer = QtWidgets.QLabel(AutoAttendence)
        self.videoContainer.setStyleSheet("background-color: black;")
        self.videoContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.videoContainer.setMinimumSize(QtCore.QSize(640, 480))
        self.videoContainer.setScaledContents(True)

        self.main_horlay.addWidget(self.videoContainer, 1)

        # 右边按钮+已签到
        self.btn_assign_verlay = QtWidgets.QVBoxLayout()

        # 按钮
        self.playbtn_horlay = QtWidgets.QHBoxLayout()
        self.btnReg = QtWidgets.QPushButton("注册", AutoAttendence)
        self.playbtn_horlay.addWidget(self.btnReg)
        self.btnBegin = QtWidgets.QPushButton("开始考勤", AutoAttendence)
        self.playbtn_horlay.addWidget(self.btnBegin)
        self.btnStop = QtWidgets.QPushButton("停止考勤", AutoAttendence)
        self.playbtn_horlay.addWidget(self.btnStop)
        self.btn_assign_verlay.addLayout(self.playbtn_horlay)

        # 已经签到框
        label1 = QtWidgets.QLabel("已签到名单")
        label1.setFont(QtGui.QFont("Arial", 12))
        label1.setStyleSheet("color: white;")
        self.btn_assign_verlay.addWidget(label1)
        self.present_frame = QtWidgets.QFrame(AutoAttendence)
        self.present_frame.setStyleSheet("background-color: #2E2E2E;")
        self.present_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btn_assign_verlay.addWidget(self.present_frame)
        layout = QtWidgets.QVBoxLayout(self.present_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        self.logEdit = QTextEdit(self.present_frame)
        self.logEdit.setReadOnly(True)
        layout.addWidget(self.logEdit)

        self.main_horlay.addLayout(self.btn_assign_verlay, 1)
        self.tot_verlay.addLayout(self.main_horlay, 5)

        self.des_text_horlay = QtWidgets.QHBoxLayout()
        label2 = QtWidgets.QLabel("人脸数据库")
        label2.setFont(QtGui.QFont("Arial", 12))
        label2.setStyleSheet("color: white;")
        self.des_text_horlay.addWidget(label2)
        label3 = QtWidgets.QLabel("未签到名单")
        label3.setFont(QtGui.QFont("Arial", 12))
        label3.setStyleSheet("color: white;")
        self.des_text_horlay.addWidget(label3)
        self.tot_verlay.addLayout(self.des_text_horlay)

        #人脸数据库和还未签到
        self.db_absent_horlay = QtWidgets.QHBoxLayout()
        
        # 数据库
        self.db_frame = QtWidgets.QFrame(AutoAttendence)
        self.db_frame.setStyleSheet("background-color: #2E2E2E;")
        self.db_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.db_absent_horlay.addWidget(self.db_frame)
        layout = QtWidgets.QVBoxLayout(self.db_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        self.logEdit2 = QTextEdit(self.db_frame)
        self.logEdit2.setReadOnly(True)
        layout.addWidget(self.logEdit2)
        

        # 未签到
        self.absent_frame = QtWidgets.QFrame(AutoAttendence)
        self.absent_frame.setStyleSheet("background-color: #2E2E2E;")
        self.absent_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.db_absent_horlay.addWidget(self.absent_frame)
        layout = QtWidgets.QVBoxLayout(self.absent_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        self.logEdit3 = QTextEdit(self.absent_frame)
        self.logEdit3.setReadOnly(True)
        layout.addWidget(self.logEdit3)

        self.tot_verlay.addLayout(self.db_absent_horlay, 5)

        # 底部
        self.bottom_horlay = QtWidgets.QHBoxLayout()

        # 删除记录
        self.xh_btn_horlay = QtWidgets.QHBoxLayout()
        self.xhinput = QtWidgets.QLineEdit(AutoAttendence)
        self.xhinput.setPlaceholderText("请输入学号")
        self.xh_btn_horlay.addWidget(self.xhinput)
        self.btnDelete = QtWidgets.QPushButton("删除记录", AutoAttendence)
        self.xh_btn_horlay.addWidget(self.btnDelete)
        self.bottom_horlay.addLayout(self.xh_btn_horlay)

        # 教师代签
        self.xh_btn_horlay2 = QtWidgets.QHBoxLayout()
        self.xhinput2 = QtWidgets.QLineEdit(AutoAttendence)
        self.xhinput2.setPlaceholderText("请输入学号")
        self.xh_btn_horlay2.addWidget(self.xhinput2)
        self.btnTeacher = QtWidgets.QPushButton("教师代签", AutoAttendence)
        self.xh_btn_horlay2.addWidget(self.btnTeacher)
        self.bottom_horlay.addLayout(self.xh_btn_horlay2)
        self.tot_verlay.addLayout(self.bottom_horlay, 1)