#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月21日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: Splitter
@description: 
"""
import sys

from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import QTextEdit, QListWidget,\
    QTreeWidget, QSplitter, QApplication, QMainWindow, QSplitterHandle


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"\



class SplitterHandle(QSplitterHandle):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(SplitterHandle, self).__init__(*args, **kwargs)
        #이 설정이 설정되어 있지 않으면 마우스는 누르면 MouseMoveEvent에 응답하여 이동할 수 있습니다. 
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        super(SplitterHandle, self).mousePressEvent(event)
        if event.pos().y() <= 24:
            # 클릭 신호를 보냅니다 
            self.clicked.emit()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        # y 좌표가 24 미만이면 상단의 직사각형 상자 높이입니다. 
        if event.pos().y() <= 24:
            # 取 样 
            self.unsetCursor()
            event.accept()
        else:
            # 기본 마우스 스타일을 설정하고 이동합니다 
            self.setCursor(Qt.SplitHCursor if self.orientation()
                           == Qt.Horizontal else Qt.SplitVCursor)
            super(SplitterHandle, self).mouseMoveEvent(event)

    def paintEvent(self, event):
        # 기본 스타일을 그립니다 
        super(SplitterHandle, self).paintEvent(event)
        # 상단 확장 버튼을 그립니다 
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.red)
        # 画矩 形形 
        painter.drawRect(0, 0, self.width(), 24)
        # 画 三角 
        painter.setBrush(Qt.red)
        painter.drawPolygon(QPolygonF([
            QPointF(0, (24 - 8) / 2),
            QPointF(self.width() - 2, 24 / 2),
            QPointF(0, (24 + 8) / 2)
        ]))


class Splitter(QSplitter):

    def onClicked(self):
        print('clicked')

    def createHandle(self):
        if self.count() == 1:
            # 여기, 첫 번째 분할 스트립 
            handle = SplitterHandle(self.orientation(), self)
            handle.clicked.connect(self.onClicked)
            return handle
        return super(Splitter, self).createHandle()


class SplitterWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SplitterWindow, self).__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle('PyQt Qsplitter')
        textedit = QTextEdit('QTextEdit', self)
        listwidget = QListWidget(self)
        listwidget.addItem("This is  a \nListWidget!")
        treewidget = QTreeWidget()
        treewidget.setHeaderLabels(['This', 'is', 'a', 'TreeWidgets!'])

        splitter = Splitter(self)
        splitter.setHandleWidth(8)
        splitter.addWidget(textedit)
        splitter.addWidget(listwidget)
        splitter.addWidget(treewidget)
        # qt.vertical 수직 qt.Horizontal 레벨 
        splitter.setOrientation(Qt.Horizontal)
        self.setCentralWidget(splitter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SplitterWindow()
    main.show()
    sys.exit(app.exec_())
