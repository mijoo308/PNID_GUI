import os
import sys
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QVBoxLayout, QTabWidget, QTableWidget, \
    QAbstractItemView, QCheckBox, QTableWidgetItem, QHeaderView, QPushButton, QAction

from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel

from LayerView import *
from utils import parseXML, makeXML

from ImgView import *


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

        self.createActioon()
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

    def createActioon(self):
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut='Ctrl++', enabled=True, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut='Ctrl+-', enabled=True, triggered=self.zoomOut)

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.mappedArea.img_label.resize(self.scaleFactor * self.mappedArea.img_label.pixmap().size())

        self.adjustScrollBar(self.mappedArea.scrollbarX, factor)
        self.adjustScrollBar(self.mappedArea.scrollbarY, factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 4.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.222)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def createMenubar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        menuBar.addMenu('&File')
        menuBar.addMenu('&Settings')
        menuBar.addMenu('&Labeling')
        menuBar.addMenu('&Recognition')
        menuBar.addMenu('&Unit Function Test')
        menuBar.addMenu('&Temporary Test')
        zoom = menuBar.addMenu('&Zoom')
        zoom.addAction(self.zoomInAct)
        zoom.addAction(self.zoomOutAct)

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
        self.tab1_table.saveXML(self.IMG_NAME)

    def deleteBoxBtnClicked(self):
        self.tab1_table.delete_cell()  # layerView에서 박스 삭제 필요

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

        self.tabview.tab2 = QWidget()

        self.tabview.tabs.resize(int(self.width() * 0.2), int(self.height()))

        self.tabview.tabs.addTab(self.tabview.tab1, 'Labeled Objects')
        self.tabview.tabs.addTab(self.tabview.tab2, 'Recognized Objects')

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

    # def getBoxData(self):


