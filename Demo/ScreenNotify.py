#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/4/13
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: ScreenNotify
@description: 屏幕、分辨率、DPI变化通知
"""
import sys

from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, qApp


class Window(QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.appendPlainText('修改分辨率后查看')
        # 마지막 값을 기록하십시오 (슬롯 줄이기). 
        self.m_rect = QRect()
        # 타이머를 사용하여 트리거 마지막 변경 지연 
        self.m_timer = QTimer(self, timeout=self.onSolutionChanged)
        self.m_timer.setSingleShot(True)  # ** 중요 ** 보증 다중 신호가 작은 통화 기능으로 

        # 주로 다중 화면 -> 화면 없음 -> 화면이있는 
        qApp.primaryScreenChanged.connect(lambda _: self.m_timer.start(1000))
        # 다른 신호는 결국이 신호를 호출합니다 
        qApp.primaryScreen().virtualGeometryChanged.connect(lambda _: self.m_timer.start(1000))
        #dpi 변경 
        qApp.primaryScreen().logicalDotsPerInchChanged.connect(lambda _: self.m_timer.start(1000))

    def onSolutionChanged(self):
        # 홈 화면을 얻으십시오 
        screen = qApp.primaryScreen()
        if self.m_rect == screen.availableVirtualGeometry():
            return
        self.m_rect = screen.availableVirtualGeometry()
        # 모든 화면을 사용할 수 있습니다 
        self.appendPlainText('\navailableVirtualGeometry: {0}'.format(str(screen.availableVirtualGeometry())))
        # 모든 화면을 얻으십시오 
        screens = qApp.screens()
        for screen in screens:
            self.appendPlainText(
                'screen: {0}, geometry({1}), availableGeometry({2}), logicalDotsPerInch({3}), '
                'physicalDotsPerInch({4}), refreshRate({5})'.format(
                    screen.name(), screen.geometry(), screen.availableGeometry(), screen.logicalDotsPerInch(),
                    screen.physicalDotsPerInch(), screen.refreshRate()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
