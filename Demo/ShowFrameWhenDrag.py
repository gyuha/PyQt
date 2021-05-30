#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月23日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: ShowFrameWhenDrag
@description: 调整窗口显示边框
"""
from ctypes import sizeof, windll, c_int, byref, c_long, c_void_p, c_ulong, c_longlong,\
    c_ulonglong, WINFUNCTYPE, c_uint

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

if sizeof(c_long) == sizeof(c_void_p):
    WPARAM = c_ulong
    LPARAM = c_long
elif sizeof(c_longlong) == sizeof(c_void_p):
    WPARAM = c_ulonglong
    LPARAM = c_longlong

WM_NCLBUTTONDOWN = 0x00a1
GWL_WNDPROC = -4
SPI_GETDRAGFULLWINDOWS = 38
SPI_SETDRAGFULLWINDOWS = 37
WNDPROC = WINFUNCTYPE(c_long, c_void_p, c_uint, WPARAM, LPARAM)

try:
    CallWindowProc = windll.user32.CallWindowProcW
    SetWindowLong = windll.user32.SetWindowLongW
    SystemParametersInfo = windll.user32.SystemParametersInfoW
except:
    CallWindowProc = windll.user32.CallWindowProcA
    SetWindowLong = windll.user32.SetWindowLongA
    SystemParametersInfo = windll.user32.SystemParametersInfoA


def GetDragFullwindows():
    rv = c_int()
    SystemParametersInfo(SPI_GETDRAGFULLWINDOWS, 0, byref(rv), 0)
    return rv.value


def SetDragFullwindows(value):
    SystemParametersInfo(SPI_SETDRAGFULLWINDOWS, value, 0, 0)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('拖动或者调整窗口试试看'))

        # 키 교체 창 처리 
        self._newwndproc = WNDPROC(self._wndproc)
        self._oldwndproc = SetWindowLong(
            int(self.winId()), GWL_WNDPROC, self._newwndproc)

    def _wndproc(self, hwnd, msg, wparam, lparam):
        if msg == WM_NCLBUTTONDOWN:
            # 시스템 자체가 이미 열려 있는지 여부를 확인하십시오 
            isDragFullWindow = GetDragFullwindows()
            if isDragFullWindow != 0:
                # 가상 라인 상자를 엽니 다 
                SetDragFullwindows(0)
                # 系统 本 处理 
                ret = CallWindowProc(
                    self._oldwndproc, hwnd, msg, wparam, lparam)
                # 关 虚 虚 虚 
                SetDragFullwindows(1)
                return ret
        return CallWindowProc(self._oldwndproc, hwnd, msg, wparam, lparam)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
