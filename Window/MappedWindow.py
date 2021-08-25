import os

from Model.BoxModel import BoxModel
from ViewModel.TableViewModel import TableViewModel
from View.TableView import TableView

from PyQt5.QtWidgets import *

from View.LayerView import *
from utils import parseXML

from View.ImgView import *


class MappedWindow(QMainWindow):
    def __init__(self, img, xml):
        super().__init__()
        self.title = img
        self.scaleFactor = 0.0

        self.IMG_NAME = os.path.basename(img).split('.')[0]
        self.IMG_PATH = img
        self.XML_PATH = xml
        self.XML_RESULT = parseXML(self.XML_PATH, xml_type='res')

        self.MODEL = BoxModel(self.XML_RESULT)

        self.initWindowUi(title=self.title)

    def initWindowUi(self, title):
        self.setWindowTitle(title)
        self.move(100, 100)
        self.resize(1600, 800)

        self.createMenubar()

        self.mapWidget = QWidget()
        self.mapWidget.layout = QHBoxLayout()
        self.mapWidget.setLayout(self.mapWidget.layout)
        self.mappedAreaViewr()
        self.mapWidget.setStyleSheet(  # 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: blue;"
            "border-radius: 3px")

        # self.layer = over_layer(self.mappedArea.img_label)
        # self.layer = BoxViewModel(data_model=self.MODEL,
        #                           parent=self.mappedArea.img_label)  ###
        #
        # self.layer.boxView.resize(self.mappedArea.img_label.width(), self.mappedArea.img_label.height())
        # self.layer.boxView.setVisible(True)

        self.tabView()
        self.createDock(self.tabview)
        # self.setCentralWidget(self.mapWidget)
        self.layerView = LayerView(self.IMG_PATH)
        self.layerViewModel = LayerViewModel(self.MODEL, self.layerView)  # 원본 데이터 채워져 있을 것
        self.setCentralWidget(self.layerView)
        self.show()

    def createMenubar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        menuBar.addMenu('&File')
        menuBar.addMenu('&Settings')
        menuBar.addMenu('&Labeling')
        menuBar.addMenu('&Recognition')
        menuBar.addMenu('&Unit Function Test')
        menuBar.addMenu('&Temporary Test')

    def mappedAreaViewr(self):
        self.mappedArea = ImgView()
        self.mappedArea.uploadImg(resize_ratio=0.4, filePath=self.IMG_PATH)
        self.scaleFactor = 1.0
        self.mapWidget.layout.addWidget(self.mappedArea)

    def createDock(self, connectedWidget):
        self.dockingWidget = QDockWidget("XML Result")  # 타이틀 설정
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.dockingWidget.setMinimumSize(int(self.frameGeometry().width() * 0.3), self.frameGeometry().height())
        self.emptyWidgetforLayout = QWidget()
        self.dockingWidget.setWidget(self.emptyWidgetforLayout)

        self.emptyWidgetForButton = QWidget()
        self.layoutForButton = QHBoxLayout()
        self.emptyWidgetForButton.setLayout(self.layoutForButton)

        ''' Top Button '''
        self.addBoxBtn = QPushButton('Add Box')
        self.addBoxBtn.setCheckable(True)
        self.deleteBoxBtn = QPushButton('Delete Box')
        self.saveToXmlBtn = QPushButton('Save to XML')
        self.IsAdding = False
        self.layoutForButton.addWidget(self.addBoxBtn)
        self.layoutForButton.addWidget(self.deleteBoxBtn)
        self.layoutForButton.addWidget(self.saveToXmlBtn)

        # self.addBoxBtn.clicked.connect(self.addBtnClicked)
        # self.cellClicked.connect(self.cell_click)
        self.saveToXmlBtn.clicked.connect(self.saveToXmlBtnClicked)
        self.deleteBoxBtn.clicked.connect(self.deleteBoxBtnClicked)
        self.addBoxBtn.clicked.connect(self.addBoxBtnClicked)

        ''' Dock '''
        self.layoutInDock = QVBoxLayout()
        self.layoutInDock.addWidget(self.emptyWidgetForButton)
        self.layoutInDock.addWidget(connectedWidget)
        self.emptyWidgetforLayout.setLayout(self.layoutInDock)
        self.dockingWidget.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dockingWidget)

    def saveToXmlBtnClicked(self):
        file_save = QFileDialog.getSaveFileName(None, 'Save XML', '', 'XML(*.xml)')
        if file_save[0]:
            file_name = os.path.basename(file_save[0])
            self.tab1_table.saveXML(file_name)

    def deleteBoxBtnClicked(self):
        self.tab1_table.delete_cell()

    def addBoxBtnClicked(self):
        if self.addBoxBtn.isChecked():
            self.addBoxBtn.setStyleSheet("background-color : lightblue")
            self.IsAdding = True
            self.deleteBoxBtn.setEnabled(False)
            self.saveToXmlBtn.setEnabled(False)
            self.layerView.activateDrawBoxMode()

        else:
            self.addBoxBtn.setStyleSheet('background-color: None')
            self.IsAdding = False
            self.deleteBoxBtn.setEnabled(True)
            self.saveToXmlBtn.setEnabled(True)
            self.layerView.deactivateDrawBoxMode()

    def tabView(self):
        self.tabview = QWidget()

        # self.scrollableTabArea = QScrollArea()
        # self.scrollableTabArea.setWidget(self.tabview)

        self.tabview.tabLayout = QVBoxLayout()
        self.tabview.tabs = QTabWidget()

        self.tabview.tab1 = QWidget()
        self.createTab1UI()

        # self.tabview.tab2 = QWidget()

        self.tabview.tabs.resize(int(self.width() * 0.2), int(self.height()))

        self.tabview.tabs.addTab(self.tabview.tab1, 'Recognized Objects')
        # self.tabview.tabs.addTab(self.tabview.tab2, 'Recognized Objects')

        self.tabview.tabLayout.addWidget(self.tabview.tabs)
        self.tabview.setLayout(self.tabview.tabLayout)

    def createTab1UI(self):
        self.tabview.tab1.layout = QHBoxLayout()
        self.tab1_table = TableView()
        self.tableViewModel = TableViewModel(self.MODEL, self.tab1_table)  # 원본 데이터 채워져 있을 것

        self.tabview.tab1.layout.addWidget(self.tab1_table)
        self.tabview.tab1.setLayout(self.tabview.tab1.layout)

    def updateTab1(self):
        header = self.tab1_table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)

