#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018年6月8日
author: Irony
site: https://pyqt5.com , https://github.com/892768447
email: 892768447@qq.com
file: ProbeWindow
description: 简单探测窗口和放大截图
"""

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QCursor, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
import win32gui


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class FrameWidget(QWidget):
    # 전체 화면 투명 창 

    def __init__(self, *args, **kwargs):
        super(FrameWidget, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()  # 전체 화면 
        self._rect = QRect()  # 감지 된 창의 사각형 위치 

    def setRect(self, x, y, w, h):
        # 업데이트 사각형 상자 
        self._rect.setX(x)
        self._rect.setY(y)
        self._rect.setWidth(w - x)
        self._rect.setHeight(h - y)
        self.update()

    def paintEvent(self, event):
        super(FrameWidget, self).paintEvent(event)
        if self._rect.isValid():  # 画边 
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 4))
            painter.drawRect(self._rect)


class Label(QLabel):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.ismd = False  # 눌렀지? 
        self.setAlignment(Qt.AlignCenter)
        self.setText('鼠标按住不放拖动到外面')
        self.resize(240, 240)
        self.frameWidget = FrameWidget()  # 국경 

    def closeEvent(self, event):
        self.frameWidget.close()
        super(Label, self).closeEvent(event)

    def mousePressEvent(self, event):
        super(Label, self).mousePressEvent(event)
        self.ismd = True  #를 누릅니다 
        # 크로스로 마우스 스타일을 설정하십시오 
        self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        super(Label, self).mouseReleaseEvent(event)
        self.ismd = False
        self.frameWidget.setRect(0, 0, 0, 0)
        # 평범한 마우스 스타일을 설정하십시오 
        self.setCursor(Qt.ArrowCursor)
        self.clear()
        self.setText('鼠标按住不放拖动到外面')

    def mouseMoveEvent(self, event):
        super(Label, self).mouseMoveEvent(event)
        # 화면에서 마우스의 위치를 ​​가져옵니다. 
        pos = self.mapToGlobal(event.pos())
        hwnd = win32gui.WindowFromPoint((pos.x(), pos.y()))
        self.frameWidget.setRect(*win32gui.GetWindowRect(hwnd))
        # 스크린 샷 
        screen = QApplication.primaryScreen()
        if screen is not None:
            image = screen.grabWindow(0,
                                      pos.x() - 60, pos.y() - 60, 120, 120)
            if not image.isNull():
                self.setPixmap(image.scaled(240, 240))

    def paintEvent(self, event):
        super(Label, self).paintEvent(event)
        # 中 の 正 间 十 
        painter = QPainter(self)
        painter.setPen(Qt.red)
        x = int(self.width() / 2)
        y = int(self.height() / 2)
        painter.drawLine(x, 0, x, self.height())
        painter.drawLine(0, y, self.width(), y)
        if self.ismd:
            # 画 坐 坐 标 
            pos = QCursor.pos()
            ret = win32gui.GetPixel(win32gui.GetWindowDC(
                win32gui.GetDesktopWindow()), pos.x(), pos.y())
            r, g, b = ret & 0xff, (ret >> 8) & 0xff, (ret >> 16) & 0xff
            print(r, g, b)
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignLeft |
                             Qt.AlignBottom, '({}, {})\nRGB: ({}, {}, {})\n{}'.format(
                                 pos.x(), pos.y(), r, g, b, QColor(r, g, b).name()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    w = Label()
    w.show()
    sys.exit(app.exec_())
