import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QPainter
from PyQt5.QtCore import Qt


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
        self.dialog.dotBtn1.resize(50, 30)
        self.dialog.dotBtn1.move(523, 5)
        self.dialog.dotBtn1.clicked.connect(self.imgDotBtnClick)

        self.dialog.dotBtn2 = QPushButton('...', self.dialog)
        self.dialog.dotBtn2.resize(50, 30)
        self.dialog.dotBtn2.move(523, 30)
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
        self.ScrollableImgArea.uploadImg(resize_ratio=1, filePath=self.FileOpen[0])
        self.dialog.close()
        self.callMappedArea() #테스트 해보려구 넣은 명려문 나중에 다른 곳으로 옮겨야 함

    def callMappedArea(self):
        self.subwindow = mapWindow(title=self.FileOpen[0])

    def imgDotBtnClick(self):
        self.FileOpen = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg, *.jpeg, *.png')
        self.dialog.imgSource.setText(self.FileOpen[0])
        self.dialog.path.append(self.FileOpen[0])

    def xmlDotBtnClick(self):
        FileOpen = QFileDialog.getOpenFileName(self, '열기', './', filter='*.xml')
        self.dialog.xmlSource.setText(FileOpen[0])
        self.dialog.path.append(FileOpen[0])

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
        pixmap = QPixmap('test.jpg')
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
        #self.filePath = filePath

    def uploadImg(self, resize_ratio, filePath):
        pixmap = QPixmap(filePath)
        size = pixmap.size()
        pixmap = pixmap.scaled(int(size.width() * resize_ratio), int(size.height() * resize_ratio))
        img_label = QLabel()
        img_label.setPixmap(pixmap)
        self.setWidget(img_label)


class mapWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        
        self.initWindowUi(title=self.title)

    def initWindowUi(self, title):
        self.setWindowTitle(title)
        self.move(100, 100)
        self.resize(1100, 800)
        self.createMenubar()

        self.mapWidget = QWidget()
        self.mapWidget.layout = QHBoxLayout()
        self.mapWidget.setLayout(self.mapWidget.layout)

        self.setCentralWidget(self.mappedAreaViewr())
        self.setCentralWidget(self.tabView())

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
        mappedArea = ImgView()
        #mappedArea.resize(800, 100) 사이즈 조절이 안됨,,,ㅠ
        #ratio = mappedArea.width() * 0.8 안됨,,
        mappedArea.uploadImg(resize_ratio=0.8, filePath=self.title)
        self.mapWidget.layout.addWidget(mappedArea)

    def tabView(self):
        self.tabview = QWidget()

        self.tabview.tabLayout = QVBoxLayout()
        self.tabview.tabs = QTabWidget()

        self.tabview.tab1 = QWidget()
        self.tab1UI()

        self.tabview.tab2 = QWidget()

        # size 변경도 안되는 것 같아서 슬픔,,,
        self.tabview.tabs.resize(int(self.width() * 0.2), int(self.height()))

        self.tabview.tabs.addTab(self.tabview.tab1, 'Labeled Objects')
        self.tabview.tabs.addTab(self.tabview.tab2, 'Recognized Objects')

        self.tabview.tabLayout.addWidget(self.tabview.tabs)
        self.tabview.setLayout(self.tabview.tabLayout)

        self.mapWidget.layout.addWidget(self.tabview)

    def tab1UI(self):

        self.tabview.tab1.layout = QHBoxLayout()
        '''Table'''
        self.tabview.tab1.table = QTableWidget()
        self.tabview.tab1.table.setRowCount(5)
        self.tabview.tab1.table.setColumnCount(5)
        self.tabview.tab1.table.setHorizontalHeaderLabels(["v", "id", "type", "class", "xml"])
        self.tabview.tab1.layout.addWidget(self.tabview.tab1.table)
        self.tabview.tab1.setLayout(self.tabview.tab1.layout)
        '''check box'''
        self.tabview.tab1.checkBoxList = []
        for i in range(5):
            ckbox = QCheckBox()
            self.tabview.tab1.checkBoxList.append(ckbox)
        for i in range(5):
            self.tabview.tab1.table.setCellWidget(i, 0, self.tabview.tab1.checkBoxList[i])

        self.tabview.tab1.table.setColumnWidth(0, 15)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
