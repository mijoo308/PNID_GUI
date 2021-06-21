from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, QGraphicsRectItem, \
    QRubberBand
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel

class LayerView(QGraphicsView):
    # rectChanged = pyqtSignal(QRect)
    def __init__(self):
        super(LayerView, self).__init__()


        # self.setDragMode(QGraphicsView.ScrollHandDrag) # RubberbandDrag -> 박스추가할 때 써도 될 듯
        self._mousePressed = False
        self._isPanning = False
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    #     self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
    #     self.setMouseTracking(True)
    #     self.origin = QPoint()
    #     self.changeRubberBand = False
    #
    # def mousePressEvent(self, event):
    #     self.origin = event.pos()
    #     self.rubberBand.setGeometry(QRect(self.origin, QSize()))
    #     self.rectChanged.emit(self.rubberBand.geometry())
    #     self.rubberBand.show()
    #     self.changeRubberBand = True
    #     QGraphicsView.mousePressEvent(self, event)
    #
    # def mouseMoveEvent(self, event):
    #     if self.changeRubberBand:
    #         self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    #         self.rectChanged.emit(self.rubberBand.geometry())
    #     QGraphicsView.mouseMoveEvent(self, event)
    #
    # def mouseReleaseEvent(self, event):
    #     self.changeRubberBand = False
    #     QGraphicsView.mouseReleaseEvent(self, event)
    #
    # def onRectChanged(self, r):
    #     topLeft = r.topLeft()
    #     bottomRight = r.bottomRight()
    #     print(topLeft.x(), topLeft.y(), bottomRight.x(), bottomRight.y())

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self._mousePressed = True
    #         if self._isPanning:
    #             self.setCursor(Qt.ClosedHandCursor)
    #             self._dragPos = event.pos()
    #             event.accept()
    #         else:
    #             super(LayerView, self).mousePressEvent(event)
    #     elif event.button() == Qt.MiddleButton:
    #         self._mousePressed = True
    #         self._isPanning = True
    #         self.setCursor(Qt.ClosedHandCursor)
    #         self._dragPos = event.pos()
    #         event.accept()
    #
    # def mouseMoveEvent(self, event):
    #     if self._mousePressed and self._isPanning:
    #         newPos = event.pos()
    #         diff = newPos - self._dragPos
    #         self._dragPos = newPos
    #         self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
    #         self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
    #         event.accept()
    #     else:
    #         super(LayerView, self).mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         if self._isPanning:
    #             self.setCursor(Qt.OpenHandCursor)
    #         else:
    #             self._isPanning = False
    #             self.setCursor(Qt.ArrowCursor)
    #         self._mousePressed = False
    #     elif event.button() == Qt.MiddleButton:
    #         self._isPanning = False
    #         self.setCursor(Qt.ArrowCursor)
    #         self._mousePressed = False
    #     super(LayerView, self).mouseReleaseEvent(event)
    #
    # def mouseDoubleClickEvent(self, event):
    #     self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
    #     pass
    #
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Space and not self._mousePressed:
    #         self._isPanning = True
    #         self.setCursor(Qt.OpenHandCursor)
    #     else:
    #         super(LayerView, self).keyPressEvent(event)
    #
    # def keyReleaseEvent(self, event):
    #     if event.key() == Qt.Key_Space:
    #         if not self._mousePressed:
    #             self._isPanning = False
    #             self.setCursor(Qt.ArrowCursor)
    #     else:
    #         super(LayerView, self).keyPressEvent(event)

    # def wheelEvent(self, event):
    #     # zoom factor
    #     factor = 1.25
    #
    #     # Set Anchors
    #     self.setTransformationAnchor(QGraphicsView.NoAnchor)
    #     self.setResizeAnchor(QGraphicsView.NoAnchor)
    #
    #     # Save the scene pos
    #     oldPos = self.mapToScene(event.pos())
    #
    #     # Zoom
    #     if event.delta() < 0:
    #         factor = 1.0 / factor
    #     self.scale(factor, factor)
    #
    #     # Get the new position
    #     newPos = self.mapToScene(event.pos())
    #
    #     # Move scene to old position
    #     delta = newPos - oldPos
    #     self.translate(delta.x(), delta.y())

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # self.setBackgroundBrush(QBrush(QColor(255, 255, 255, 100)))
        self.backImg = ''
        self._start = QPointF()
        self._current_rect_item = None
        self.isDragging = False
        self.selectedItem = None
        self.setSceneRect(0, 0, 680, 459)


    def set_image(self, img_path):
        self.backImg = QPixmap(img_path)
        # backImg = backImg.scaled(int(self.width()), int(self.height()))
        #

        graphicsPixmapItem = QGraphicsPixmapItem(self.backImg)
        self.addItem(graphicsPixmapItem)

    def mousePressEvent(self, event):
        print('pressed')
        print(type(self.itemAt(event.scenePos(), QTransform())))
        if not(isinstance(self.itemAt(event.scenePos(), QTransform()), GraphicsRectItem)):
            self._current_rect_item = GraphicsRectItem()
            self._current_rect_item.setBrush(QColor(255, 0, 0, 127))
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self._current_rect_item.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
            # self._current_rect_item.paint(QColor(0, 0, 255, 127))
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        else:
            self.isDragging = True
            self.selectedItem = self.itemAt(event.scenePos(), QTransform())
            QGraphicsItem.mousePressEvent(self.selectedItem, event)

        # self.mousePressEvent(event)
        # prepareGeometryChange()

    def mouseMoveEvent(self, event):
        if self.isDragging:
            QGraphicsItem.mouseMoveEvent(self.selectedItem, event)

        elif self._current_rect_item is not None:
            r = QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(r)

        # self.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.isDragging:
            QGraphicsItem.mouseReleaseEvent(self.selectedItem, event)
            self.isDragging = False

        else:
            self._current_rect_item = None
        # self.mouseReleaseEvent(event)






    # def draw_rect(self):
    #     # create painter instance with pixmap
    #     self.painterInstance = QPainter(self.backImg)
    #
    #     # set rectangle color and thickness
    #     self.pen = QPen(Qt.red)
    #     self.pen.setWidth(3)
    #
    #     # draw rectangle on painter
    #     self.painterInstance.setPen(self.pen)
    #     self.painterInstance.drawRect(100, 100, 1000, 1000) # test



# def populate(self):
#     scene = self.gv.scene()
#
#     for i in range(500):
#         rect = scene.addEllipse(300, 500, 20, 20,
#                                 QPen(QColor(255, 128, 0), 0.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin),
#                                 QBrush(QColor(255, 0, 0, 128)))
#         rect.setFlag(QGraphicsItem.ItemIsSelectable)
#         rect.setFlag(QGraphicsItem.ItemIsMovable)
#         x = random.randint(0, 1000)
#         y = random.randint(0, 1000)
#         r = random.randint(2, 8)
#         rect = scene.addEllipse(x, y, r, r,
#                                 QPen(QColor(255, 128, 0), 0.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin),
#                                 QBrush(QColor(255, 128, 20, 128)))
#         rect.setFlag(QGraphicsItem.ItemIsSelectable)
#         rect.setFlag(QGraphicsItem.ItemIsMovable)

class GraphicsRectItem(QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            print("MR")
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)

# def selection_changed(self):
#     selection = self.gv.scene().selectedItems()
#     print
#     'Selected:', len(selection)
#     for i in selection:
#         i.setPen(QPen(QColor(255, 255, 255), 0.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

