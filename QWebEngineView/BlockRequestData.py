#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020年2月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QWebEngineView.BlockRequestData
@description: 拦截请求内容
"""
from PyQt5.QtCore import QUrl, QFile, QIODevice
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler,\
    QWebEngineUrlRequestInterceptor, QWebEngineUrlScheme  # @UnresolvedImport
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


# 사용자 정의 URL 프로토콜 헤더 
class UrlSchemeHandler(QWebEngineUrlSchemeHandler):

    def requestStarted(self, job):
        url = job.requestUrl().toString()
        if url == 'myurl://png':
            file = QFile('Data/app.png', job)
            file.open(QIODevice.ReadOnly)
            job.reply(b'image/png', file)

# 가난자를 요청하십시오 


class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        # 여기서 데모는 JS 파일을 가로 채는 것과 같이 자유롭게 재생할 수있는 모든 PNG 그림을 가로 챌 수 있습니다. 
        if url.endswith('.png'):
            # Ration은 자체 URL 프로토콜로 리디렉션하는 것입니다. 
            info.redirect(QUrl('myurl://png'))


class Window(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)

        # 먼저 기본 URL 프로토콜을 가져옵니다 
        h1 = QWebEngineUrlScheme.schemeByName(b'http')
        h2 = QWebEngineUrlScheme.schemeByName(b'https')

        # 여기에서 로컬 파일과 도메인 간 지원을 수정해야합니다. 
        CorsEnabled = 0x80  # 5.14 증가 
        h1.setFlags(h1.flags() |
                    QWebEngineUrlScheme.SecureScheme |
                    QWebEngineUrlScheme.LocalScheme |
                    QWebEngineUrlScheme.LocalAccessAllowed |
                    CorsEnabled)
        h2.setFlags(h2.flags() |
                    QWebEngineUrlScheme.SecureScheme |
                    QWebEngineUrlScheme.LocalScheme |
                    QWebEngineUrlScheme.LocalAccessAllowed |
                    CorsEnabled)

        # URL 인터셉터 및 사용자 정의 URL 프로토콜 처리 설치 
        de = QWebEngineProfile.defaultProfile()  # @UndefinedVariable
        de.setRequestInterceptor(RequestInterceptor(self))
        de.installUrlSchemeHandler(b'myurl', UrlSchemeHandler(self))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load(QUrl('https://www.baidu.com/'))
    sys.exit(app.exec_())
