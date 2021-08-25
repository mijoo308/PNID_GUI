from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImgListView(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.resize(self.frameGeometry().width(), self.frameGeometry().height())

        # empty widget for scrollArea
        self.emptyWidget = QWidget()
        self.setWidget(self.emptyWidget)

        self.box_layout = QVBoxLayout()
        self.setLayout(self.box_layout)
        self.setStyleSheet(  # 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: red;"
            "border-radius: 3px")

        # for scroll test
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()

        self.emptyWidget.setLayout(self.box_layout)

    def makeImgListElement(self):
        pixmap = QPixmap('test.jpg')  # test
        pixmap = pixmap.scaled(270, 150)
        img_label = QLabel()
        img_label.setPixmap(pixmap)
        img_name_label = QLabel("Test")
        img_name_label.setAlignment(Qt.AlignCenter)

        # layout에 추가
        self.box_layout.addWidget(img_label)
        self.box_layout.addWidget(img_name_label)

        # self.box_layout.addStretch()