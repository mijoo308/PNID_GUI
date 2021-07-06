import sys

from MainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel, QBrush

class graphicsView(QGraphicsView):
    def __init__(self, imgPath):
        super().__init__()

        self.setBackgroundBrush(QBrush(Qt.white, Qt.SolidPattern))

        self.scene = GraphicsScene()
        self.scene.set_image(img_path=imgPath)
        self.setScene(self.scene)

        self.zoomInCnt = 0
        self.zoomOutCnt = 0

    def selectActivate(self, flag, state):
        if flag == 'except' and state == True:
            self.scene.exceptActive = True
            self.scene.outlineActive = False
        elif flag == 'except' and state == False:
            self.scene.exceptActive = False
        elif flag == 'outline' and state == True :
            self.scene.outlineActive = True
            self.scene.exceptActive = False
        else:
            self.scene.outlineActive = False

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
        self.exceptActive = False
        self.outlineActive = False

        self._start = QPointF()
        self._current_rect_item = None
        self.exceptRegion = QRectF()
        self.outlineRegion = QRect()

        self.EXCEPT_FIELD_COLOR = QColor(137, 119, 173, 50)
        self.OUTLINE_FIELD_COLOR = QColor(150, 38, 23, 50)

    def set_image(self, img_path):
        self.img = QPixmap(img_path)
        self.graphicsPixmapItem = QGraphicsPixmapItem(self.img)
        self.addItem(self.graphicsPixmapItem)

    def exceptFieldConfirm(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('해당 포인트로 저장 하시겠습니까 ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        self.exceptReply = msg.exec_()

    def outlineConfirm(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('해당 포인트로 저장 하시겠습니까 ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        self.outlineReply = msg.exec_()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and self.exceptActive:
            self._current_rect_item = QGraphicsRectItem()
            self._current_rect_item.setBrush(self.EXCEPT_FIELD_COLOR)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        elif event.button() == Qt.RightButton and self.outlineActive:
            self._current_rect_item = QGraphicsRectItem()
            self._current_rect_item.setBrush(self.OUTLINE_FIELD_COLOR)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None and self.exceptActive:
            self.exceptRegion = QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(self.exceptRegion)
        elif self._current_rect_item is not None and self.outlineActive:
            self.outlineRegion = QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(self.outlineRegion)
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            if self._current_rect_item is not None and self.exceptActive:
                self.exceptFieldConfirm()
                self.removeItem(self._current_rect_item)
                if self.exceptReply == QMessageBox.Yes:
                    self.cutoffImg()
                    self._current_rect_item = None
                    self.exceptActive = False
            if self._current_rect_item is not None and self.outlineActive:
                self.outlineConfirm()
                self.removeItem(self._current_rect_item)
                if self.outlineReply == QMessageBox.Yes:
                    self.outline()
                    self._current_rect_item = None
                    self.outlineActive = False
        super(GraphicsScene, self).mouseReleaseEvent(event)

    def outline(self):
        x = int(self.outlineRegion.x())
        y = int(self.outlineRegion.y())
        width = int(self.outlineRegion.width())
        height = int(self.outlineRegion.height())
        input = self.img.copy(x, y, width, height)
        mapImg = QPixmap(input.size())
        mapImg.fill(Qt.transparent)
        painter = QPainter(mapImg)
        painter.setOpacity(0.999)
        painter.drawPixmap(0, 0, input)
        painter.end()
        mapImg.save('./icon_img/convertPNG.png', 'png')
        self.mapImg = QPixmap('./icon_img/convertPNG.png')
        self.clear()
        self.graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(self.graphicsPixmapItem)

    def cutoffImg(self):
        painterFrame = QPainter(self.mapImg)
        painterFrame.setCompositionMode(QPainter.CompositionMode_Clear)
        painterFrame.eraseRect(self.exceptRegion)
        painterFrame.end()
        self.removeItem(self.graphicsPixmapItem)
        self.graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(self.graphicsPixmapItem)
        self.mapImg.save('./icon_img/EditImg.png', 'png')