# View
class TableView(QTableWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.setSelectionBehavior(QAbstractItemView.SelectItems)  # column값 필요해서 items로 바꿈
        self.IsInitialized = False  # itemChanged 때문에
        self.cellClicked.connect(self.cell_click)  # cellClick 이벤트를 감지하면 cell_click 함수를 실행
        self.itemChanged.connect(self.edit_cell)
        self.setStyleSheet("selection-background-color : #c1c5ff;" "selection-color : black;")

        # TODO: checkbox event 설정 필요

        ''' signal to connect with ViewModel '''  # View Model에서 사용

    def setSignal(self, on_data_changed_from_view, get_data_func, notify_selected_index, notify_deleted_index):
        self.on_data_changed_from_view = on_data_changed_from_view
        self.get_data = get_data_func
        self.on_selected = notify_selected_index
        self.on_deleted = notify_deleted_index

    # def itemChanged(self, item): # connect 할 거면 쓰면 안 됨
    #     self.chaged_row = item.row()
    #     self.changed_col= item.column()
    #     self.changed_content = item.text()
    #     print(self.chaged_row, self.changed_col, self.changed_content)

    def setInitData(self):
        self.data = self.get_data()
        table_size = len(self.data)
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
            self.checkBoxList[i].setChecked(True)  # checked가 default

            # 순서: type, string, xmin, ymin, xmax, ymax, orientation, visible
            self.setItem(i, 1, QTableWidgetItem(self.data[i][0]))
            self.setItem(i, 2, QTableWidgetItem(str(self.data[i][1])))
            self.setItem(i, 3, QTableWidgetItem(str(self.data[i][2])))
            self.setItem(i, 4, QTableWidgetItem(str(self.data[i][3])))
            self.setItem(i, 5, QTableWidgetItem(str(self.data[i][4])))
            self.setItem(i, 6, QTableWidgetItem(str(self.data[i][5])))
            self.setItem(i, 7, QTableWidgetItem(str(self.data[i][6])))

        for i in range(8):
            if i == 2:
                continue
            self.resizeColumnToContents(i)

    # def on_table_valueChanged(self, value):
    #     self.lcd.display(value)
    #     self.printLabel(value)
    #     self.logLabel(value)


    def setTableCell(self, newData, i):
        self.setCellWidget(i, 0, self.checkBoxList[i])
        self.checkBoxList[i].setChecked(True)
        self.setItem(i, 1, QTableWidgetItem(newData[0]))
        self.setItem(i, 2, QTableWidgetItem(str(newData[1])))
        self.setItem(i, 3, QTableWidgetItem(str(newData[2])))
        self.setItem(i, 4, QTableWidgetItem(str(newData[3])))
        self.setItem(i, 5, QTableWidgetItem(str(newData[4])))
        self.setItem(i, 6, QTableWidgetItem(str(newData[5])))
        self.setItem(i, 7, QTableWidgetItem(str(newData[6])))

    def addTableCell(self, addedData):
        row = self.rowCount()
        self.insertRow(row)

        ckbox = QCheckBox()
        self.checkBoxList.append(ckbox)
        self.setTableCell(addedData, row)
        self.selectRow(row)

    def getTableCell(self, i, j=None):
        result = []
        if j is None:
            for col in range(1, self.columnCount()):
                result.append(self.item(i, col).text())

        else:
            result.append(self.item(i, j).text())

        return result

    def cell_click(self):
        clicked_row = (self.selectedIndexes())[0].row()
        print(clicked_row, 'clicked')  # Test
        print(self.getTableCell(clicked_row))  # Test
        self.on_selected(clicked_row)

    def edit_cell(self):
        if self.IsInitialized:
            if self.selectedIndexes():
                edited_row_index = self.selectedIndexes()[0].row()
                edited_row = self.getTableCell(edited_row_index)

                if self.checkBoxList[edited_row_index].isChecked():
                    edited_row.append(True)  # TODO: bool 타입으로 저장이 안되는 것 수정 필요
                else:
                    edited_row.append(False)

                # edited_row = np.array(edited_row)  # list type -> np  np제거
                print(edited_row_index, 'changed')  # Test
                self.on_data_changed_from_view(edited_row_index, edited_row)  # row 단위로 업데이트

    def delete_cell(self):
        deleted_index = self.selectedIndexes()[0].row()
        self.removeRow(deleted_index)
        del self.checkBoxList[deleted_index]
        self.on_deleted(deleted_index)

    def saveXML(self, filename):
        makeXML(self.get_data(), filename)

    def selectionChange(self, i):  # ViewModel에서 사용
        self.setCurrentCell(i, 2)


# ViewModel
class TableViewModel:
    def __init__(self, data_model, view):
        super().__init__()

        # 모델 객체 이용 (모델)
        self.model = data_model
        self.selectedIndex = None
        # self.data = self.model.getData()
        # self.boxModel = BoxModel(self.data)

        # 처음엔 원본xml로 초기화 (뷰)
        self.tableView = view
        self.tableView.setSignal(on_data_changed_from_view=self.getChagedDataFromView, get_data_func=self.getBoxData,
                                 notify_selected_index=self.notify_selected_index,
                                 notify_deleted_index=self.notify_deleted_index)
        self.model.setTableSignal(notify_selected_to_table=self.get_selected_index,
                                  notify_added_to_table=self.get_added_box)
        self.tableView.setInitData()
        self.tableView.IsInitialized = True

    def getChagedDataFromView(self, row, value):
        self.updateBoxData(row, value)

        print(row, value, "is changed")  # test
        # box 그리는 것도 추가해야함

    def getBoxData(self):
        return self.model.getBoxData()

    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)

    def get_selected_index(self, i):
        self.selectedIndex = i
        self.tableView.selectionChange(self.selectedIndex)

    def get_added_box(self):
        added_data = self.model.getBoxData(idx=-1).copy()
        self.tableView.addTableCell(added_data)
        # table view에 업데이트

    def notify_selected_index(self, i):
        self.model.setSelectedDataIndex(i, 1)

    def notify_deleted_index(self, i):
        self.model.deleteBox(i)


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
        self.selectedDataIndex = None
        # string, orientation, xmin, ymin, xmax, ymax, visible

    #     self.row = self.data.shape[0]
    #     self.col = self.data.shape[1]
    #
    #     self.model = QStandardItemModel()
    #     for i in range(self.col):
    #         self.model.appendRow(self.data[:, i])

    def setLayerSignal(self, notify_selected_to_layer, notify_deleted_to_layer, notify_edited_to_layer):
        self.notify_selected_to_layer = notify_selected_to_layer
        self.notify_deleted_to_layer = notify_deleted_to_layer
        self.notify_edited_to_layer = notify_edited_to_layer

    def setTableSignal(self, notify_selected_to_table, notify_added_to_table):
        self.notify_selected_to_table = notify_selected_to_table
        self.notify_added_to_table = notify_added_to_table

    def deleteBox(self, i):
        del self.data[i]
        self.notify_deleted_to_layer(i)

    def setSelectedDataIndex(self, index, flag):  # flag = 0 : to table/ 1: to layer
        self.selectedDataIndex = index
        if flag == 0:
            self.notify_selected_to_table(self.selectedDataIndex)
        elif flag == 1:
            self.notify_selected_to_layer(self.selectedDataIndex)

    def getBoxData(self, idx=None):
        if idx is None:
            return self.data
        else:
            return self.data[idx]

    def setBoxData(self, i, new_data):
        prev_data = self.data[i].copy()
        self.data[i] = new_data

        bndbox_ischanged = False
        for bndbox_idx in range(2, 6):  # box 좌표가 바뀌었으면
            if prev_data[bndbox_idx] != new_data[bndbox_idx]:
                bndbox_ischanged = True
                break
        if bndbox_ischanged:
            self.notify_edited_to_layer(i, new_data)

    def addBoxData(self, new_bndbox):
        xmin = new_bndbox[0]
        ymin = new_bndbox[1]
        xmax = new_bndbox[2]
        ymax = new_bndbox[3]
        string = ''
        orientation = 0

        if ymax - ymin > xmax - xmin: orientation = 90

        new_row = ['text', string, xmin, ymin, xmax, ymax, orientation, True]
        # self.data = np.append(self.data, new_row, axis=1) # np제거
        self.data.append(new_row)

        self.notify_added_to_table()


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

    def getBoxData(self):
        return self.model.getBoxData()

    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)
