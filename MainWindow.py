# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect

from MappedWindow import *
from ImgView import *
from ImgListView import *
import editMap
import subprocess
# import testSrc.run_easyTess

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

        # self.createImgListDock() # Dock 없어도 될 것 같음
        #self.createImgViewer()

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
        self.openImgFileAction.triggered.connect(self.openImgDialog)
        self.openXmlFileAction = QAction(QIcon('./icon_img/xml.png'), 'xml 파일')
        self.openXmlFileAction.triggered.connect(self.openFileDialog)
        self.folderAction = QAction(QIcon('./icon_img/folder.png'), 'folder', self)
        self.saveAction = QAction(QIcon('./icon_img/save.png'), 'save', self)
        self.saveAction.triggered.connect(self.save_file)
        self.dotAction = QAction(QIcon('./icon_img/dotted.png'), ' ', self)
        self.icon1ImgAction = QAction(QIcon('./icon_img/icon1.png'), ' ', self)
        self.preprocessImgAction = QAction(QIcon('./Icon_img/pre.png'), '원본도면 전처리')
        self.preprocessImgAction.triggered.connect(self.preprocessImg)
        self.recogImgAction = QAction(QIcon('./Icon_img/cognition.png'), '도면 객체 인식')
        self.recogImgAction.triggered.connect(self.recogImg)

    def save_file(self):
        label = QLabel()
        label.setPixmap(self.imgArea.scene.mapImg)
        fileSave = QFileDialog.getSaveFileName(label, 'Save Image', '', 'PNG(*.png)')
        if fileSave[0]:
            self.imgArea.scene.mapImg.save(fileSave[0])


    def recogImg(self):
        recog_img_name = os.path.basename(self.imgFilePath[0])
        recog_img_path = os.path.join('./data', recog_img_name)
        self.imgArea.scene.mapImg.save(recog_img_path)

        exec(open('./testSrc/run_easyTess.py', encoding="utf-8").read())

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
        self.imgArea.selectActivate(flag='outline', state=True)

    def exceptFieldMessageBox(self):
        if self.imgArea.scene.ready:
            QMessageBox.information(self, "Information", '알림\n\n최대한 표제 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                    QMessageBox.Ok, QMessageBox.Ok)
            self.imgArea.selectActivate(flag='except', state=True)
        elif not self.imgArea.scene.ready:
            QMessageBox.warning(self, 'Warning', 'Warning\n\n외곽 영역을 먼저 선택해주십시오.', QMessageBox.Ok, QMessageBox.Ok)

    def mapFieldMessageBox(self):
        QMessageBox.information(self, 'Information', '알림\n\n최대한 도면 영역만을 선택해주십시오.\n(우클릭으로 선택)',
                                QMessageBox.Ok, QMessageBox.Ok)

    def openImgDialog(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('도면 인식 시작하기')
        self.dialog.setGeometry(300, 100, 600, 300)
        self.dialog.setFixedSize(600, 300)

        self.dialog.imgLabel = QLabel('도면 입력', self.dialog)
        self.dialog.imgLabel.move(20, 10)

        '''Dot Button'''
        self.dialog.dotBtn1 = QPushButton('...', self.dialog)
        self.dialog.dotBtn1.resize(33, 22)
        self.dialog.dotBtn1.move(523, 9)
        self.dialog.dotBtn1.clicked.connect(self.imgDotBtnClick)

        '''File Path'''
        self.dialog.imgSource = QLineEdit(self.dialog)
        self.dialog.imgSource.resize(300, 20)
        self.dialog.imgSource.move(225, 10)
        self.dialog.imgSource.setReadOnly(True)
        self.dialog.imgSource.setPlaceholderText('도면 파일 경로')

        self.dialog.path = QTextEdit(self.dialog)
        self.dialog.path.resize(550, 180)
        self.dialog.path.move(20, 60)
        self.dialog.path.append('File Path')

        '''Confirm button'''
        self.dialog.confirm = QPushButton('OK', self.dialog)
        self.dialog.confirm.move(480, 250)
        self.dialog.confirm.clicked.connect(self.imgOkBtnClick)

        self.dialog.show()

    def openFileDialog(self):
        self.dialog = QDialog()

        '''Import file window'''
        self.dialog.setWindowTitle('xml 수정하기')
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
        self.dialog.confirm.clicked.connect(self.xmlOkBtnClick)

        self.dialog.show()

    def xmlOkBtnClick(self):
        # imgView = ImgView()
        # self.ScrollableImgArea.uploadImg(resize_ratio=0.2, filePath=self.imgFilePath[0])
        self.createImgViewer()
        self.dialog.close()
        self.callMappedArea()  # 테스트 해보려구 넣은 명려문 나중에 다른 곳으로 옮겨야 함

    def imgOkBtnClick(self):
        self.createImgViewer()
        self.dialog.close()

    def callMappedArea(self):
        self.subwindow = MappedWindow(img=self.imgFilePath[0], xml=self.xmlFilePath[0])

    def imgDotBtnClick(self):
        self.imgFilePath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg *.jpeg *.png')
        self.dialog.imgSource.setText(self.imgFilePath[0])
        self.dialog.path.append(self.imgFilePath[0])

    def xmlDotBtnClick(self):
        self.xmlFilePath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.xml')
        self.dialog.xmlSource.setText(self.xmlFilePath[0])
        self.dialog.path.append(self.xmlFilePath[0])

    def createImgViewer(self):
        #self.ScrollableImgArea = ImgView()
        self.imgArea = editMap.graphicsView(self.imgFilePath[0])
        self.setCentralWidget(self.imgArea)

    def createImgListDock(self):
        self.dockingWidget = QDockWidget("도면 목록")  # 타이틀 설정
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.dockingWidget.setMinimumSize(int(self.frameGeometry().width() * 0.2), self.frameGeometry().height())
        self.dockingWidget.setWidget(ImgListView())  # imgListView()랑 연결
        self.dockingWidget.setFloating(False)  # ? False했는데도 움직여짐,,

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockingWidget)



