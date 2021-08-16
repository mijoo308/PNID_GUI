import os
import sys
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

'''from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QVBoxLayout, QTabWidget, QTableWidget, \
    QAbstractItemView, QCheckBox, QTableWidgetItem, QHeaderView, QPushButton, QAction, QComboBox, QStandardItemModel,\
    QTreeView'''
from PyQt5.QtWidgets import *

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

    # def getBoxData(self):


# View
class TableView(QTableWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.setSelectionBehavior(QAbstractItemView.SelectItems)  # column값 필요해서 items로 바꿈
        self.IsInitialized = False  # itemChanged 때문에
        self.cellClicked.connect(self.cell_click)  # cellClick 이벤트를 감지하면 cell_click 함수를 실행
        self.doubleClicked.connect(self.double_click)
        self.itemChanged.connect(self.edit_cell)
        self.setStyleSheet("selection-background-color : #c1c5ff;" "selection-color : black;")
        # self.connect(self.horizontalHeader(), SIGNAL("sectionClicked(int"), self.typeSort)
        self.horizontalHeader().sectionClicked.connect(self.typeSort)
        self.type = QComboBox()
        self.type.addItem('text')
        self.type.addItem('equipment_symbol')
        self.type.addItem('pipe_symbol')
        self.type.addItem('instrument_symbol')
        self.type.currentIndexChanged.connect(self.editType)
        self.makeTextComboBox()
        self.equipment.currentIndexChanged.connect(self.equipmentType)
        self.pipe.currentIndexChanged.connect(self.pipeType)
        self.instrument.currentIndexChanged.connect(self.instrumentType)

        self.typeIndex = 0
        self.classIndex = 1
        self.xminIndex = 2
        self.yminIndex = 3
        self.xmaxIndex = 4
        self.ymaxIndex = 5
        self.degreeIndex = 6

        self.current_row = None # to edit sorted cell

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
        self.data = self.get_data().copy()
        table_size = len(self.data)
        self.setRowCount(table_size)
        self.setColumnCount(7)

        self.setHorizontalHeaderLabels(
            ["type", "class", "xmin", "ymin", "xmax", "ymax", "degree"])

        # '''check box'''
        # self.checkBoxList = []
        # for i in range(table_size):
        #     ckbox = QCheckBox()
        #     self.checkBoxList.append(ckbox)
        for i in range(table_size):
            # self.setCellWidget(i, 0, self.checkBoxList[i])
            # self.checkBoxList[i].setChecked(True)  # checked가 default

            # 순서: type, string, xmin, ymin, xmax, ymax, degree, visible
            self.setItem(i, self.typeIndex, QTableWidgetItem(self.data[i][0]))
            self.setItem(i, self.classIndex, QTableWidgetItem(str(self.data[i][1])))
            self.setItem(i, self.xminIndex, QTableWidgetItem(str(self.data[i][2])))
            self.setItem(i, self.yminIndex, QTableWidgetItem(str(self.data[i][3])))
            self.setItem(i, self.xmaxIndex, QTableWidgetItem(str(self.data[i][4])))
            self.setItem(i, self.ymaxIndex, QTableWidgetItem(str(self.data[i][5])))
            self.setItem(i, self.degreeIndex, QTableWidgetItem(str(self.data[i][6])))

        for i in range(self.columnCount()):
            if i == self.classIndex:
                continue
            self.resizeColumnToContents(i)

        # for i in range(self.rowCount()):
        #     test = self.rowAt(i)
        #     print(test)


    # def on_table_valueChanged(self, value):
    #     self.lcd.display(value)
    #     self.printLabel(value)
    #     self.logLabel(value)

    def typeSort(self, idx):
        if idx == self.typeIndex:
            self.setSortingEnabled(True)
            self.sortItems(self.typeIndex, Qt.AscendingOrder)
            self.setSortingEnabled(False)

            # self.sortItems(1, Qt.DescendingOrder)

    def setTableCell(self, newData, i):
        # self.setCellWidget(i, 0, self.checkBoxList[i])
        # self.checkBoxList[i].setChecked(True)
        self.setItem(i, self.typeIndex, QTableWidgetItem(newData[0]))
        self.setItem(i, self.classIndex, QTableWidgetItem(str(newData[1])))
        self.setItem(i, self.xminIndex, QTableWidgetItem(str(newData[2])))
        self.setItem(i, self.yminIndex, QTableWidgetItem(str(newData[3])))
        self.setItem(i, self.xmaxIndex, QTableWidgetItem(str(newData[4])))
        self.setItem(i, self.ymaxIndex, QTableWidgetItem(str(newData[5])))
        self.setItem(i, self.degreeIndex, QTableWidgetItem(str(newData[6])))

    def addTableCell(self, addedData):
        self.current_row = None
        row = self.rowCount()
        self.insertRow(row)
        self.setTableCell(newData=addedData, i=row)

        added_row = addedData.copy()
        for i in range(self.xminIndex, self.degreeIndex + 1):
            added_row[i] = int(added_row[i])

        print(added_row, 'is added row')

        self.data.append(added_row)
        self.selectRow(row)

    def getTableCell(self, i, j=None):
        result = []
        if j is None:
            for col in range(0, self.columnCount()):
                result.append(self.item(i, col).text())

        else:
            result.append(self.item(i, j).text())

        return result

    def returnOriginDataIndex(self, sorted_index):
        current_row = self.getTableCell(sorted_index).copy()
        for i in range(self.xminIndex, self.degreeIndex+1):
            current_row[i] = int(current_row[i])

        origin_index = self.data.index(current_row)

        return origin_index


    def cell_click(self):
        self.clicked_row_index = (self.selectedIndexes())[0].row()
        self.current_row = self.getTableCell(self.clicked_row_index)

        origin_index = self.returnOriginDataIndex(self.clicked_row_index)

        print(origin_index, 'is original index')

        # self.clicked_col = index.column()
        print(self.clicked_row_index, 'clicked')  # Test
        print(self.getTableCell(self.clicked_row_index))  # Test
        self.on_selected(origin_index)

    def double_click(self):
        index = (self.selectionModel().currentIndex())
        self.double_row = index.row()
        self.double_col = index.column()

        if self.double_col == self.typeIndex:
            self.setCellWidget(self.double_row, self.double_col, self.type)
            self.setItem(self.double_row, self.double_col, QTableWidgetItem(self.type.currentText()))
        elif self.double_col == self.classIndex:
            type = self.getTableCell(i=self.double_row, j=self.typeIndex)
            self.editText(text=type)

    def makeTextComboBox(self):
        self.equipment = QComboBox()
        self.pipe = QComboBox()
        self.instrument = QComboBox()

        f = open('./SymbolClass_Type/Hyundai_SymbolClass_Type.txt', 'r')
        lines = f.readlines()
        for line in lines:
            i = line.find('|')
            j = line.find('\n')
            if line[0:i] == 'equipment_symbol':
                self.equipment.addItem(line[i + 1:j])
            elif line[0:i] == 'pipe_symbol':
                self.pipe.addItem(line[i + 1:j])
            elif line[0:i] == 'instrument_symbol':
                self.instrument.addItem(line[i + 1:j])

    def editText(self, text):
        if text == ['equipment_symbol']:
            self.setCellWidget(self.double_row, self.double_col, self.equipment)
            self.equipmentType()

        elif text == ['pipe_symbol']:
            self.setCellWidget(self.double_row, self.double_col, self.pipe)
            self.pipeType()
        elif text == ['instrument_symbol']:
            self.setCellWidget(self.double_row, self.double_col, self.instrument)
            self.instrumentType()

    def selectText(self, text):
        if text == 'equipment_symbol':
            self.setCellWidget(self.double_row, self.classIndex, self.equipment)

        elif text == 'pipe_symbol':
            self.setCellWidget(self.double_row, self.classIndex, self.pipe)

        elif text == 'instrument_symbol':
            self.setCellWidget(self.double_row, self.classIndex, self.instrument)

    def editType(self):
        type = str(self.type.currentText())
        self.setItem(self.double_row, self.double_col, QTableWidgetItem(type))
        self.selectText(text=type)
        if type == 'equipment_symbol':
            self.equipmentType()
        elif type == 'pipe_symbol':
            self.pipeType()
        elif type == 'instrument_symbol':
            self.instrumentType()

    def equipmentType(self):
        type = str(self.equipment.currentText())
        self.setItem(self.double_row, self.classIndex, QTableWidgetItem(type))

    def pipeType(self):
        type = str(self.pipe.currentText())
        self.setItem(self.double_row, self.classIndex, QTableWidgetItem(type))

    def instrumentType(self):
        type = str(self.instrument.currentText())
        self.setItem(self.double_row, self.classIndex, QTableWidgetItem(type))

    def edit_cell(self):
        if self.IsInitialized:
            if self.selectedIndexes() and self.current_row is not None:
                origin_row = self.current_row.copy()
                edited_row_index = self.selectedIndexes()[0].row()
                edited_row = self.getTableCell(edited_row_index)

                # if self.checkBoxList[edited_row_index].isChecked():
                #     edited_row.append(True)  # TODO: bool 타입으로 저장이 안되는 것 수정 필요
                # else:
                #     edited_row.append(False)

                # edited_row = np.array(edited_row)  # list type -> np  np제거
                print(edited_row_index, 'changed')  # Test
                if self.getTableCell(i=edited_row_index, j=self.typeIndex) == ['']:
                    self.setItem(edited_row_index, self.typeIndex, QTableWidgetItem('text'))

                for i in range(self.xminIndex, self.degreeIndex + 1):
                    origin_row[i] = int(origin_row[i])

                origin_index = self.data.index(origin_row)

                print(origin_index, 'is origin_index')
                print(edited_row_index,' is edited_row_index')

                self.on_data_changed_from_view(origin_index, edited_row)  # row 단위로 업데이트

                self.current_row = edited_row.copy()

                for i in range(self.xminIndex, self.degreeIndex + 1):
                    edited_row[i] = int(edited_row[i])

                self.data[origin_index] = edited_row

    def delete_cell(self):
        deleted_index = self.selectedIndexes()[0].row()

        origin_index = self.returnOriginDataIndex(deleted_index)

        self.removeRow(deleted_index) # Table삭제
        # del self.checkBoxList[deleted_index]
        self.on_deleted(origin_index) # Model에서 삭제
        del self.data[origin_index]

    def saveXML(self, filename):
        makeXML(self.get_data(), filename)

    def selectionChange(self, i):  # ViewModel에서 사용
        self.setCurrentCell(i, self.classIndex)


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

        new_row = ['', string, xmin, ymin, xmax, ymax, orientation]
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
