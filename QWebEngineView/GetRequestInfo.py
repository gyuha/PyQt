#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月24日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QWebEngineView.BlockAds
@description: 拦截请求
"""
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler, QWebEngineUrlScheme, \
    QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


class UrlSchemeHandler(QWebEngineUrlSchemeHandler):
    AttrType = QNetworkRequest.User + 1

    def __init__(self, *args, **kwargs):
        super(UrlSchemeHandler, self).__init__(*args, **kwargs)
        self._manager = QNetworkAccessManager(self)
        self._manager.finished.connect(self.onFinished)

    def requestStarted(self, request):
        # 
        # request.fail(QWebEngineUrlRequestJob.RequestDenied)
        # print('initiator:', request.initiator())
        print('requestMethod:', request.requestMethod())
        print('requestHeaders:', request.requestHeaders())
        url = request.requestUrl()
        if url.scheme().startswith('myurl'):
            url.setScheme(url.scheme().replace('myurl', 'http'))
        print('requestUrl:', url)

        # 실제 요청을 구성합니다 
        req = QNetworkRequest(url)
        req.setAttribute(self.AttrType, request)  # 기록 
        for headerName, headerValue in request.requestHeaders().items():
            req.setRawHeader(headerName, headerValue)
        method = request.requestMethod()

        # Todo : 여기서 브라우저 내부에서 쿠키를 가져와 그것을 재설정해야합니다. 
        if method == b'GET':
            self._manager.get(req)
        # TODO : 이것은 게시물 데이터를 얻을 수있는 방법이없고 AJAX 요청이 문제가있는 것 같습니다. 
        elif method == b'POST':
            self._manager.post(req)

    def onFinished(self, reply):
        req = reply.request()  # 요청 받기 
        o_req = req.attribute(self.AttrType, None)
        if o_req:
            #주의 사항 : 데이터를 수정하고 데이터로 돌아갈 수 있습니다. 
            # Todo : QnetworkAccessManager 및 브라우저간에 쿠키 동기화 문제가있을 수 있습니다. 
            o_req.reply(req.header(QNetworkRequest.ContentTypeHeader) or b'text/html', reply)
            o_req.destroyed.connect(reply.deleteLater)


# 모든 요청을 MyUrl로 리디렉션합니다 
class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl()
        if url.scheme() == 'http':
            # 重 向 
            url.setScheme('myurl')
            info.redirect(url)
        elif url.scheme() == 'https':
            # 重 向 
            url.setScheme('myurls')
            info.redirect(url)


class Window(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        profile = QWebEngineProfile.defaultProfile()

        # 먼저 기본 URL 프로토콜을 가져옵니다 
        o_http = QWebEngineUrlScheme.schemeByName(b'http')
        o_https = QWebEngineUrlScheme.schemeByName(b'https')
        print('scheme:', o_http, o_https)

        # 여기에서 로컬 파일과 도메인 간 지원을 수정해야합니다. 
        CorsEnabled = 0x80  # 5.14 증가 
        o_http.setFlags(
            o_http.flags() | QWebEngineUrlScheme.SecureScheme | QWebEngineUrlScheme.LocalScheme | QWebEngineUrlScheme.LocalAccessAllowed | CorsEnabled)
        o_https.setFlags(
            o_https.flags() | QWebEngineUrlScheme.SecureScheme | QWebEngineUrlScheme.LocalScheme | QWebEngineUrlScheme.LocalAccessAllowed | CorsEnabled)

        # URL 인터셉터 및 사용자 정의 URL 프로토콜 처리 설치 
        de = QWebEngineProfile.defaultProfile()  # @UndefinedVariable
        de.setRequestInterceptor(RequestInterceptor(self))
        self.urlSchemeHandler = UrlSchemeHandler(self)
        de.installUrlSchemeHandler(b'myurl', self.urlSchemeHandler)  # for http
        de.installUrlSchemeHandler(b'myurls', self.urlSchemeHandler)  # for https


if __name__ == '__main__':
    import sys
    import os
    import webbrowser
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # F12 콘솔 기능을 켜면 브라우저를 통해이 페이지를 별도로 열어야합니다. 
    #이 환경 변수를 삭제할 수 있으므로 보호 기능을 수행 할 수 있습니다. 환경 변수를 통해 다른 사람들이 열리지 않도록합니다 
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    # 디버그를 엽니 다 
    webbrowser.open_new_tab('http://127.0.0.1:9966')

    w = Window()
    w.show()
    w.load(QUrl('https://pyqt.site'))
    sys.exit(app.exec_())
