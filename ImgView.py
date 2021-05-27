from PyQt5.QtWidgets import QScrollArea, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QEvent, QPoint

class ImgView(QScrollArea):
    def __init__(self):
        super().__init__()

        self.last_time_move_x = 0
        self.last_time_move_y = 0

        self.setWidgetResizable(True)
        self.scrollbarY = self.verticalScrollBar()
        self.scrollbarX = self.horizontalScrollBar()


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
        self.installEventFilter(self)

    def eventFilter(self, source, event):

        if event.type() == event.MouseMove:
            #self.img_label.setCursor(QCursor(Qt.SizeAllCursor))

            if self.last_time_move_x == 0:
                self.last_time_move_x = event.pos().x()

            if self.last_time_move_y == 0:
                self.last_time_move_y = event.pos().y()

            distance_x = self.last_time_move_x - event.pos().x()
            distance_y = self.last_time_move_y - event.pos().y()

            #print(self.last_time_move_x, event.pos().x(), distance_x, self.scrollbarX.value())
            #print(self.last_time_move_y, event.pos().y(), distance_y, self.scrollbarY.value())

            self.scrollbarX.setValue(self.scrollbarX.value() + distance_x)
            self.scrollbarY.setValue(self.scrollbarY.value() + distance_y)

            #print(self.scrollbarX.value())
            #print(self.scrollbarY.value())


        elif event.type() == event.MouseButtonRelease:

            self.last_time_move_x = self.last_time_move_y = 0
            #self.img_label.setCursor(QCursor(Qt.PointingHandCursor))

        return QWidget.eventFilter(self, source, event)

    def wheelEvent(self, wheel_event):

        if wheel_event.modifiers() == Qt.ControlModifier:
            delta = wheel_event.angleDelta().y()
            if delta > 0:
                self.zoom_in()

            elif delta < 0:
                self.zoom_out()

        else:
            return super().wheelEvent(wheel_event)

    def zoom_in(self):
        self.img_label.setPixmap(self.pixmap.scaled(int(self.img_label.size().width * 0.8),
                                                    int(elf.img_label.size().height() * 0.8), Qt.IgnoreAspectRatio))
    def zoom_out(self):
        self.img_label.setPixmap(self.pixmap.scaled(int(self.img_label.size().width * 1.2),
                                                    int(elf.img_label.size().height() * 1.2), Qt.IgnoreAspectRatio))
