import sys
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QIcon, QPixmap, QCursor, QPainter,QImage, QPalette
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon, QPixmap, QCursor, QPainter, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QRect

from utils import parseXML


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMainUI()

    def initMainUI(self):
        self.setWindowTitle('도면 인식 프로그램')
        self.move(300, 100)
        self.resize(1600, 800)
        self.statusBar()

        self.createActions()

        self.createMenuBar()
        self.createToolBar()

        #self.createImgListDock() # Dock 없어도 될 것 같음
        self.createImgViewer()

        self.show()


    def createMenuBar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.addMenu('&파일')
        menubar.addMenu('&보기')
        menubar.addMenu('&도구')
        menubar.addMenu('&도움말')

    def createToolBar(self):
        self.file_toolbar = self.addToolBar('시작하기')
        self.file_toolbar.addAction(self.openImgFileAction)
        self.file_toolbar.addAction(self.openXmlFileAction)
        self.file_toolbar.addAction(self.folderAction)
        self.file_toolbar.addAction(self.saveAction)
        self.file_toolbar.addAction(self.dotAction)
        self.file_toolbar.addAction(self.icon1ImgAction)
        self.file_toolbar.addAction(self.preprocessImgAction)
        self.file_toolbar.addAction(self.recogImgAction)

    def createActions(self):
        self.openImgFileAction = QAction(QIcon('./icon_img/file.png'), '시작하기')
        self.openImgFileAction.triggered.connect(self.openFileDialog)
        self.openXmlFileAction = QAction(QIcon('./icon_img/xml.png'), 'xml 파일')
        self.openXmlFileAction.triggered.connect(self.openFileDialog)
        self.folderAction = QAction(QIcon('./icon_img/folder.png'), 'folder', self)
        self.saveAction = QAction(QIcon('./icon_img/save.png'), 'save', self)
        self.dotAction = QAction(QIcon('./icon_img/dotted.png'), ' ', self)
        self.icon1ImgAction = QAction(QIcon('./icon_img/icon1.png'), ' ', self)
        self.preprocessImgAction = QAction(QIcon('./Icon_img/pre.png'), '원본도면 전처리')
        self.preprocessImgAction.triggered.connect(self.preprocessImg)
        self.recogImgAction = QAction(QIcon('./Icon_img/cognition.png'), '도면 객체 인식', self)

    def preprocessImg(self):
        self.enableToolBtn()
        # preprocessImg

    def enableToolBtn(self):
        self.dotAction = QAction(QIcon('./icon_img/dotted.png'), ' ', self)
        self.outlineImgAction = QAction(QIcon('./Icon_img/outline.png'), '외곽선 영역 선택', self)
        self.outlineImgAction.triggered.connect(self.outlineMessageBox)
        self.exceptFieldImgAction = QAction(QIcon('./Icon_img/exceptField.png'), '표제영역 선택', self)
        self.exceptFieldImgAction.triggered.connect(self.exceptFieldMessageBox)
        self.mapFieldImAction = QAction(QIcon('./Icon_img/mapField.png'), '도면영역 선택', self)
        self.mapFieldImAction.triggered.connect(self.mapFieldMessageBox)

        self.file_toolbar.addAction(self.dotAction)
        self.file_toolbar.addAction(self.outlineImgAction)
        self.file_toolbar.addAction(self.exceptFieldImgAction)
        self.file_toolbar.addAction(self.mapFieldImAction)


    def outlineMessageBox(self):
        QMessageBox.information(self, 'Information', '알림\n\n최대한 테두리 안쪽 영역을 선택해주십시오.\n(우클릭으로 선택)',
                                         QMessageBox.Ok, QMessageBox.Ok)

    def exceptFieldMessageBox(self):
        QMessageBox.information(self, "Information", '알림\n\n최대한 표제 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                QMessageBox.Ok, QMessageBox.Ok)

    def mapFieldMessageBox(self):
        QMessageBox.information(self, 'Information', '알림\n\n최대한 도면 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                QMessageBox.Ok, QMessageBox.Ok)

    def openFileDialog(self):
        self.dialog = QDialog()

        '''Import file window'''
        self.dialog.setWindowTitle('이미지 도면 인식 시작 하기')
        self.dialog.setGeometry(300, 100, 600, 300)
        self.dialog.setFixedSize(600, 300)

        self.dialog.imgLabel = QLabel('도면 입력', self.dialog)
        self.dialog.imgLabel.move(20, 10)
        self.dialog.xmlLabel = QLabel('XML 입력', self.dialog)
        self.dialog.xmlLabel.move(20, 35)

        '''Dot Button'''
        self.dialog.dotBtn1 = QPushButton('...', self.dialog)
        self.dialog.dotBtn1.resize(33, 22)
        self.dialog.dotBtn1.move(523, 9)
        self.dialog.dotBtn1.clicked.connect(self.imgDotBtnClick)

        self.dialog.dotBtn2 = QPushButton('...', self.dialog)
        self.dialog.dotBtn2.resize(33, 22)
        self.dialog.dotBtn2.move(523, 34)
        self.dialog.dotBtn2.clicked.connect(self.xmlDotBtnClick)

        '''File Path'''
        self.dialog.imgSource = QLineEdit(self.dialog)
        self.dialog.imgSource.resize(300, 20)
        self.dialog.imgSource.move(225, 10)
        self.dialog.imgSource.setReadOnly(True)
        self.dialog.imgSource.setPlaceholderText('도면 파일 경로')

        self.dialog.xmlSource = QLineEdit(self.dialog)
        self.dialog.xmlSource.resize(300, 20)
        self.dialog.xmlSource.move(225, 35)
        self.dialog.xmlSource.setReadOnly(True)
        self.dialog.xmlSource.setPlaceholderText('XML 파일 경로')

        self.dialog.path = QTextEdit(self.dialog)
        self.dialog.path.resize(550, 180)
        self.dialog.path.move(20, 60)
        self.dialog.path.append('File Path')

        '''Confirm button'''
        self.dialog.confirm = QPushButton('OK', self.dialog)
        self.dialog.confirm.move(480, 250)
        self.dialog.confirm.clicked.connect(self.btnClick)

        self.dialog.show()

    def btnClick(self):
        # imgView = ImgView()
        self.ScrollableImgArea.uploadImg(resize_ratio=1, filePath=self.imgFilePath[0])
        self.dialog.close()
        self.callMappedArea() #테스트 해보려구 넣은 명려문 나중에 다른 곳으로 옮겨야 함

    def callMappedArea(self):
        self.subwindow = mapWindow(img=self.imgFilePath[0], xml=self.xmlFilePath[0])

    def imgDotBtnClick(self):
        self.imgFilePath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg *.jpeg *.png')
        self.dialog.imgSource.setText(self.imgFilePath[0])
        self.dialog.path.append(self.imgFilePath[0])


    def xmlDotBtnClick(self):
        self.xmlFilePath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.xml')
        self.dialog.xmlSource.setText(self.xmlFilePath[0])
        self.dialog.path.append(self.xmlFilePath[0])

    def createImgViewer(self):
        self.ScrollableImgArea = ImgView()
        self.setCentralWidget(self.ScrollableImgArea)

    def createImgListDock(self):
        self.dockingWidget = QDockWidget("도면 목록")  # 타이틀 설정
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.dockingWidget.setMinimumSize(int(self.frameGeometry().width() * 0.2), self.frameGeometry().height())
        self.dockingWidget.setWidget(ImgListView()) #imgListView()랑 연결
        self.dockingWidget.setFloating(False)  # ? False했는데도 움직여짐,,

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockingWidget)

class ImgListView(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.resize(self.frameGeometry().width(), self.frameGeometry().height())

        # empty widget for scrollArea
        self.emptyWidget = QWidget()
        self.setWidget(self.emptyWidget)

        self.box_layout = QVBoxLayout()
        self.setLayout(self.box_layout)
        self.setStyleSheet(# 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: red;"
            "border-radius: 3px")

        # for scroll test
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()
        self.makeImgListElement()

        self.emptyWidget.setLayout(self.box_layout)

    def makeImgListElement(self):
        pixmap = QPixmap('test.jpg') # test
        pixmap = pixmap.scaled(270, 150)
        img_label = QLabel()
        img_label.setPixmap(pixmap)
        img_name_label = QLabel("Test")
        img_name_label.setAlignment(Qt.AlignCenter)

        # layout에 추가
        self.box_layout.addWidget(img_label)
        self.box_layout.addWidget(img_name_label)

        # TODO: element 마지막에 stretch 처리 필요
        # self.box_layout.addStretch()


class ImgView(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        # empty widget for scrollArea
        self.emptyWidget = QWidget()
        self.setWidget(self.emptyWidget)


    def uploadImg(self, resize_ratio, filePath):
        self.pixmap = QPixmap(filePath)
        size = self.pixmap.size()
        self.pixmap.scaled(int(size.width() * resize_ratio), int(size.height() * resize_ratio))
        self.img_label = QLabel()
        self.img_label.setPixmap(self.pixmap)
        self.setWidget(self.img_label)


    def layer(self):
        '''self.img_label.forepalette = QPalette(self.img_lable.palette())
        self.img_label.forepalette.setColor(self.img_label.forepalette.Background, Qt.black)
        self.setPalette(self.img_label.forepalette)
        self.setWidget(self.img_label)'''
        self.layer = QImage(self.img_label.size(), QImage.Format_ARGB32)
        self.layer.fill(Qt.black)

    #def test(self):

class LayerItem(QGraphicsRectItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_pixmap = QPixmap()

    def reset(self, size):
        self.m_pixmap = QPixmap(size)
        self.m_pixmap.fill(Qt.black)

class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))

        self.background_item = QGraphicsPixmapItem()
        #self.foreground_item = LayerItem(self.background_item)
        self.scene().addItem(self.background_item)
        #self.scene().addItem(self.foreground_item)

    def set_image(self, image):
        self.background_item.setPixmap(image) #pixmap 넘겨줘야함
        #self.foreground_item.reset(size=self.background_item.pixmap().size())
        self.centerOn(self.background_item)



class mapWindow(QMainWindow):
    def __init__(self, img, xml):
        super().__init__()
        self.title = img

        self.IMG_PATH = img
        self.XML_PATH = xml

        self.initWindowUi(title=self.title)

    def initWindowUi(self, title):
        self.setWindowTitle(title)
        self.move(100, 100)
        self.resize(1600, 800)

        self.createMenubar()

        self.mapWidget = QWidget()
        self.mapWidget.layout = QHBoxLayout()
        #self.mapWidget.viewLayout = QVBoxLayout()
        self.mapWidget.setLayout(self.mapWidget.layout)
        self.mappedAreaViewr()

        self.mapWidget.mlayer = QImage(self.mappedArea.img_label.size(), QImage.Format_ARGB32)
        self.mapWidget.mlayer.fill(Qt.black)


        self.layer = over_layer(self.mappedArea)
        rect = QRect(self.mappedArea.x(), self.mappedArea.y(), self.mappedArea.width(), self.mappedArea.height())
        self.layer.layerSetting(size=rect)
        self.layer.setVisible(True)


        self.tabView()
        self.createDock(self.tabview)

        self.setCentralWidget(self.mapWidget)

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
        self.mappedArea.uploadImg(resize_ratio=0.2, filePath=self.IMG_PATH)
        self.mapWidget.layout.addWidget(self.mappedArea)

        '''self.view = GraphicsView()
        self.pixmap = QPixmap(self.IMG_PATH)
        self.view.set_image(self.pixmap)

        self.mapWidget.viewLayout.addWidget(self.view)
        self.mapWidget.layout.addLayout(self.mapWidget.viewLayout)'''


    def createDock(self, connectedWidget):
        self.dockingWidget = QDockWidget("XML Result")  # 타이틀 설정
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.dockingWidget.setMinimumSize(int(self.frameGeometry().width() * 0.3), self.frameGeometry().height())
        self.dockingWidget.setWidget(connectedWidget)
        self.dockingWidget.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dockingWidget)


    def tabView(self):
        self.tabview = QWidget()

        # self.scrollableTabArea = QScrollArea()
        # self.scrollableTabArea.setWidget(self.tabview)

        self.tabview.tabLayout = QVBoxLayout()
        self.tabview.tabs = QTabWidget()

        self.tabview.tab1 = QWidget()
        self.createTab1UI(self.XML_PATH)

        self.tabview.tab2 = QWidget()

        self.tabview.tabs.resize(int(self.width() * 0.2), int(self.height()))

        self.tabview.tabs.addTab(self.tabview.tab1, 'Labeled Objects')
        self.tabview.tabs.addTab(self.tabview.tab2, 'Recognized Objects')

        self.tabview.tabLayout.addWidget(self.tabview.tabs)
        self.tabview.setLayout(self.tabview.tabLayout)


    def createTab1UI(self, xml_path):

        self.tabview.tab1.layout = QHBoxLayout()

        '''XML Parsing'''
        result = parseXML(xml_path, type='res')
        table_size = len(result)

        '''Table'''
        self.tabview.tab1.table = QTableWidget()
        self.tabview.tab1.table.setRowCount(table_size)
        self.tabview.tab1.table.setColumnCount(8)
        self.tabview.tab1.table.setHorizontalHeaderLabels(["v", "type", "text", "xmin", "ymin", "xmax", "ymax", "orientation"])
        self.tabview.tab1.layout.addWidget(self.tabview.tab1.table)
        self.tabview.tab1.setLayout(self.tabview.tab1.layout)

        '''check box'''
        self.tabview.tab1.checkBoxList = []
        for i in range(table_size):
            ckbox = QCheckBox()
            self.tabview.tab1.checkBoxList.append(ckbox)
        for i in range(table_size):
            self.tabview.tab1.table.setCellWidget(i, 0, self.tabview.tab1.checkBoxList[i])

            # result 순서 string, orientation, xmin, ymin, xmax, ymax
            self.tabview.tab1.table.setItem(i, 2, QTableWidgetItem(result[i][0]))
            self.tabview.tab1.table.setItem(i, 3, QTableWidgetItem(result[i][2]))
            self.tabview.tab1.table.setItem(i, 4, QTableWidgetItem(result[i][3]))
            self.tabview.tab1.table.setItem(i, 5, QTableWidgetItem(result[i][4]))
            self.tabview.tab1.table.setItem(i, 6, QTableWidgetItem(result[i][5]))
            self.tabview.tab1.table.setItem(i, 7, QTableWidgetItem(result[i][1]))

        self.tabview.tab1.table.setColumnWidth(0, 5)

    def updateTab1(self):
        header = self.tabview.tab1.table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)


class over_layer(QWidget):
    def __init__(self, parent=None):
        super(over_layer, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.black)

        self.setPalette(palette)

    def layerSetting(self, size):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #painter.fillRect(event.rect(), QBrush(QColor(1, 1, 1, 100)))
        painter.fillRect(size, QBrush(QColor(1, 1, 1, 100)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
