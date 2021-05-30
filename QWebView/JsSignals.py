#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月27日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QWebEngineView.JsSignals
@description: 
"""
import os
from time import time

from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QPushButton


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class WebView(QWebView):

    customSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)
        self.initSettings()
        # 노출 인터페이스 개체 
        self.page().mainFrame().javaScriptWindowObjectCleared.connect(self._exposeInterface)

    def _exposeInterface(self):
        """向Js暴露调用本地方法接口
        """
        self.page().mainFrame().addToJavaScriptWindowObject('Bridge', self)

    # note pyqtslot은 JS에 함수를 노출하는 데 사용됩니다. 
    @pyqtSlot(str)
    def callFromJs(self, text):
        QMessageBox.information(self, "提示", "来自js调用：{}".format(text))

    def sendCustomSignal(self):
        # 사용자 정의 신호를 보냅니다 
        self.customSignal.emit('当前时间: ' + str(time()))

    @pyqtSlot(str)
    @pyqtSlot(QUrl)
    def load(self, url):
        '''
        eg: load("https://pyqt5.com")
        :param url: 网址
        '''
        return super(WebView, self).load(QUrl(url))

    def initSettings(self):
        '''
        eg: 初始化设置
        '''
        # 브라우저 기본 설정을 얻습니다 
        settings = self.settings()
        # 개발자 도구를 엽니 다 
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        # 기본 코드를 설정하십시오 
        settings.setDefaultTextEncoding('UTF-8')


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.webview = WebView(self)
        layout.addWidget(self.webview)
        layout.addWidget(QPushButton(
            '发送自定义信号', self, clicked=self.webview.sendCustomSignal))

        self.webview.windowTitleChanged.connect(self.setWindowTitle)
        self.webview.load(QUrl.fromLocalFile(
            os.path.abspath('Data/JsSignals.html')))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.move(100, 100)
    sys.exit(app.exec_())
