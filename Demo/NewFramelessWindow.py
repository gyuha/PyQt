#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年4月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: NewFramelessWindow
@description:
"""

from Lib.ui_frameless import Ui_FormFrameless
from PyQt5.QtCore import QTimer, Qt, QEvent, QObject
from PyQt5.QtGui import QWindow, QPainter, QColor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


class FramelessObject(QObject):
    Margins = 3  # 가장자리 여백 
    TitleHeight = 36  # 标 标 高度 
    Widgets = set()  # 无球 集 集 

    @classmethod
    def set_margins(cls, margins):
        cls.Margins = margins

    @classmethod
    def set_title_height(cls, height):
        cls.TitleHeight = height

    @classmethod
    def add_widget(cls, widget):
        cls.Widgets.add(widget)

    @classmethod
    def del_widget(cls, widget):
        if widget in cls.Widgets:
            cls.Widgets.remove(widget)

    def _get_edges(self, pos, width, height):
        """根据坐标获取方向
        :param pos: QPoint
        :param width: int
        :param height: int
        :return: Qt.Edges
        """
        edge = 0
        x, y = pos.x(), pos.y()

        if y <= self.Margins:
            edge |= Qt.TopEdge
        if x <= self.Margins:
            edge |= Qt.LeftEdge
        if x >= width - self.Margins:
            edge |= Qt.RightEdge
        if y >= height - self.Margins:
            edge |= Qt.BottomEdge

        return edge

    def _get_cursor(self, edges):
        """调整鼠标样式
        :param edges: int or None
        :return: Qt.CursorShape
        """
        if edges == Qt.LeftEdge | Qt.TopEdge or edges == Qt.RightEdge | Qt.BottomEdge:
            return Qt.SizeFDiagCursor
        elif edges == Qt.RightEdge | Qt.TopEdge or edges == Qt.LeftEdge | Qt.BottomEdge:
            return Qt.SizeBDiagCursor
        elif edges == Qt.LeftEdge or edges == Qt.RightEdge:
            return Qt.SizeHorCursor
        elif edges == Qt.TopEdge or edges == Qt.BottomEdge:
            return Qt.SizeVerCursor

        return Qt.ArrowCursor

    def is_titlebar(self, pos):
        """判断是否是标题栏
        :param pos: QPoint
        :return: bool
        """
        return pos.y() <= self.TitleHeight

    def moveOrResize(self, window, pos, width, height):
        edges = self._get_edges(pos, width, height)
        if edges:
            if window.windowState() == Qt.WindowNoState:
                window.startSystemResize(edges)
        else:
            if self.is_titlebar(pos):
                window.startSystemMove()

    def eventFilter(self, obj, event):
        if obj.isWindowType():
            # 탑 윈도우 처리 커서 스타일 
            if event.type() == QEvent.MouseMove and obj.windowState() == Qt.WindowNoState:
                obj.setCursor(self._get_cursor(self._get_edges(event.pos(), obj.width(), obj.height())))
            elif event.type() == QEvent.TouchUpdate:
                self.moveOrResize(obj, event.pos(), obj.width(), obj.height())
        elif obj in self.Widgets and isinstance(event, QMouseEvent) and event.button() == Qt.LeftButton:
            if event.type() == QEvent.MouseButtonDblClick:
                # 복원을 최대화하려면 더블 클릭하십시오 
                if self.is_titlebar(event.pos()):
                    if obj.windowState() == Qt.WindowFullScreen:
                        pass
                    elif obj.windowState() == Qt.WindowMaximized:
                        obj.showNormal()
                    else:
                        obj.showMaximized()
            elif event.type() == QEvent.MouseButtonPress:
                self.moveOrResize(obj.windowHandle(), event.pos(), obj.width(), obj.height())

        return False


class FramelessWindow(QWidget, Ui_FormFrameless):

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 무시건 
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        # 복원 버튼을 숨 깁니다 
        self.buttonNormal.setVisible(False)
        # 标题 단추 신호 
        self.buttonMinimum.clicked.connect(self.showMinimized)
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonNormal.clicked.connect(self.showNormal)
        self.buttonClose.clicked.connect(self.close)
        self.setStyleSheet('#widgetTitleBar{background: rgb(232, 232, 232);}')

    def changeEvent(self, event):
        """窗口状态改变
        :param event:
        """
        super(FramelessWindow, self).changeEvent(event)
        # # 时 控制 时 修 时 
        visible = self.isMaximized()
        self.buttonMaximum.setVisible(not visible)
        self.buttonNormal.setVisible(visible)
        if visible:
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            # todo는 UI 파일의 여백 여백과 일치합니다. 
            m = FramelessObject.Margins
            self.layout().setContentsMargins(m, m, m, m)

    def paintEvent(self, event):
        # 透 透 背景 背景 그러나 마우스 캡처를위한 투명성을 남겨 둘 필요가 있습니다. 
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255, 1))


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    if not hasattr(QWindow, 'startSystemMove'):
        QWindow.startSystemResize()
        # 지원하지 않습니다 
        QMessageBox.critical(None, '错误', '当前Qt版本不支持该例子')
        QTimer.singleShot(100, app.quit)
    else:
        # 글로벌 이벤트 필터 설치 
        fo = FramelessObject()
        app.installEventFilter(fo)

        w1 = FramelessWindow()
        fo.add_widget(w1)
        w1.show()

        w2 = FramelessWindow()
        fo.add_widget(w2)
        w2.show()
    sys.exit(app.exec_())
