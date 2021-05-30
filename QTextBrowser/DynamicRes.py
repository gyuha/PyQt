#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/6/3
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: DynamicRes
@description: 
"""
from threading import Thread

import requests
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtGui import QImage, QTextDocument
from PyQt5.QtWidgets import QTextBrowser, QWidget, QVBoxLayout, QPushButton

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020'
__Version__ = 'Version 1.0'


class TextBrowser(QTextBrowser):
    NetImages = {}

    def __init__(self, *args, **kwargs):
        super(TextBrowser, self).__init__(*args, **kwargs)
        self.setOpenLinks(False)  # URL을 열지 마십시오 

    def downloadImage(self, url):
        try:
            self.NetImages[url] = [QByteArray(requests.get(url.toString()).content), 1]
            print('下载完成', url)
        except Exception as e:
            print('下载失败', url, e)
            self.NetImages[url] = [QByteArray(), 1]

    def loadResource(self, rtype, url):
        ret = super(TextBrowser, self).loadResource(rtype, url)
        # 이미지 리소스를로드합니다 
        if rtype == QTextDocument.ImageResource:
            if ret:
                return ret
            if url.toString().startswith('irony'):  # 사용자 정의 프로토콜 헤더 
                print('加载本地', '../Donate/zhifubao.png', url)
                return QImage('../Donate/zhifubao.png')  # 或者 qbytearray (오픈 ( '../ 기부 / zhifubao.png', 'rb') 읽기 ()) 
            elif url.toString().startswith('http'):  # 加 网 网 
                img, status = self.NetImages.get(url, [None, None])
                if url not in self.NetImages or status is None:
                    # 子 线 下载 下载 下载. 
                    self.NetImages[url] = [None, 1]
                    print('download ', url)
                    Thread(target=self.downloadImage, args=(url,), daemon=True).start()
                elif img:
                    return img
        return ret

    def mouseDoubleClickEvent(self, event):
        # 이미지의 그림을 얻으려면 이미지를 두 번 클릭하거나이를 사용하여 확대 / 축소 할 수 있습니다. 
        super(TextBrowser, self).mouseDoubleClickEvent(event)
        url = self.anchorAt(event.pos())
        if url:
            print('url:', url, self.document().resource(QTextDocument.ImageResource, QUrl(url)))


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        self.textBrowser = TextBrowser(self)
        self.downButton = QPushButton('加载网络图片', self)

        layout.addWidget(self.textBrowser)
        layout.addWidget(self.downButton)

        # 로딩 사진로드 
        img = QImage('../Donate/weixin.png')
        # 두 번째 매개 변수는 QRC 모드와 유사한 임의의 고유 URL입니다. 
        self.textBrowser.document().addResource(QTextDocument.ImageResource, QUrl('dynamic:/images/weixin.png'), img)

        # html을 설정합니다 
        # 내부 이미지 주소에주의가 필요합니다 
        self.textBrowser.setHtml(
            '<p><a href="../Donate/weixin.png"><img src="../Donate/weixin.png"></a></p>'  # 方式 一 직접 로컬 그림을로드합니다 
            '<p><a href="dynamic:/images/weixin.png"><img src="dynamic:/images/weixin.png"></a></p>'  # 方式 二 AddResource를 통해 리소스 추가 
            '<p><a href="irony://zhifubao.png"><img src="irony://zhifubao.png"></a></p>'  # 方式 三 맞춤형 프로토콜 헤드 정의 loadResource를 통해 동적으로로드됩니다. 
            '<p><a href="https://blog.pyqt5.com/img/avatar.png"><img '  # ¶ 네 가지 유사한 방식 3이지만 네트워크에서 다운로드 할 필요가 없습니다. 
            'src="https://blog.pyqt5.com/img/avatar.png"></a></p>')


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
