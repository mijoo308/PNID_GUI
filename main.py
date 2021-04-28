import sys
from PyQt5.QtWidgets import QApplication, QApplication, QMainWindow, QAction, qApp, QToolBar
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
        folderAction = QAction(QIcon('./icon_img/folder.png'), 'folder', self)
        saveAction = QAction(QIcon('./icon_img/save.png'), 'save', self)


        ''' tool bar '''
        self.file_toolbar = self.addToolBar('시작하기')
        self.file_toolbar.addAction(openImgFileAction)
        self.file_toolbar.addAction(folderAction)
        self.file_toolbar.addAction(saveAction)


        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   mainWindow = MainWindow()
   sys.exit(app.exec_())