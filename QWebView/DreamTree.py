#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年4月6日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: DreamTree
@description: 
'''

import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from Lib import data_rc  # @UnusedImport @UnresolvedImport

# from PyQt5.QtWebKit import QWebSettings
__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


# 투명한 WebView를 얻으려면 QWidget을 상위 제어로 사용해야합니다. 


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 부모 컨트롤 위젯 배경을 투명하게 설정합니다 
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去 掉 掉 边 
        palette = self.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)  # 父 控 控 背景 透 透 
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        #         QWebSettings.globalSettings().setAttribute(
        # QWebSettings.DeveloperExtraSenabled, true) # 웹 개발자 도구 

        self.webView = QWebView(self)  # 网 网 조절기 
        layout.addWidget(self.webView)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)  # 去 键 键 菜 
        self.mainFrame = self.webView.page().mainFrame()

        self.mainFrame.setScrollBarPolicy(
            Qt.Vertical, Qt.ScrollBarAlwaysOff)  # 去 滑条 
        self.mainFrame.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)

        # maximize. 
        rect = app.desktop().availableGeometry()
        self.resize(rect.size())
        self.webView.resize(rect.size())

    def load(self):
        self.webView.load(QUrl('qrc:/tree.html'))  # 加 网 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load()
    sys.exit(app.exec_())