# view
class OverLayer(QWidget):
    def __init__(self, parent=None):
        super(OverLayer, self).__init__(parent)

        # self.data = None

        ''' signal to connect with ViewModel '''  # View Model에서 사용

    def setSignal(self, on_data_changed_func, get_data_func):
        self.on_data_changed = on_data_changed_func
        self.get_data = get_data_func

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setBrush(QColor(255, 229, 204, 100))  # 채우기 색깔
        painter.setPen(QPen(QColor(255, 128, 0), 3))  # 선 색깔
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_rect(painter)

    def draw_rect(self, qp):
        self.data = self.get_data()
        # string, orientation, xmin, ymin, xmax, ymax
        for box in self.data:
            xmin = int(box[2])
            ymin = int(box[3])
            xmax = int(box[4])
            ymax = int(box[5])
            width = xmax - xmin
            height = ymax - ymin
            qp.drawRect(xmin, ymin, width, height)  # x,y,width,height
        qp.drawRect(5, 5, 10, 10)


class BoundingBox:
    def __init__(self, data):
        super().__init__()
        self.type = data[0]
        self.clss = data[1]
        self.xmin = int(data[2])
        self.ymin = int(data[3])
        self.xmax = int(data[4])
        self.ymax = int(data[5])
        self.degree = int(data[6])