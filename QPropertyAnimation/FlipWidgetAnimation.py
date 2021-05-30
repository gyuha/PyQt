#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: 翻转动画
@description: 
"""
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QStackedWidget, QLabel

from Lib.FlipWidget import FlipWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class LoginWidget(QLabel):
    # 只 显示 로그인 인터페이스 표시 스크린 샷 

    windowClosed = pyqtSignal()
    windowChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(LoginWidget, self).__init__(*args, **kwargs)
        self.setPixmap(QPixmap('Data/1.png'))

    def mousePressEvent(self, event):
        super(LoginWidget, self).mousePressEvent(event)
        pos = event.pos()
        if pos.y() <= 40:
            if pos.x() > self.width() - 30:
                # 버튼이 닫힌 곳을 클릭하십시오. 
                self.windowClosed.emit()
            elif self.width() - 90 <= pos.x() <= self.width() - 60:
                # 핸드 오버 버튼을 클릭하십시오 
                self.windowChanged.emit()


class SettingWidget(QLabel):
    # 只 是 设置 设置 设置 设置 스크린 샷 

    windowClosed = pyqtSignal()
    windowChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(SettingWidget, self).__init__(*args, **kwargs)
        self.setPixmap(QPixmap('Data/2.png'))

    def mousePressEvent(self, event):
        super(SettingWidget, self).mousePressEvent(event)
        pos = event.pos()
        if pos.y() >= self.height() - 30:
            if self.width() - 95 <= pos.x() <= self.width() - 10:
                # 핸드 오버 버튼을 클릭하십시오 
                self.windowChanged.emit()
        elif pos.y() <= 40:
            if pos.x() > self.width() - 30:
                # 버튼이 닫힌 곳을 클릭하십시오. 
                self.windowClosed.emit()


class Window(QStackedWidget):
    # 메인 창 

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(428, 329)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # 这个 是 动, 먼저 표시되지 않습니다 
        self.flipWidget = FlipWidget()
        self.flipWidget.finished.connect(self.showWidget)

        #luge 창 
        self.loginWidget = LoginWidget(self)
        self.loginWidget.windowClosed.connect(self.close)
        self.loginWidget.windowChanged.connect(self.jumpSettingWidget)
        self.addWidget(self.loginWidget)

        # 창을 설정하십시오 
        self.settingWidget = SettingWidget(self)
        self.settingWidget.windowClosed.connect(self.close)
        self.settingWidget.windowChanged.connect(self.jumpLoginWidget)
        self.addWidget(self.settingWidget)

    def showWidget(self):
        # 메인 윈도우 숨겨진 애니메이션 창을 표시합니다 
        self.setWindowOpacity(1)
        QTimer.singleShot(100, self.flipWidget.hide)

    def jumpLoginWidget(self):
        # œ 로그인 인터페이스 
        self.setWindowOpacity(0)                 # 类似 隐,하지만 작업 표시 줄을 유지합니다 
        self.setCurrentWidget(self.loginWidget)  # 很 重要, 과거를 전환해야합니다, 그렇지 않으면 첫 번째 스크린 샷 수입이 발생합니다. 
        image1 = self.loginWidget.grab()       # 图 图 1. 
        image2 = self.settingWidget.grab()     # 图 图 2. 
        padding = 100                          # margin @unusedvariable을 확장하십시오 
        self.flipWidget.setGeometry(self.geometry())
        # .adjusted(-padding, -padding, padding, padding))
        self.flipWidget.updateImages(FlipWidget.Right, image2, image1)

    def jumpSettingWidget(self):
        # 翻 到 설정 인터페이스 
        self.setWindowOpacity(0)                  # 类似 隐,하지만 작업 표시 줄을 유지합니다 
        self.setCurrentWidget(self.settingWidget)  # 很 重要, 과거를 전환해야합니다, 그렇지 않으면 첫 번째 스크린 샷 수입이 발생합니다. 
        image1 = self.loginWidget.grab()       # 图 图 1. 
        image2 = self.settingWidget.grab()     # 图 图 2. 
        padding = 100                          # margin @unusedvariable을 확장하십시오 
        self.flipWidget.setGeometry(self.geometry())
        # .adjusted(-padding, -padding, padding, padding))
        self.flipWidget.updateImages(FlipWidget.Left, image1, image2)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
