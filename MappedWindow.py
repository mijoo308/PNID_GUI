import os
import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QVBoxLayout, QTabWidget, QTableWidget, \
    QAbstractItemView, QCheckBox, QTableWidgetItem, QHeaderView, QPushButton

from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel
from utils import parseXML, makeXML

from ImgView import *


class MappedWindow(QMainWindow):
    def __init__(self, img, xml):
        super().__init__()
        self.title = img

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
        self.mapWidget.setStyleSheet( # 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: blue;"
            "border-radius: 3px")

        # self.layer = over_layer(self.mappedArea.img_label)
        self.layer = BoxViewModel(data_model=self.MODEL,
                                  parent=self.mappedArea.img_label)  ### TODO: XML_RESULT 관리

        self.layer.boxView.resize(self.mappedArea.img_label.width(), self.mappedArea.img_label.height())
        self.layer.boxView.setVisible(True)

        self.tabView()
        self.createDock(self.tabview)
        self.setCentralWidget(self.mapWidget)
        self.show()

    # def resizeEvent(self, event):  # 윈도우 사이즈가 달라지면 호출되는 이벤트 함수
    #     # self.layer.boxView.resize(event.size())
    #     event.accept()

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
        self.mappedArea.uploadImg(resize_ratio=1, filePath=self.IMG_PATH)
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
        self.deleteBoxBtn = QPushButton('Delete Box')
        self.saveToXmlBtn = QPushButton('Save to XML')
        self.layoutForButton.addWidget(self.addBoxBtn)
        self.layoutForButton.addWidget(self.deleteBoxBtn)
        self.layoutForButton.addWidget(self.saveToXmlBtn)

        # self.addBoxBtn.clicked.connect(self.addBtnClicked)
        # self.cellClicked.connect(self.cell_click)
        self.saveToXmlBtn.clicked.connect(self.saveToXmlBtnClicked)


        ''' Dock '''
        self.layoutInDock = QVBoxLayout()
        self.layoutInDock.addWidget(self.emptyWidgetForButton)
        self.layoutInDock.addWidget(connectedWidget)
        self.emptyWidgetforLayout.setLayout(self.layoutInDock)
        self.dockingWidget.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dockingWidget)

    # def addBtnClicked(self):
    #     self.tab1_table
    #     # TODO: tableViewModel에서 이벤트 만든 후 연결하기

    def saveToXmlBtnClicked(self):
        self.tab1_table.saveXML(self.IMG_NAME)

    def tabView(self):
        self.tabview = QWidget()

        # self.scrollableTabArea = QScrollArea()
        # self.scrollableTabArea.setWidget(self.tabview)

        self.tabview.tabLayout = QVBoxLayout()
        self.tabview.tabs = QTabWidget()

        self.tabview.tab1 = QWidget()
        self.createTab1UI()

        self.tabview.tab2 = QWidget()

        self.tabview.tabs.resize(int(self.width() * 0.2), int(self.height()))

        self.tabview.tabs.addTab(self.tabview.tab1, 'Labeled Objects')
        self.tabview.tabs.addTab(self.tabview.tab2, 'Recognized Objects')

        self.tabview.tabLayout.addWidget(self.tabview.tabs)
        self.tabview.setLayout(self.tabview.tabLayout)

    def createTab1UI(self):

        self.tabview.tab1.layout = QHBoxLayout()
        self.tab1_table = TableView()
        self.tableViewModel = TableViewModel(self.MODEL, self.tab1_table) # 원본 데이터 채워져 있을 것

        self.tabview.tab1.layout.addWidget(self.tab1_table)
        self.tabview.tab1.setLayout(self.tabview.tab1.layout)

    def updateTab1(self):
        header = self.tab1_table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)

    # def getBoxData(self):

