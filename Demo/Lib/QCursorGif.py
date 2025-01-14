#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020年3月13日
@author: Irony
@site: https://pyqt.site https://github.com/892768447
@email: 892768447@qq.com
@file: Demo.Lib.QCursorGif
@description: 
"""
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020'
__Version__ = 1.0


class QCursorGif:

    def initCursor(self, cursors, parent=None):
        # 기본 커서를 녹화하십시오 
        self._oldCursor = Qt.ArrowCursor
        self.setOldCursor(parent)
        # 커서 사진로드 
        self._cursorImages = [
            QCursor(QPixmap(cursor)) for cursor in cursors]
        self._cursorIndex = 0
        self._cursorCount = len(self._cursorImages) - 1
        # 새로 고침 타이머를 만듭니다 
        self._cursorTimeout = 200
        self._cursorTimer = QTimer(parent)
        self._cursorTimer.timeout.connect(self._doBusy)

    def _doBusy(self):
        if self._cursorIndex > self._cursorCount:
            self._cursorIndex = 0
        QApplication.instance().setOverrideCursor(
            self._cursorImages[self._cursorIndex])
        self._cursorIndex += 1

    def startBusy(self):
        if not self._cursorTimer.isActive():
            self._cursorTimer.start(self._cursorTimeout)

    def stopBusy(self):
        self._cursorTimer.stop()
        QApplication.instance().setOverrideCursor(self._oldCursor)

    def setCursorTimeout(self, timeout):
        self._cursorTimeout = timeout

    def setOldCursor(self, parent=None):
        self._oldCursor = (parent.cursor() or Qt.ArrowCursor) if parent else (
            QApplication.instance().overrideCursor() or Qt.ArrowCursor)
