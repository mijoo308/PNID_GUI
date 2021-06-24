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
        self.currentItem = None

        self.DEFAULT_COLOR = QColor(255, 0, 0, 50)
        self.SELECTED_COLOR = QColor(0, 0, 255, 50)

    def setSignal(self, on_data_changed_func, get_data_func, notify_selected_index):
        self.on_data_changed = on_data_changed_func
        self.get_data = get_data_func
        self.scene.on_selected = notify_selected_index

    def setInitData(self):
        self.data = self.get_data()
        box_num = self.data.shape[0]
        for box_index in range(box_num): # rect 객체 list 만들기
            box = BoundingBox(box_index)
            box.setBrush(self.DEFAULT_COLOR)
            box.setFlag(QGraphicsItem.ItemIsSelectable, True)
            box.setFlag(QGraphicsItem.ItemIsMovable, True)
            box.setFlag(QGraphicsItem.ItemIsFocusable, True)
            self.scene.addItem(box)
            xmin = int(self.data[box_index][2]) #TODO: table에 보낼 때 int->string
            ymin = int(self.data[box_index][3])
            width = int(self.data[box_index][4]) - xmin
            height = int(self.data[box_index][5]) - ymin
            r = QRectF(xmin, ymin, width, height)
            box.setRect(r)

            self.bndboxList.append(box)

    def selectionChange(self, i):
        current_item = self.bndboxList[i]
        self.centerOn(current_item)
        self.changeSelctedItemColor(current_item)
        # test = current_item.scenePos()
        # self.centerOn(current_item.pos())

    def on_deleted(self, i):
        self.scene.removeItem(self.bndboxList[i])
        del self.bndboxList[i]

    def changeSelctedItemColor(self, item):
        if self.currentItem is not None:
            self.currentItem.setBrush(self.DEFAULT_COLOR)
        self.currentItem = item
        self.currentItem.setBrush(self.SELECTED_COLOR)

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

    def redraw_box(self, i, new_row): # ?
        self.scene.removeItem(self.bndboxList[i])
        self.bndboxList[i].setBrush(self.DEFAULT_COLOR)
        self.bndboxList[i].setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.bndboxList[i].setFlag(QGraphicsItem.ItemIsMovable, True)
        self.bndboxList[i].setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.scene.addItem(self.bndboxList[i])
        xmin = int(new_row[2])  # TODO: table에 보낼 때 int->string
        ymin = int(new_row[3])
        width = int(new_row[4]) - xmin
        height = int(new_row[5]) - ymin
        r = QRectF(xmin, ymin, width, height)
        self.bndboxList[i].setRect(r)





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

        self.NEWBOX_COLOR = QColor(0, 0, 200, 50)

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
        if not (isinstance(self.itemAt(event.scenePos(), QTransform()), QGraphicsRectItem)): # 새로운 박스 추가
            self._current_rect_item = QGraphicsRectItem()
            self._current_rect_item.setBrush(self.NEWBOX_COLOR)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            # self._current_rect_item.setFlag(QGraphicsItem.ItemIsFocusable, True) # ?
            # self._current_rect_item.paint(QColor(0, 0, 255, 127))
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        else:                                                                               # 박스 움직임
            self.isDragging = True
            self.selectedItem = self.itemAt(event.scenePos(), QTransform())
            print(self.selectedItem.tableIndex) # TODO: 새로만든 박스 table에 추가 필요 (box생성 enable버튼도 필요)
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
        # self.xmin = None
        # self.ymin = None
        # self.xmax = None
        # self.ymax = None



class LayerViewModel:
    def __init__(self, data_model, view):
        super().__init__()
        self.selectedDataIndex = None

        # 모델 객체 이용 (모델)
        self.model = data_model
        self.model.setLayerSignal(notify_selected_to_layer=self.get_selected_index, notify_deleted_to_layer=self.get_deleted_index, notify_edited_to_layer=self._redraw_box)
        # self.data = self.model.getData()
        # self.boxModel = BoxModel(self.data)

        # 처음엔 원본xml로 초기화 (뷰)
        self.layerView = view
        self.layerView.setSignal(on_data_changed_func=self.getChagedDataFromView, get_data_func=self.getBoxData, notify_selected_index=self.notify_selected_index)
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
        self.model.setSelectedDataIndex(i, 0)

    def get_selected_index(self, i):
        self.selectedIndex = i
        self.layerView.selectionChange(self.selectedIndex)

    def get_deleted_index(self, i):
        self.deletedIndex = i
        self.layerView.on_deleted(self.deletedIndex)

    def _redraw_box(self, i, newRow):
        self.layerView.redraw_box(i, newRow)


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