# View
class TableView(QTableWidget):
    def __init__(self):
        super().__init__()
        self.data = None

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cellClicked.connect(self.cell_click)  # cellClick 이벤트를 감지하면 cell_click 함수를 실행

    def setInitData(self, init_data):
        self.data = init_data
        table_size = self.data.shape[0]
        self.setRowCount(table_size)
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(
            ["v", "type", "text", "xmin", "ymin", "xmax", "ymax", "orientation"])

        '''check box'''
        self.checkBoxList = []
        for i in range(table_size):
            ckbox = QCheckBox()
            self.checkBoxList.append(ckbox)
        for i in range(table_size):
            self.setCellWidget(i, 0, self.checkBoxList[i])

            # result 순서 string, orientation, xmin, ymin, xmax, ymax, type
            self.setItem(i, 1, QTableWidgetItem(self.data[i][6]))
            self.setItem(i, 2, QTableWidgetItem(self.data[i][0]))
            self.setItem(i, 3, QTableWidgetItem(self.data[i][2]))
            self.setItem(i, 4, QTableWidgetItem(self.data[i][3]))
            self.setItem(i, 5, QTableWidgetItem(self.data[i][4]))
            self.setItem(i, 6, QTableWidgetItem(self.data[i][5]))
            self.setItem(i, 7, QTableWidgetItem(self.data[i][1]))

        self.setColumnWidth(0, 5)


    def cell_click(self):
        self.clicked_row = (self.selectedIndexes())[0].row()
        print(self.clicked_row, 'clicked') # Test

    def saveXML(self, filename):
        makeXML(self.data, filename)

# ViewModel
class TableViewModel:
    def __init__(self, data_model, view):
        super().__init__()

        # 모델 객체 이용 (모델)
        self.model = data_model
        self.data = self.model.getData()
        # self.boxModel = BoxModel(self.data)

        # 처음엔 원본xml로 초기화 (뷰)
        self.tableView = view
        self.tableView.setInitData(self.data)

    def getBoxData(self):
        return self.data

    def setBoxData(self, newData, index):
        self.data[index] = newData




# view
class over_layer(QWidget):
    def __init__(self, data, parent=None):
        super(over_layer, self).__init__(parent)

        self.box_data = data

    def paintEvent(self, event):  # painter에 그릴 때(?) 쓰는 이벤트 함수
        painter = QPainter()
        painter.begin(self)
        #painter.fillRect(event.rect(), QBrush(QColor(1, 1, 1, 100))) #TODO QBrush(Qt.transparent)로 바꿔주기

        painter.setBrush(QColor(255, 229, 204, 100))  # 채우기 색깔
        painter.setPen(QPen(QColor(255, 128, 0), 3))  # 선 색깔
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_rect(painter, self.box_data)

    def draw_rect(self, qp, boxes):
        # string, orientation, xmin, ymin, xmax, ymax, visible
        for box in boxes:
            visible = box[6]
            if visible:
                xmin = int(box[2])
                ymin = int(box[3])
                xmax = int(box[4])
                ymax = int(box[5])
                width = xmax - xmin
                height = ymax - ymin
                qp.drawRect(xmin, ymin, width, height)  # x,y,width,height
        qp.drawRect(5, 5, 10, 10)


# data
class BoxModel:
    def __init__(self, parsed_data):
        super().__init__()
        self.data = parsed_data
        # string, orientation, xmin, ymin, xmax, ymax, visible

    #     self.row = self.data.shape[0]
    #     self.col = self.data.shape[1]
    #
    #     self.model = QStandardItemModel()
    #     for i in range(self.col):
    #         self.model.appendRow(self.data[:, i])
    #
    def getData(self):
        return self.data



class BoxViewModel:
    def __init__(self, data_model, parent=None):
        super().__init__()

        # xml 원본 데이터로 초기화
        self.model = data_model
        self.data = self.model.getData()

        # self.boxModel = BoxModel(self.data)
        self.boxView = over_layer(self.data, parent)

    def setBoxData(self, newData, index):
        self.data[index] = newData

    # # Button이랑 연결필요
    # def finalResultToXML(self):
    #
    #     data = self.getBoxData()
    #     if data[6]:   # TODO: 일단 xml viewModel에서 만들게 되어있음
    #         makeXML(data)

