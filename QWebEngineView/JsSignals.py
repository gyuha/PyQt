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
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QPushButton


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class WebEngineView(QWebEngineView):

    customSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(WebEngineView, self).__init__(*args, **kwargs)
        self.initSettings()
        self.channel = QWebChannel(self)
        # 자신의 개체를 통과하십시오 
        self.channel.registerObject('Bridge', self)
        # 대화 형 인터페이스를 설정하십시오 
        self.page().setWebChannel(self.channel)

        # 시작 ##### 다음 코드는 5.6 QWEBENGINEVIEW가 방금 나오는 경우 버그 일 수 있으며 각로드 페이지 중에 수동으로 주입해야합니다. 
        #### 점프 후에 실패 할 수도 있고, 무효가 될 수 있으며 수동으로 임플란트를 사용해야하며, 테스트되지 않은 특정 수리가 없습니다. 

#         self.page().loadStarted.connect(self.onLoadStart)
#         self._script = open('Data/qwebchannel.js', 'rb').read().decode()

#     def onLoadStart(self):
#         self.page().runJavaScript(self._script)

        # END ###########################

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
        return super(WebEngineView, self).load(QUrl(url))

    def initSettings(self):
        '''
        eg: 初始化设置
        '''
        # 브라우저 기본 설정을 얻습니다 
        settings = QWebEngineSettings.globalSettings()
        # 기본 인코딩 된 UTF8을 설정합니다 
        settings.setDefaultTextEncoding("utf-8")
        # 자동으로 그림을로드하고 기본값을 엽니 다 
        # settings.setAttribute(QWebEngineSettings.AutoLoadImages,True)
        # 자동으로 아이콘을로드하고 기본값을 엽니 다 
        # settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage,True)
        # JS를 엽니 다. 기본값을 엽니 다 
        # settings.setAttribute(QWebEngineSettings.JavascriptEnabled,True)
        # JS 액세스 클립 보드 
        settings.setAttribute(
            QWebEngineSettings.JavascriptCanAccessClipboard, True)
        # JS 창을 열고 기본값을 엽니 다. 
        # settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows,True)
        #Link 상태를 가져 오면 기본값이 켜져 있습니다. 
        # settings.setAttribute(QWebEngineSettings.LinksIncludedInFocusChain,True)
        # 로컬 저장소, 기본 열림 
        # settings.setAttribute(QWebEngineSettings.LocalStorageEnabled,True)
        # 로컬 액세스 원격 
        settings.setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        # 로컬로드, 기본 열림 
        # settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls,True)
        #로드 요청을 모니터합니다. 사이트 크로스 스크립트, 기본값 닫기 
        # settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled,False)
        # 공간 탐색 특성, 기본 닫기 
        # settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled,False)
        # 플랫 체인 링크 속성을 지원합니다. 기본 닫기 
        # settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled,False)
        # 스크롤 애니메이션을 사용하여 기본값을 닫습니다 
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        # 기본적으로 사용 가능한 오류 페이지를 지원합니다 
        # settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        # 지원 플러그인, 기본 닫기 
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # 전체 화면 응용 프로그램 지원, 기본 닫기 
        settings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True)
        # 지원 화면 스크린 샷, 기본 닫기 
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        # HTML5 WebGL 지원, 기본 열림 
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        # 지원 2D 그리기, 기본 열기 
        settings.setAttribute(
            QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        # 지원 아이콘 터치, 기본 닫기 
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.webview = WebEngineView(self)
        layout.addWidget(self.webview)
        layout.addWidget(QPushButton(
            '发送自定义信号', self, clicked=self.webview.sendCustomSignal))

        self.webview.windowTitleChanged.connect(self.setWindowTitle)
        self.webview.load(QUrl.fromLocalFile(
            os.path.abspath('Data/JsSignals.html')))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    # F12 콘솔 기능을 켜면 브라우저를 통해이 페이지를 별도로 열어야합니다. 
    #이 환경 변수를 삭제할 수 있으므로 보호 기능을 수행 할 수 있습니다. 환경 변수를 통해 다른 사람들이 열리지 않도록합니다 
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.move(100, 100)

    # 디버그를 엽니 다 
    dw = QWebEngineView()
    dw.setWindowTitle('开发人员工具')
    dw.load(QUrl('http://127.0.0.1:9966'))
    dw.move(600, 100)
    dw.show()
    sys.exit(app.exec_())
