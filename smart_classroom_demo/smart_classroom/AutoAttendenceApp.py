import csv
import cv2
import matplotlib.pyplot as plt
from ui.auto_attendence import Ui_AutoAttendence
import torch
from utils.AttendenceThread import AttendenceThread
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QInputDialog, QMessageBox
from datetime import datetime
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# model weights
device = "cuda" if torch.cuda.is_available() else "cpu"

class AutoAttendenceApp(QWidget, Ui_AutoAttendence):
    def __init__(self, parent=None):
        super(AutoAttendenceApp, self).__init__(parent)
        self.setup(self)
        self.setWindowTitle("智慧课堂“亿”点通-注册考勤")

        from models.auto_attendence_detector import AttendenceDetector
        from utils.AttendenceThread import AttendenceThread
        import threading

        self.attendance_file = 'resource/attendance.csv'
        self.lock            = threading.Lock()

        self.detector = AttendenceDetector()
        self.thread   = None

        self.present = set()
        self.absent  = set(self.detector.known_ids)

        self.btnReg.clicked.connect(self.handle_register)
        self.btnBegin.clicked.connect(self.start_attendance)
        self.btnStop.clicked.connect(self.stop_attendance)
        self.btnDelete.clicked.connect(self.delete_record)
        self.btnTeacher.clicked.connect(self.teacher_sign)

        self.refresh_db_and_absent()
        self.refresh_present()
        

    def open(self):
        pass
    # ——— 新增：注册功能 ———
    def handle_register(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qimg = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.videoContainer.setPixmap(QtGui.QPixmap.fromImage(qimg))
        cap.release()
        if not ret:
            QMessageBox.warning(self, "错误", "无法获取摄像头画面，请检查设备。")
            return
        sid, ok1 = QInputDialog.getText(self, "注册", "请输入学号：")
        if not ok1 or not sid:
            return
        name, ok2 = QInputDialog.getText(self, "注册", "请输入姓名：")
        if not ok2 or not name:
            return
        success, msg = self.detector.register(frame, sid, name)
        QMessageBox.information(self, "注册", msg)
        if success:
            self.absent.add(sid)
            self.refresh_db_and_absent()

    def start_attendance(self):
        if self.thread and self.thread.isRunning():
            return
        # 重置状态
        self.present.clear()
        self.absent = set(self.detector.known_ids)
        self.logEdit.clear()
        self.refresh_db_and_absent()
        self.refresh_present()
        # 启动线程
        self.thread = AttendenceThread(self.detector)
        self.thread.frame_signal.connect(self.update_video)
        self.thread.signin_signal.connect(self.mark_present)
        self.thread.start()

    def stop_attendance(self):
        if self.thread:
            self.thread.stop()
            self.thread = None

    def delete_record(self):
        sid = self.xhinput.text().strip()
        if sid in self.present:
            self.present.remove(sid)
            self.absent.add(sid)
            self._remove_csv_entry(sid)
            self.refresh_present()
            self.refresh_db_and_absent()
            QMessageBox.information(self, "删除", f"已删除{sid}的签到记录。")
        else:
            QMessageBox.warning(self, "提示", "该学号未签到或不存在。")

    def teacher_sign(self):
        sid = self.xhinput2.text().strip()
        if sid in self.absent:
            self.present.add(sid)
            self.absent.remove(sid)
            self._write_csv(sid)
            self.refresh_present()
            self.refresh_db_and_absent()
            QMessageBox.information(self, "代签", f"教师已代签{sid}。")
        else:
            QMessageBox.warning(self, "提示", "该学号已签到或不存在。")

    def update_video(self, rgb_img):
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        qimg = QtGui.QImage(rgb_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.videoContainer.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def mark_present(self, ids):
        updated = False
        for sid in ids:
            if sid in self.absent:
                self.present.add(sid)
                self.absent.remove(sid)
                self._write_csv(sid)
                updated = True
        if updated:
            self.refresh_present()
            self.refresh_db_and_absent()

    def refresh_db_and_absent(self):
        # 人脸数据库
        db_txt = "".join(f"{sid}: {self.detector.known_names[i]}\n"
                         for i, sid in enumerate(self.detector.known_ids))
        self.logEdit2.setPlainText(db_txt)
        # 未签到名单
        abs_txt = "".join(f"{sid}: {self.detector.known_names[self.detector.known_ids.index(sid)]}\n"
                          for sid in sorted(self.absent))
        self.logEdit3.setPlainText(abs_txt)

    def refresh_present(self):
        pres_txt = "".join(f"{sid}: {self.detector.known_names[self.detector.known_ids.index(sid)]}\n"
                           for sid in sorted(self.present))
        self.logEdit.setPlainText(pres_txt)

    def _write_csv(self, sid):
        with self.lock:
            with open(self.attendance_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([sid, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    def _remove_csv_entry(self, sid):
        with self.lock:
            rows = []
            with open(self.attendance_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = [r for r in reader if r[0] != sid]
            with open(self.attendance_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)

