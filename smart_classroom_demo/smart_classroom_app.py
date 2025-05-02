import sys

import qdarkstyle
from smart_classroom import AutoAttendenceApp, SentimentDetectionApp
from smart_classroom.AutoAttendenceApp import AutoAttendenceApp
from smart_classroom.behavior_detection_app import BehaviorDetectionApp
from smart_classroom.class_concentration_app import ClassConcentrationApp
from smart_classroom.SentimentDetectionApp import SentimentDetectionApp

try:
    import smart_classroom_rc
except ImportError:
    pass
import torch
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

from ui.smart_classroom import Ui_MainWindow as SmartClassroomMainWindow

torch._C._jit_set_profiling_mode(False)
torch.jit.optimized_execution(False)


class SmartClassroomApp(QMainWindow, SmartClassroomMainWindow):

    def __init__(self, parent=None):
        super(SmartClassroomApp, self).__init__(parent)
        self.setupUi(self)

        self.behavior_detection_widget = BehaviorDetectionApp()
        self.behavior_detection_widget.setObjectName("behavior_detection_widget")
        self.tabWidget.addTab(self.behavior_detection_widget, "课堂行为分析")

        self.class_concentration_widget = ClassConcentrationApp()
        self.class_concentration_widget.setObjectName("class_concentration_widget")
        self.tabWidget.addTab(self.class_concentration_widget, "课堂专注度分析")

        self.sentiment_detection_widget = SentimentDetectionApp()
        self.sentiment_detection_widget.setObjectName("sentiment_detection_widget")
        self.tabWidget.addTab(self.sentiment_detection_widget, "情感分析")

        self.registe_attendence_widget = AutoAttendenceApp()
        self.registe_attendence_widget.setObjectName("registe_attendence_widget")
        self.tabWidget.addTab(self.registe_attendence_widget, "注册考勤")

        self.current_tab_widget = self.tabWidget.currentWidget()

        def current_tab_change(idx, self=self):
            if self.current_tab_widget is not None:
                self.current_tab_widget.close()
            self.current_tab_widget = self.tabWidget.widget(idx)
            self.current_tab_widget.open()

        self.tabWidget.currentChanged.connect(current_tab_change)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.cheating_detection_widget.close()
        self.face_register_widget.close()
        self.dynamic_attendance_widget.close()
        self.class_concentration_widget.close()
        super(SmartClassroomApp, self).closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # from QcureUi import cure
    #
    # window = cure.Windows(SmartClassroomApp(), 'trayname', True, title='智慧教室')
    window = SmartClassroomApp()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # run
    window.show()
    sys.exit(app.exec_())
