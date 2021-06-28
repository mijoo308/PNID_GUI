import sys

from MainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel

class graphicsView(QGraphicsView):
    def __init__(self, imgPath):
        super().__init__()

        self.scene = GraphicsScene()
        self.scene.set_image(img_path=imgPath)
        self.setScene(self.scene)

    def selectActivate(self, flag):
        if flag:
            self.scene.active = True
        else:
            self.scene.active = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(self.ScrollHandDrag)
        super(graphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(self.NoDrag)
        super(graphicsView, self).mouseReleaseEvent(event)

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.active = False

        self._start = QPointF()
        self._current_rect_item = None

        self.FIELD_COLOR = QColor(137, 119, 173, 50)

    def set_image(self, img_path):
        self.mapImg = QPixmap(img_path)
        graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(graphicsPixmapItem)

    def exceptFieldConfirm(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Question)
        self.msg.setText('해당 포인트로 저장 하시겠습니까 ?')
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msg.setDefaultButton(QMessageBox.Yes)
        self.reply = self.msg.exec_()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and self.active:
            self._current_rect_item = QGraphicsRectItem()
            self._current_rect_item.setBrush(self.FIELD_COLOR)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None and self.active:
            r = QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            if self._current_rect_item is not None and self.active:
                self.exceptFieldConfirm()
                self.removeItem(self._current_rect_item)
                if self.reply == QMessageBox.Yes:
                    self._current_rect_item = None
                    self.active = False
        super(GraphicsScene, self).mouseReleaseEvent(event)