#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月1日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: EmbedWindow
@description: 嵌入外部窗口
"""

__Author__ = 'By: Irony\nQQ: 892768447\nEmail: 892768447@qq.com'
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0

import win32con
import win32gui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, \
    QLabel


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        self.myhwnd = int(self.winId())  # 自己 的 手柄. 

        layout.addWidget(QPushButton('获取所有可用、可视窗口', self,
                                     clicked=self._getWindowList, maximumHeight=30))
        layout.addWidget(QPushButton('释放窗口', clicked=self.releaseWidget, maximumHeight=30))
        layout.addWidget(
            QLabel('双击列表中的项目则进行嵌入目标窗口到下方\n格式为：句柄|父句柄|标题|类名', self, maximumHeight=30))
        self.windowList = QListWidget(
            self, itemDoubleClicked=self.onItemDoubleClicked, maximumHeight=200)
        layout.addWidget(self.windowList)

    def releaseWidget(self):
        """释放窗口"""
        if self.layout().count() == 5:
            self.restore()
            self._getWindowList()

    def closeEvent(self, event):
        """窗口关闭"""
        self.releaseWidget()
        super(Window, self).closeEvent(event)

    def _getWindowList(self):
        """清空原来的列表"""
        self.windowList.clear()
        win32gui.EnumWindows(self._enumWindows, None)

    def onItemDoubleClicked(self, item):
        """列表双击选择事件"""
        # 첫 번째 항목을 제거하십시오 
        self.windowList.takeItem(self.windowList.indexFromItem(item).row())
        hwnd, phwnd, _, _ = item.text().split('|')
        # 시작을 시작합니다 
        self.releaseWidget()
        hwnd, phwnd = int(hwnd), int(phwnd)
        # 이전 속성을 포함시킵니다 
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        wrect = win32gui.GetWindowRect(hwnd)[:2] + win32gui.GetClientRect(hwnd)[2:]
        print('save', hwnd, style, exstyle, wrect)

        widget = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
        widget.hwnd = hwnd  # 手 句 
        widget.phwnd = phwnd  #flial 창 핸들 
        widget.style = style  # 창 스타일 
        widget.exstyle = exstyle  # 样 
        widget.wrect = wrect  # 位置 位置 
        self.layout().addWidget(widget)

        widget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        win32gui.SetParent(hwnd, int(self.winId()))

    def restore(self):
        """归还窗口"""
        # 버그가 있고 WS_VISIBLE 스타일이없는 창을 반환합니다. 
        widget = self.layout().itemAt(4).widget()
        hwnd, phwnd, style, exstyle, wrect = widget.hwnd, widget.phwnd, widget.style, widget.exstyle, widget.wrect
        print('restore', hwnd, phwnd, style, exstyle, wrect)
        widget.close()
        self.layout().removeWidget(widget)  # 레이아웃에서 # 
        widget.deleteLater()

        win32gui.SetParent(hwnd, phwnd)  # 부모 창으로 돌아가십시오 
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style | win32con.WS_VISIBLE)  # 스타일 복원 
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle)  # 스타일 복원 
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # 显示 显示 口 
        win32gui.SetWindowPos(hwnd, 0, wrect[0], wrect[1], wrect[2], wrect[3], win32con.SWP_NOACTIVATE)

    def _enumWindows(self, hwnd, _):
        """遍历回调函数"""
        if hwnd == self.myhwnd:
            return  # 자신을 삽입하지 못하게하십시오 
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            phwnd = win32gui.GetParent(hwnd)
            title = win32gui.GetWindowText(hwnd)
            name = win32gui.GetClassName(hwnd)
            self.windowList.addItem(
                '{0}|{1}|\t标题：{2}\t|\t类名：{3}'.format(hwnd, phwnd, title, name))


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='txt')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
