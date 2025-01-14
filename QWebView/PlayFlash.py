#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QWebView.PlayFlash
@description: 播放Flash
"""
import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QSslConfiguration, QSslCertificate, QSsl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWebView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 览 设置 
        setting = QWebSettings.globalSettings()
        setting.setAttribute(QWebSettings.PluginsEnabled, True)
        # 解 x 下 s 문제 
        self.page().networkAccessManager().sslErrors.connect(self.handleSslErrors)
        sslconf = QSslConfiguration.defaultConfiguration()
        clist = sslconf.caCertificates()
        cnew = QSslCertificate.fromData(b"CaCertificates")
        clist.extend(cnew)
        sslconf.setCaCertificates(clist)
        sslconf.setProtocol(QSsl.AnyProtocol)
        QSslConfiguration.setDefaultConfiguration(sslconf)

    def handleSslErrors(self, reply, errors):
        # SSL 오류를 해결하십시오 
        reply.ignoreSslErrors()


if __name__ == '__main__':
    # 매우 중요합니다. 디렉토리가있는 npswf32.dll 파일로 설정 
    os.environ['QTWEBKIT_PLUGIN_PATH'] = os.path.abspath('Data')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load(QUrl('https://www.17sucai.com/preview/8825/2013-07-07/%E4%B8%80%E6%AC%BE%E4%BA%BA%E5%BD%A2%E5%8A%A8%E4%BD%9C%E6%98%BE%E7%A4%BA%E7%9A%84flash%E6%97%B6%E9%97%B4/index.html'))
    sys.exit(app.exec_())
