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

    def mousePressEvent(self, event):
        self.setDragMode(self.ScrollHandDrag)
        super(graphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(self.NoDrag)
        super(graphicsView, self).mouseReleaseEvent(event)

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

    def set_image(self, img_path):
        self.mapImg = QPixmap(img_path)
        graphicsPixmapItem = QGraphicsPixmapItem(self.mapImg)
        self.addItem(graphicsPixmapItem)