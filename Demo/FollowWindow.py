#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: FollowWindow
@description: 跟随外部窗口
"""
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import win32gui


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('test', self))
        self.tmpHwnd = None
        #TOOT 타이머는 메모장의 위치 크기와 폐쇄 여부를 감지합니다. 
        self.checkTimer = QTimer(self, timeout=self.checkWindow)
        self.checkTimer.start(10)  # 10 밀리 초 부드럽습니다 

    def checkWindow(self):
        # 查 找 
        hwnd = win32gui.FindWindow('Notepad', None)
        if self.tmpHwnd and not hwnd:
            # 表示 记 记 记 
            self.checkTimer.stop()
            self.close()  # 너 자신을 닫으십시오 
            return
        if not hwnd:
            return
        self.tmpHwnd = hwnd
        # 获取 位置 
        rect = win32gui.GetWindowRect(hwnd)
        print(rect)
        self.move(rect[2], rect[1])


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    # 첫 번째 탐지가 열리기위한 메모장이있는 경우 
    hwnd = win32gui.FindWindow('Notepad', None)
    print('hwnd', hwnd)
    if not hwnd:
        # 启 记 记事. 
        os.startfile('notepad')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
