from PyQt5 import QtWidgets, QtCore
from .clickable_label import ClickableLabel
from PyQt5.QtCore import pyqtSignal, Qt
import numpy as np

class RecordWidget(QtWidgets.QWidget):
    # thumbnailClicked = pyqtSignal(tuple)  # (x1,y1,x2,y2)
    # full_frame: numpy.ndarray, bbox: (x1,y1,x2,y2)
    thumbnailClicked = pyqtSignal(object, tuple)
    def __init__(self, text: str, pixmaps: list,bboxes: list, frames :list,parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(2,2,2,2)
        # self.bboxes = bboxes
        self.bboxes = bboxes
        # frames 参数改为 full_frame（numpy）
        self.full_frame = frames
        # 文字
        lbl = QtWidgets.QLabel(text, self)
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        #图片行
        row = QtWidgets.QHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignLeft)
        # for pm, bbox,frame in zip(pixmaps, bboxes,frames):
        for pm, bbox in zip(pixmaps, bboxes):
            img_lbl = ClickableLabel(self)
            img_lbl.setPixmap(pm)
            img_lbl.setScaledContents(True)
            img_lbl.setFixedSize(100, 100)
            img_lbl._bbox = bbox
            # 将子标签的点击信号转发为 RecordWidget 的 thumbnailClicked
            # img_lbl.clicked.connect(
            #     lambda _, bb=bbox, op=frame: 
            #         self.thumbnailClicked.emit(op, bb)
            # )
            # 点击时传出 full_frame + bbox
            img_lbl.clicked.connect(
                lambda _, bb=bbox: 
                    self.thumbnailClicked.emit(self.full_frame, bb)
            )
            row.addWidget(img_lbl)
        layout.addLayout(row)
