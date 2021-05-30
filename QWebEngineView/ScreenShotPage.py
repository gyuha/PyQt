#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月8日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: ScreenShotPage
@description: 网页整体截图
"""
import base64
import cgitb
import os
import sys

from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QSize, QTimer
from PyQt5.QtGui import QImage, QPainter, QIcon, QPixmap
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton,\
    QGroupBox, QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem,\
    QProgressDialog


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"
__Version__ = "Version 1.0"

# 일부 콘텐츠의 스크린 샷 
CODE = """
var el = $("%s");
html2canvas(el[0], {
    width: el.outerWidth(true), 
    windowWidth: el.outerWidth(true),
}).then(function(canvas) {
    window._self.saveImage(canvas.toDataURL());
    canvas = null;
});
"""

# 대화 형 브리지 스크립트를 만듭니다 
CreateBridge = """
new QWebChannel(qt.webChannelTransport,
    function(channel) {
        window._self = channel.objects._self;
    }
);
"""


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(600, 400)
        layout = QHBoxLayout(self)

        # 左 
        widgetLeft = QWidget(self)
        layoutLeft = QVBoxLayout(widgetLeft)
        # 권리 
        self.widgetRight = QListWidget(
            self, minimumWidth=200, iconSize=QSize(150, 150))
        self.widgetRight.setViewMode(QListWidget.IconMode)
        layout.addWidget(widgetLeft)
        layout.addWidget(self.widgetRight)

        self.webView = QWebEngineView()
        layoutLeft.addWidget(self.webView)

        # 스크린 샷 방법 
        groupBox1 = QGroupBox('截图方式一', self)
        layout1 = QVBoxLayout(groupBox1)
        layout1.addWidget(QPushButton('截图1', self, clicked=self.onScreenShot1))
        layoutLeft.addWidget(groupBox1)

        # 스크린 샷 모드 2 (JS 사용) 
        groupBox2 = QGroupBox('截图方式二', self)
        layout2 = QVBoxLayout(groupBox2)
        self.codeEdit = QLineEdit(
            'body', groupBox2, placeholderText='请输入需要截图的元素、ID或者class：如body、#id .class')
        layout2.addWidget(self.codeEdit)
        self.btnMethod2 = QPushButton(
            '', self, clicked=self.onScreenShot2, enabled=False)
        layout2.addWidget(self.btnMethod2)
        layoutLeft.addWidget(groupBox2)

        # 액세스 인터페이스를 제공합니다 
        self.channel = QWebChannel(self)
        # 자신의 개체를 통과하십시오 
        self.channel.registerObject('_self', self)
        # 대화 형 인터페이스를 설정하십시오 
        self.webView.page().setWebChannel(self.channel)
        # 지원 스크린 샷 
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        self.webView.loadStarted.connect(self.onLoadStarted)
        self.webView.loadFinished.connect(self.onLoadFinished)
        self.webView.load(QUrl("https://pyqt.site"))

    def onLoadStarted(self):
        print('load started')
        self.btnMethod2.setEnabled(False)
        self.btnMethod2.setText('暂时无法使用（等待页面加载完成）')

    @pyqtSlot(bool)
    def onLoadFinished(self, finished):
        if not finished:
            return
        print('load finished')
        # 注 
        page = self.webView.page()
        # qwebchannel, jquery, 약속, html2canvas를 실행하십시오 
        page.runJavaScript(
            open('Data/qwebchannel.js', 'rb').read().decode())
        page.runJavaScript(
            open('Data/jquery.js', 'rb').read().decode())
#         page.runJavaScript(
#             open('Data/promise-7.0.4.min.js', 'rb').read().decode())
        page.runJavaScript(
            open('Data/html2canvas.min.js', 'rb').read().decode())
        page.runJavaScript(CreateBridge)
        print('inject js ok')
        self.btnMethod2.setText('截图2')
        self.btnMethod2.setEnabled(True)

    def onScreenShot1(self):
        # 스크린 샷 방법 1 
        page = self.webView.page()
        oldSize = self.webView.size()
        self.webView.resize(page.contentsSize().toSize())

        def doScreenShot():
            rect = self.webView.contentsRect()
            size = rect.size()
            image = QImage(size, QImage.Format_ARGB32_Premultiplied)
            image.fill(Qt.transparent)

            painter = QPainter()
            painter.begin(image)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            self.webView.render(painter)
            painter.end()
            self.webView.resize(oldSize)

            # 왼쪽 목록에 추가하십시오 
            item = QListWidgetItem(self.widgetRight)
            image = QPixmap.fromImage(image)
            item.setIcon(QIcon(image))
            item.setData(Qt.UserRole + 1, image)

        # 먼저 스크린 샷을 찍어 보자. 
        QTimer.singleShot(2000, doScreenShot)

    def onScreenShot2(self):
        # 스크린 샷 모드 2 
        code = self.codeEdit.text().strip()
        if not code:
            return
        self.progressdialog = QProgressDialog(self, windowTitle='正在截图中')
        self.progressdialog.setRange(0, 0)
        self.webView.page().runJavaScript(CODE % code)
        self.progressdialog.exec_()

    @pyqtSlot(str)
    def saveImage(self, image):
        self.progressdialog.close()
        # data:image/png;base64,iVBORw0KG....
        if not image.startswith('data:image'):
            return
        data = base64.b64decode(image.split(';base64,')[1])
        image = QPixmap()
        image.loadFromData(data)
        # 왼쪽 목록에 추가하십시오 
        item = QListWidgetItem(self.widgetRight)
        item.setIcon(QIcon(image))
        item.setData(Qt.UserRole + 1, image)


if __name__ == "__main__":
    # F12 콘솔 기능을 켜면 브라우저를 통해이 페이지를 별도로 열어야합니다. 
    #이 환경 변수를 삭제할 수 있으므로 보호 기능을 수행 할 수 있습니다. 환경 변수를 통해 다른 사람들이 열리지 않도록합니다 
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = Window()
    w.show()

    # 디버그를 엽니 다 
    dw = QWebEngineView()
    dw.setWindowTitle('开发人员工具')
    dw.load(QUrl('http://127.0.0.1:9966'))
    dw.show()
    dw.move(100, 100)
    sys.exit(app.exec_())
