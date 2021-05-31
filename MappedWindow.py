import os
import sys
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
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
        self.IsInitialized = False # itemChanged 때문에
        self.cellClicked.connect(self.cell_click)  # cellClick 이벤트를 감지하면 cell_click 함수를 실행
        self.itemChanged.connect(self.cell_edit)

        #TODO: checkbox event 설정 필요


        ''' signal to connect with ViewModel '''  # View Model에서 사용
    def setSignal(self, on_data_changed_func, get_data_func):
        self.on_data_changed = on_data_changed_func
        self.get_data = get_data_func

    # def itemChanged(self, item): # connect 할 거면 쓰면 안 됨
    #     self.chaged_row = item.row()
    #     self.changed_col= item.column()
    #     self.changed_content = item.text()
    #     print(self.chaged_row, self.changed_col, self.changed_content)

    def setInitData(self):
        self.data = self.get_data()
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
            self.checkBoxList[i].setChecked(True) # checked가 default

            # 순서: type, string, xmin, ymin, xmax, ymax, orientation, visible
            self.setItem(i, 1, QTableWidgetItem(self.data[i][0]))
            self.setItem(i, 2, QTableWidgetItem(self.data[i][1]))
            self.setItem(i, 3, QTableWidgetItem(self.data[i][2]))
            self.setItem(i, 4, QTableWidgetItem(self.data[i][3]))
            self.setItem(i, 5, QTableWidgetItem(self.data[i][4]))
            self.setItem(i, 6, QTableWidgetItem(self.data[i][5]))
            self.setItem(i, 7, QTableWidgetItem(self.data[i][6]))

        for i in range(8):
            if i == 2:
                continue
            self.resizeColumnToContents(i)

    # def on_table_valueChanged(self, value):
    #     self.lcd.display(value)
    #     self.printLabel(value)
    #     self.logLabel(value)


    def setTableCell(self, newData, i):
        self.setItem(i, 1, QTableWidgetItem(self.newData[i][6]))
        self.setItem(i, 2, QTableWidgetItem(self.newData[i][0]))
        self.setItem(i, 3, QTableWidgetItem(self.newData[i][2]))
        self.setItem(i, 4, QTableWidgetItem(self.newData[i][3]))
        self.setItem(i, 5, QTableWidgetItem(self.newData[i][4]))
        self.setItem(i, 6, QTableWidgetItem(self.newData[i][5]))
        self.setItem(i, 7, QTableWidgetItem(self.newData[i][1]))

    def getTableCell(self, i):
        result = []
        for j in range(1, self.columnCount()):
            result.append(self.item(i, j).text())

        return result

    def cell_click(self):
        clicked_row = (self.selectedIndexes())[0].row()
        print(clicked_row, 'clicked') # Test
        print(self.getTableCell(clicked_row)) # Test

    def cell_edit(self):
        if self.IsInitialized:
            edited_row = (self.selectedIndexes())[0].row()
            edited_cell = self.getTableCell(edited_row)

            if self.checkBoxList[edited_row].isChecked():
                edited_cell.append(1) #TODO: bool 타입으로 저장이 안되는 것 수정 필요
            else:
                edited_cell.append(0)

            edited_cell = np.array(edited_cell) # list type -> np
            print(edited_row, 'changed')  # Test
            self.on_data_changed(edited_row, edited_cell)

    def saveXML(self, filename):
        makeXML(self.get_data(), filename)

# ViewModel
class TableViewModel:
    def __init__(self, data_model, view):
        super().__init__()

        # 모델 객체 이용 (모델)
        self.model = data_model
        # self.data = self.model.getData()
        # self.boxModel = BoxModel(self.data)

        # 처음엔 원본xml로 초기화 (뷰)
        self.Test = False
        self.tableView = view
        self.tableView.setSignal(on_data_changed_func=self.getChagedDataFromView, get_data_func=self.getBoxData)
        self.tableView.setInitData()
        self.tableView.IsInitialized = True

    def getChagedDataFromView(self, row, value):
        self.updateBoxData(row, value)

        print(row, value, "is changed") # test
        # box 그리는 것도 추가해야함

    def getBoxData(self):
        return self.model.getBoxData()

    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)





# view
class over_layer(QWidget):
    def __init__(self, parent=None):
        super(over_layer, self).__init__(parent)

        # self.data = None

        ''' signal to connect with ViewModel '''  # View Model에서 사용
    def setSignal(self, on_data_changed_func, get_data_func):
        self.on_data_changed = on_data_changed_func
        self.get_data = get_data_func

    def paintEvent(self, event):  # painter에 그릴 때(?) 쓰는 이벤트 함수
        painter = QPainter()
        painter.begin(self)
        #painter.fillRect(event.rect(), QBrush(QColor(1, 1, 1, 100))) #TODO QBrush(Qt.transparent)로 바꿔주기

        painter.setBrush(QColor(255, 229, 204, 100))  # 채우기 색깔
        painter.setPen(QPen(QColor(255, 128, 0), 3))  # 선 색깔
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_rect(painter)

    def draw_rect(self, qp):

        self.data = self.get_data()
        # string, orientation, xmin, ymin, xmax, ymax, visible
        for box in self.data:
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
    def getBoxData(self):
        return self.data

    def setBoxData(self, row, newData):
        self.data[row] = newData
        test = self.data[row]


class BoxViewModel:
    def __init__(self, data_model, parent=None):
        super().__init__()


        # xml 원본 데이터로 초기화
        self.model = data_model
        # self.data = self.model.getBoxData()

        # self.boxModel = BoxModel(self.data)
        self.boxView = over_layer(parent)
        self.boxView.setSignal(on_data_changed_func=self.getChagedDataFromView, get_data_func=self.getBoxData)

    def getChagedDataFromView(self, row, value):
        self.updateBoxData(row, value)

        print(row, value, "is changed")
        # box 그리는 것도 추가해야함

    def getBoxData(self):
        return self.model.getBoxData()

    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)

