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

        self.zoomInCnt = 0
        self.zoomOutCnt = 0

    def selectActivate(self, flag):
        if flag:
            self.scene.active = True
        else:
            self.scene.active = False

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(self.NoAnchor)
        self.setResizeAnchor(self.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
            if self.zoomInCnt < 3:
                self.zoomInCnt += 1
                self.scale(zoomFactor, zoomFactor)
                self.zoomOutCnt -= 1
        else:
            zoomFactor = zoomOutFactor
            if self.zoomOutCnt <= 10:
                self.zoomOutCnt += 1
                self.scale(zoomFactor, zoomFactor)
                self.zoomInCnt -= 1

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

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
        self.region = QRectF()

        self.FIELD_COLOR = QColor(137, 119, 173, 50)

    def set_image(self, img_path):
        self.mapImg = QPixmap(img_path)
        self.graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(self.graphicsPixmapItem)

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
            self.region = QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(self.region)
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            if self._current_rect_item is not None and self.active:
                self.exceptFieldConfirm()
                self.removeItem(self._current_rect_item)
                if self.reply == QMessageBox.Yes:
                    self.cutoffImg()
                    self._current_rect_item = None
                    self.active = False
        super(GraphicsScene, self).mouseReleaseEvent(event)

    def cutoffImg(self):
        painterFrame = QPainter(self.mapImg)
        painterFrame.setCompositionMode(QPainter.CompositionMode_Source)
        painterFrame.fillRect(self.region, Qt.transparent)
        painterFrame.end()
        self.removeItem(self.graphicsPixmapItem)
        self.graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(self.graphicsPixmapItem)