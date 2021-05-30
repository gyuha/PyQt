#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Created on 2018年8月2日
author: Irony
site: https://pyqt5.com , https://github.com/892768447
email: 892768447@qq.com
file: win无边框调整大小
description:
"""

from ctypes.wintypes import POINT
import ctypes.wintypes

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWinExtras import QtWin
import win32api
import win32con
import win32gui


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved",      POINT),
        ("ptMaxSize",       POINT),
        ("ptMaxPosition",   POINT),
        ("ptMinTrackSize",  POINT),
        ("ptMaxTrackSize",  POINT),
    ]


class Window(QWidget):

    BorderWidth = 5

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 主 主 可 大 (작업 표시 줄 제거) 
        self._rect = QApplication.instance().desktop().availableGeometry(self)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)
        # 얇은 국경을 늘리십시오 
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

        if QtWin.isCompositionEnabled():
            # 加 er 边 边 阴 shadow. 
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

    def nativeEvent(self, eventType, message):
        retval, result = super(Window, self).nativeEvent(eventType, message)
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # 마우스 이동의 좌표를 얻으십시오 
            x = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            y = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            # : 마우스 위치에서 다른 컨트롤을 수행하십시오 
            if self.childAt(x, y) != None:
                return retval, result
            if msg.message == win32con.WM_NCCALCSIZE:
                # 시스템 상단을 표시하지 않는 테두리를 가로 챌 수 있습니다. 
                return True, 0
            if msg.message == win32con.WM_GETMINMAXINFO:
                # 창 위치가 변경되거나 크기가 변경되면 # 메시지를 끕니다. 
                info = ctypes.cast(
                    msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                # 최대 창 크기 수정 메인 화면의 사용 가능한 크기입니다. 
                info.ptMaxSize.x = self._rect.width()
                info.ptMaxSize.y = self._rect.height()
                # x를 수정하십시오. 배치 점의 y 좌표가 0, 0입니다. 
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0
            if msg.message == win32con.WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth
                # 上 上 上 上 
                if (lx and ty):
                    return True, win32con.HTTOPLEFT
                # 一 右 下角 
                if (rx and by):
                    return True, win32con.HTBOTTOMRIGHT
                오른쪽 상단 구석에 # 카운트 다운 
                if (rx and ty):
                    return True, win32con.HTTOPRIGHT
                # 下 下 
                if (lx and by):
                    return True, win32con.HTBOTTOMLEFT
                # 
                if ty:
                    return True, win32con.HTTOP
                # 
                if by:
                    return True, win32con.HTBOTTOM
                # 왼쪽 
                if lx:
                    return True, win32con.HTLEFT
                # 
                if rx:
                    return True, win32con.HTRIGHT
                # 标题 
                return True, win32con.HTCAPTION
        return retval, result


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    btn = QPushButton('exit', w, clicked=app.quit)
    btn.setGeometry(10, 10, 100, 40)
    w.show()
    sys.exit(app.exec_())
