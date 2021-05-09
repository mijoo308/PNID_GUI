import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMainUI()

    def initMainUI(self):
        self.setWindowTitle('도면 인식 프로그램')
        self.move(300, 100)
        self.resize(1600, 800)
        self.statusBar()

        ''' menu bar '''
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.addMenu('&파일')
        menubar.addMenu('&보기')
        menubar.addMenu('&도구')
        menubar.addMenu('&도움말')

        ''' Actions '''
        openImgFileAction = QAction(QIcon('./icon_img/file.png'), '시작하기', self)
        openImgFileAction.triggered.connect(self.fileOpen)
        folderAction = QAction(QIcon('./icon_img/folder.png'), 'folder', self)
        saveAction = QAction(QIcon('./icon_img/save.png'), 'save', self)
        dotAction = QAction(QIcon('./icon_img/dotted.png'), ' ', self)
        icon1Img = QAction(QIcon('./icon_img/icon1.png'), ' ', self)
        preImgAction = QAction(QIcon('./Icon_img/pre.png'), '원본도면 전처리', self)
        preImgAction.triggered.connect(self.addTool)
        cogImgAction = QAction(QIcon('./Icon_img/cognition.png'), '도면 객체 인식', self)

        ''' tool bar '''
        self.file_toolbar = self.addToolBar('시작하기')
        self.file_toolbar.addAction(openImgFileAction)
        self.file_toolbar.addAction(folderAction)
        self.file_toolbar.addAction(saveAction)
        self.file_toolbar.addAction(dotAction)
        self.file_toolbar.addAction(icon1Img)
        self.file_toolbar.addAction(preImgAction)
        self.file_toolbar.addAction(cogImgAction)

        self.initBoxlayout()

        self.show()

    def addTool(self):
        dotAction = QAction(QIcon('./icon_img/dotted.png'), ' ', self)
        outlineImgAction = QAction(QIcon('./Icon_img/outline.png'), '외곽선 영역 선택', self)
        outlineImgAction.triggered.connect(self.outlineMessageBox)
        exceptFieldImgAction = QAction(QIcon('./Icon_img/exceptField.png'), '표제영역 선택', self)
        exceptFieldImgAction.triggered.connect(self.exceptFieldMessageBox)
        mapFieldImAction = QAction(QIcon('./Icon_img/mapField.png'), '도면영역 선택', self)
        mapFieldImAction.triggered.connect(self.mapFieldMessageBox)

        self.file_toolbar.addAction(dotAction)
        self.file_toolbar.addAction(outlineImgAction)
        self.file_toolbar.addAction(exceptFieldImgAction)
        self.file_toolbar.addAction(mapFieldImAction)

    def outlineMessageBox(self):
        msgBox = QMessageBox.information(self, 'Information', '알림\n\n최대한 테두리 안쪽 영역을 선택해주십시오.\n(우클릭으로 선택)',
                                     QMessageBox.Ok, QMessageBox.Ok)

    def exceptFieldMessageBox(self):
        QMessageBox.information(self, "Information", '알림\n\n최대한 표제 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                    QMessageBox.Ok, QMessageBox.Ok)

    def mapFieldMessageBox(self):
        QMessageBox.information(self, 'Information', '알림\n\n최대한 도면 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                    QMessageBox.Ok, QMessageBox.Ok)
        

    def fileOpen(self):
        self.dialog = QDialog()

        '''Import file window'''
        self.dialog.setWindowTitle('이미지 도면 인식 시작 하기')
        self.dialog.setGeometry(300, 100, 600, 300)

        self.dialog.label = QLabel('Source file', self.dialog)
        self.dialog.label.move(20, 10)

        '''Dot Button'''
        self.dialog.dotBtn = QPushButton('...', self.dialog)
        self.dialog.dotBtn.resize(50, 30)
        self.dialog.dotBtn.move(520, 5)
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

    def initBoxlayout(self):

        widget = QWidget()
        # vbox = initImgList()
        widget.setStyleSheet(
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: blue;"
                      "border-radius: 3px")


        # QGridLayout 설정
        boxlayout = QHBoxLayout(widget)

        boxlayout.addLayout(self.initImgList(), 1)  # 레이아웃의 왼쪽

        boxlayout.addWidget(QLabel('도면View 자리'),4)   # 레이아웃의 오른쪽

        self.setCentralWidget(widget)

    def initImgList(self):
        label = QLabel('도면목록 자리')

        vbox = QVBoxLayout()
        # vbox.addStretch(1)

        vbox.addWidget(label)
        return vbox

if __name__ == '__main__':
   app = QApplication(sys.argv)
   mainWindow = MainWindow()
   sys.exit(app.exec_())