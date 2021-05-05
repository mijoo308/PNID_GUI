import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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


        ''' tool bar '''
        self.file_toolbar = self.addToolBar('시작하기')
        self.file_toolbar.addAction(openImgFileAction)
        self.file_toolbar.addAction(folderAction)
        self.file_toolbar.addAction(saveAction)

        self.show()

    def fileOpen(self):
        '''Import file window'''
        self.dialog = QDialog()
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
        # self.dialog.confirm.resize(60, 40)
        self.dialog.confirm.move(500, 250)

        self.dialog.show()

    def dotBtnClick(self):
        FileOpen = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg, *.jpeg, *.png')
        self.dialog.source.setText(FileOpen[0])
        self.dialog.path.append(FileOpen[0])

if __name__ == '__main__':
   app = QApplication(sys.argv)
   mainWindow = MainWindow()
   sys.exit(app.exec_())