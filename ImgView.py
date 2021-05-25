from PyQt5.QtWidgets import QScrollArea, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImgView(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

    def uploadImg(self, resize_ratio, filePath):

        self.pixmap = QPixmap(filePath)
        size = self.pixmap.size()
        self.img_label = QLabel()

        self.img_label.setPixmap(self.pixmap.scaled(int(size.width() * resize_ratio),
                                                    int(size.height() * resize_ratio), Qt.IgnoreAspectRatio))

        self.img_label.setStyleSheet(  # 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: red;"
            "border-radius: 3px")

        self.setWidget(self.img_label)