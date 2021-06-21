from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, QGraphicsRectItem, \
    QRubberBand
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel


class LayerView(QGraphicsView):
    # rectChanged = pyqtSignal(QRect)
    def __init__(self, backgroundimg):
        super().__init__()

        self.scene = GraphicsScene()
        self.scene.set_image(backgroundimg)
        self.setScene(self.scene)

        # self.setDragMode(QGraphicsView.ScrollHandDrag) # RubberbandDrag -> 박스추가할 때 써도 될 듯
        self._mousePressed = False
        self._isPanning = False
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.bndboxList = []

        self.selectedIndex = None

    def setSignal(self, on_data_changed_func, get_data_func, notify_selected_index):
        self.on_data_changed = on_data_changed_func
        self.get_data = get_data_func
        self.scene.on_selected = notify_selected_index

    def setInitData(self):
        self.data = self.get_data()
        box_num = self.data.shape[0]
        for box_index in range(box_num): # rect 객체 list 만들기
            box = BoundingBox(box_index)
            box.setBrush(QColor(255, 0, 0, 127))
            box.setFlag(QGraphicsItem.ItemIsSelectable, True)
            box.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.scene.addItem(box)
            xmin = int(self.data[box_index][2]) #TODO: table에 보낼 때 int->string
            ymin = int(self.data[box_index][3])
            width = int(self.data[box_index][4]) - xmin
            height = int(self.data[box_index][5]) - ymin
            r = QRectF(xmin, ymin, width, height)
            box.setRect(r)

            self.bndboxList.append(box)

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

        self.on_selected = None # from viewModel

    def set_image(self, img_path):
        self.backImg = QPixmap(img_path)
        # backImg = backImg.scaled(int(self.width()), int(self.height()))
        #

        graphicsPixmapItem = QGraphicsPixmapItem(self.backImg)
        self.addItem(graphicsPixmapItem)

    # def initial_box_draw(self):
    #     self._current_rect_item = QGraphicsRectItem()
    #     self._current_rect_item.setBrush(QColor(255, 0, 0, 127))
    #     self._current_rect_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
    #     self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
    #     # self._current_rect_item.paint(QColor(0, 0, 255, 127))
    #     self.addItem(self._current_rect_item)
    #     self._start = event.scenePos()
    #     r = QRectF(self._start, self._start)
    #     self._current_rect_item.setRect(r)
    #     r = QRectF(self._start, event.scenePos()).normalized()
    #     self._current_rect_item.setRect(r)


    def mousePressEvent(self, event):
        print('pressed')
        print(type(self.itemAt(event.scenePos(), QTransform())))
        if not (isinstance(self.itemAt(event.scenePos(), QTransform()), QGraphicsRectItem)):
            self._current_rect_item = QGraphicsRectItem()
            self._current_rect_item.setBrush(QColor(255, 0, 0, 127))
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            # self._current_rect_item.paint(QColor(0, 0, 255, 127))
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        else:
            self.isDragging = True
            self.selectedItem = self.itemAt(event.scenePos(), QTransform())
            print(self.selectedItem.tableIndex) # Test
            self.on_selected(self.selectedItem.tableIndex)
            QGraphicsItem.mousePressEvent(self.selectedItem, event)

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


class BoundingBox(QGraphicsRectItem):
    def __init__(self, initialIndex):
        super().__init__()
        self.tableIndex = initialIndex



class LayerViewModel:
    def __init__(self, data_model, view):
        super().__init__()
        self.selectedDataIndex = None # Test

        # 모델 객체 이용 (모델)
        self.model = data_model
        # self.data = self.model.getData()
        # self.boxModel = BoxModel(self.data)

        # 처음엔 원본xml로 초기화 (뷰)
        self.layerView = view
        self.layerView.setSignal(on_data_changed_func=self.getChagedDataFromView, get_data_func=self.getBoxData, notify_selected_index = self.notify_selected_index)
        self.layerView.setInitData()

        # self.model.setSelectedDataIndex(self.selectedDataIndex) # TODO:

    def getChagedDataFromView(self, row, value):
        self.updateBoxData(row, value)

        print(row, value, "is changed")  # test
        # box 그리는 것도 추가해야함

    def getBoxData(self):
        return self.model.getBoxData()

    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)

    def notify_selected_index(self, i):
        self.model.setSelectedDataIndex(i)



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


# def selection_changed(self):
#     selection = self.gv.scene().selectedItems()
#     print
#     'Selected:', len(selection)
#     for i in selection:
#         i.setPen(QPen(QColor(255, 255, 255), 0.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
