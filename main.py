import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
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
        self.file_toolbar.addAction(self.folderAction)
        self.file_toolbar.addAction(self.saveAction)
        self.file_toolbar.addAction(self.dotAction)
        self.file_toolbar.addAction(self.icon1ImgAction)
        self.file_toolbar.addAction(self.preprocessImgAction)
        self.file_toolbar.addAction(self.recogImgAction)

        self.initBoxlayout()
        self.initImgListDock()

    def createActions(self):
        self.openImgFileAction = QAction(QIcon('./icon_img/file.png'), '시작하기')
        self.openImgFileAction.triggered.connect(self.openImgFileDialog)
        self.folderAction = QAction(QIcon('./icon_img/folder.png'), 'folder', self)
        self.saveAction = QAction(QIcon('./icon_img/save.png'), 'save', self)
        self.dotAction = QAction(QIcon('./icon_img/dotted.png'), ' ', self)
        self.icon1ImgAction = QAction(QIcon('./icon_img/icon1.png'), ' ', self)
        self.preprocessImgAction = QAction(QIcon('./Icon_img/pre.png'), '원본도면 전처리')
        self.preprocessImgAction.triggered.connect(self.preprocessImg)
        self.recogImgAction = QAction(QIcon('./Icon_img/cognition.png'), '도면 객체 인식', self)

    def preprocessImg(self):
        self.enableToolBtn()

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
        msgBox = QMessageBox.information(self, 'Information', '알림\n\n최대한 테두리 안쪽 영역을 선택해주십시오.\n(우클릭으로 선택)',
                                         QMessageBox.Ok, QMessageBox.Ok)

    def exceptFieldMessageBox(self):
        QMessageBox.information(self, "Information", '알림\n\n최대한 표제 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                QMessageBox.Ok, QMessageBox.Ok)

    def mapFieldMessageBox(self):
        QMessageBox.information(self, 'Information', '알림\n\n최대한 도면 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                QMessageBox.Ok, QMessageBox.Ok)

    def openImgFileDialog(self):
        self.dialog = QDialog()

        '''Import file window'''
        self.dialog.setWindowTitle('이미지 도면 인식 시작 하기')
        self.dialog.setGeometry(300, 100, 600, 300)
        self.dialog.setFixedSize(600, 300)

        self.dialog.label = QLabel('Source file', self.dialog)
        self.dialog.label.move(20, 10)

        '''Dot Button'''
        self.dialog.dotBtn = QPushButton('...', self.dialog)
        self.dialog.dotBtn.resize(50, 30)
        self.dialog.dotBtn.move(523, 5)
        self.dialog.dotBtn.clicked.connect(self.dotBtnClick)

        '''File Path'''
        self.dialog.source = QLineEdit(self.dialog)
        self.dialog.source.resize(300, 20)
        self.dialog.source.move(225, 10)
        self.dialog.source.setReadOnly(True)
        self.dialog.source.setPlaceholderText('파일 경로')

        self.dialog.path = QTextEdit(self.dialog)
        self.dialog.path.resize(550, 200)
        self.dialog.path.move(20, 40)
        self.dialog.path.append('File Path')

        '''Confirm button'''
        self.dialog.confirm = QPushButton('OK', self.dialog)
        self.dialog.confirm.move(480, 250)

        self.dialog.show()

    def dotBtnClick(self):
        FileOpen = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg, *.jpeg, *.png')
        self.dialog.source.setText(FileOpen[0])
        self.dialog.path.append(FileOpen[0])

    def initBoxlayout(self):  # 다른 img 관련 widget으로 바꿔도 될 것 같음
        widget = QWidget()
        # vbox = initImgList()
        widget.setStyleSheet(  # 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: blue;"
            "border-radius: 3px")

        # Box Layout 설정
        boxlayout = QHBoxLayout(widget)

        boxlayout.addWidget(QLabel('도면View 자리'))

        self.setCentralWidget(widget)

    def initImgListDock(self):
        dockWidgetContent = QWidget()
        dockWidgetContent.setStyleSheet(  # 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: red;"
            "border-radius: 3px")

        self.dockingWidget = QDockWidget("도면 목록")  # 타이틀 설정
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.dockingWidget.setWidget(self.imgListView()) #imgListView()랑 연결
        self.dockingWidget.setFloating(False)  # ? False했는데도 움직여짐,,
        self.dockingWidget.setMinimumSize(int(self.frameGeometry().width() * 0.2), self.frameGeometry().height())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockingWidget)

    def imgListView(self):
        pixmap = QPixmap('./icon_img/save.png')
        pixmap = pixmap.scaled(300, 150)
        img_label = QLabel()
        img_label.setPixmap(pixmap)
        img_name_label = QLabel("Test")
        # label.setAlignment(Qt.AlignTop)
        # label_text.setAlignment(Qt.AlignTop)
        img_name_label.setAlignment(Qt.AlignCenter)

        img_list_view = QWidget()
        box_layout = QVBoxLayout()
        img_list_view.setLayout(box_layout)
        box_layout.addWidget(img_label)
        box_layout.addWidget(img_name_label)
        box_layout.addStretch()
        img_list_view.setStyleSheet(# 레이아웃 확인용
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: red;"
            "border-radius: 3px")

        return img_list_view


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
