#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月24日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QWebView.BlockAds
@description: 拦截请求
"""
from PyQt5.QtCore import QUrl, QBuffer, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtWebKitWidgets import QWebView


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


class RequestInterceptor(QNetworkAccessManager):

    def createRequest(self, op, originalReq, outgoingData):
        """创建请求
        :param op:           操作类型见http://doc.qt.io/qt-5/qnetworkaccessmanager.html#Operation-enum
        :param originalReq:  原始请求
        :param outgoingData: 输出数据
        """
        url = originalReq.url().toString()
        if url.find('pos.baidu.com') > -1 and url.find('ltu=') > -1:
            # 가로 촬영 Baidu Alliance 광고 
            print('block:', url)
            originalReq.setUrl(QUrl())
        if op == self.PostOperation and outgoingData:
            # 포스트 데이터를 가로 채거나 수정하십시오 
            # 읽는 후 다시 설정해야합니다. 그렇지 않으면 웹 사이트가 요청을받지 못합니다. 
            data = outgoingData.readAll().data()
            print('post data:', data)
            # 데이터를 수정 한 후 # 재설정하십시오 
            outgoingData = QBuffer(self)
            outgoingData.setData(data)

        return super(RequestInterceptor, self).createRequest(op, originalReq, outgoingData)


class Window(QWebView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.page().setNetworkAccessManager(RequestInterceptor(self))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.load(QUrl('https://so.csdn.net/so/search/s.do?q=Qt&t=blog'))
    sys.exit(app.exec_())
