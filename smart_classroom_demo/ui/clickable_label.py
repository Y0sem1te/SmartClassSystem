from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel

class ClickableLabel(QLabel):
    clicked = pyqtSignal(tuple)  # 例如 (x1, y1, x2, y2)

    def mousePressEvent(self, event):
        # 在此之前，需要在实例化时为 self._bbox 赋值
        if hasattr(self, '_bbox'):
            self.clicked.emit(self._bbox)          # 发出信号并传递坐标
        super().mousePressEvent(event)