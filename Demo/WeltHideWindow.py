#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月1日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: WeltHideWindow
@description: 简单的窗口贴边隐藏
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


__Author__ = 'By: Irony\nQQ: 892768447\nEmail: 892768447@qq.com'
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class WeltHideWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(WeltHideWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.resize(800, 600)
        self._width = QApplication.desktop().availableGeometry(self).width()
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("닫기", self, clicked=self.close))

    def mousePressEvent(self, event):
        '''鼠标按下事件，需要记录下坐标self._pos 和 是否可移动self._canMove'''
        super(WeltHideWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._pos = event.globalPos() - self.pos()
            # 창이 최대화되거나 전체 화면이 발생합니다
            self._canMove = not self.isMaximized() or not self.isFullScreen()

    def mouseMoveEvent(self, event):
        '''鼠标移动事件，动态调整窗口位置'''
        super(WeltHideWindow, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton and self._canMove:
            self.move(event.globalPos() - self._pos)

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件，这个时候需要判断窗口的左边是否符合贴到左边，顶部，右边一半'''
        super(WeltHideWindow, self).mouseReleaseEvent(event)
        self._canMove = False
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            # 왼쪽 숨기기
            return self.move(1 - self.width(), y)
        if y < 0:
            # 꼭대기에 숨겨진 것
            return self.move(x, 1 - self.height())
        if x > self._width - self.width() / 2:  # 口 进 进 一
            # 오른쪽에 숨어 있습니다
            return self.move(self._width - 1, y)

    def enterEvent(self, event):
        '''鼠标进入窗口事件，用于弹出显示窗口'''
        super(WeltHideWindow, self).enterEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            return self.move(0, y)
        if y < 0:
            return self.move(x, 0)
        if x > self._width - self.width() / 2:
            return self.move(self._width - self.width(), y)

    def leaveEvent(self, event):
        '''鼠标离开事件，如果原先窗口已经隐藏，并暂时显示，此时离开后需要再次隐藏'''
        super(WeltHideWindow, self).leaveEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x == 0:
            return self.move(1 - self.width(), y)
        if y == 0:
            return self.move(x, 1 - self.height())
        if x == self._width - self.width():
            return self.move(self._width - 1, y)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = WeltHideWindow()
    w.show()
    sys.exit(app.exec_())
