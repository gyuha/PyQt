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
import sys

from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPainter, QIcon, QPixmap
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
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
    _self.saveImage(canvas.toDataURL());
});
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

        self.webView = QWebView()
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

        # 개발자 도구를 엽니 다 
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True)
        self.webView.loadStarted.connect(self.onLoadStarted)
        self.webView.loadFinished.connect(self.onLoadFinished)
        self.webView.load(QUrl("https://pyqt5.com"))

        # 인터페이스 및로드 후 jQuery와 같은 일부 라이브러리 파일을 실행하는 데 노출됩니다. 
        self.webView.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScriptWindowObject)

    def populateJavaScriptWindowObject(self):
        self.webView.page().mainFrame().addToJavaScriptWindowObject(
            '_self', self)

    def onLoadStarted(self):
        print('load started')
        self.btnMethod2.setEnabled(False)
        self.btnMethod2.setText('暂时无法使用（等待页面加载完成）')

    def onLoadFinished(self):
        # 注 
        mainFrame = self.webView.page().mainFrame()
        # jQuery, 약속, html2canvas를 실행하십시오 
        mainFrame.evaluateJavaScript(
            open('Data/jquery.js', 'rb').read().decode())
        mainFrame.evaluateJavaScript(
            open('Data/promise-7.0.4.min.js', 'rb').read().decode())
        mainFrame.evaluateJavaScript(
            open('Data/html2canvas.min.js', 'rb').read().decode())
        print('inject js ok')
        self.btnMethod2.setText('截图2')
        self.btnMethod2.setEnabled(True)

    def onScreenShot1(self):
        # 스크린 샷 방법 1 
        page = self.webView.page()
        frame = page.mainFrame()
        size = frame.contentsSize()
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)

        painter = QPainter()
        painter.begin(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # 오래된 크기를 녹음하십시오 
        oldSize = page.viewportSize()
        # **** 초점은 여기 ****** 
        page.setViewportSize(size)
        frame.render(painter)
        painter.end()

        # 스크린 샷이 완료된 후 # 복원, 그렇지 않으면 인터페이스가 마우스에 응답하지 않습니다. 
        page.setViewportSize(oldSize)

        # 왼쪽 목록에 추가하십시오 
        item = QListWidgetItem(self.widgetRight)
        image = QPixmap.fromImage(image)
        item.setIcon(QIcon(image))
        item.setData(Qt.UserRole + 1, image)

    def onScreenShot2(self):
        # 스크린 샷 모드 2 
        code = self.codeEdit.text().strip()
        if not code:
            return
        self.progressdialog = QProgressDialog(self, windowTitle='正在截图中')
        self.progressdialog.setRange(0, 0)
        self.webView.page().mainFrame().evaluateJavaScript(CODE % code)
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
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
