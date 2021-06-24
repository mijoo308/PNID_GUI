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

        #self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    '''def mouseMoveEvent(self, event):
        self.setDragMode(self.ScrollHandDrag)

    def mouseReleaseEvent(self, event):
        self.setDragMode(self.Nodrag)'''

    '''def mousePressEvent(self, event):

        if event.button() == Qt.MidButton:
            self.viewport().setCursor(Qt.ClosedHandCursor)
            self.original_event = event
            handmade_event = QMouseEvent(QEvent.MouseButtonPress, QPointF(event.pos()), Qt.LeftButton, event.buttons(),
                                         Qt.KeyboardModifiers())
            self.mousePressEvent(handmade_event)
            # Im Sure I have to do something here.

        super(graphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton:
            # for changing back to Qt.OpenHandCursor
            self.viewport().setCursor(Qt.OpenHandCursor)
            handmade_event = QMouseEvent(QEvent.MouseButtonRelease, QPointF(event.pos()), Qt.LeftButton,
                                         event.buttons(), Qt.KeyboardModifiers())
            self.mouseReleaseEvent(handmade_event)
        super(graphicsView, self).mouseReleaseEvent(event)'''

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
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

    def set_image(self, img_path):
        self.mapImg = QPixmap(img_path)
        graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(graphicsPixmapItem)