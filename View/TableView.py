
from PyQt5.QtWidgets import QTableWidget, QComboBox, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QEvent, QPoint
from utils import *


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

            # 순서: type, string, xmin, ymin, xmax, ymax, degree
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

        # print(added_row, 'is added row')

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

        # print(origin_index, 'is original index')

        # self.clicked_col = index.column()
        # print(self.clicked_row_index, 'clicked')  # Test
        # print(self.getTableCell(self.clicked_row_index))  # Test
        self.on_selected(origin_index)

    def double_click(self):
        index = (self.selectionModel().currentIndex())
        self.double_row = index.row()
        self.double_col = index.column()

        self.current_row = self.getTableCell(self.double_row)

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

                # print(edited_row_index, 'changed')  # Test
                if self.getTableCell(i=edited_row_index, j=self.typeIndex) == ['']:
                    self.setItem(edited_row_index, self.typeIndex, QTableWidgetItem('text'))

                for i in range(self.xminIndex, self.degreeIndex + 1):
                    origin_row[i] = int(origin_row[i])

                origin_index = self.data.index(origin_row)

                # print(origin_index, 'is origin_index')
                # print(edited_row_index,' is edited_row_index')

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
