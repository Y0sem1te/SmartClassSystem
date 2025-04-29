from PyQt5 import QtWidgets, QtCore

class RecordWidget(QtWidgets.QWidget):
    def __init__(self, text: str, pixmaps: list, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(2,2,2,2)

        # 文字
        lbl = QtWidgets.QLabel(text, self)
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        #图片行
        row = QtWidgets.QHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignLeft)
        for pm in pixmaps:
            img_lbl = QtWidgets.QLabel(self)
            img_lbl.setPixmap(pm)
            img_lbl.setScaledContents(True)
            img_lbl.setFixedSize(100, 100)
            row.addWidget(img_lbl)
        layout.addLayout(row)
