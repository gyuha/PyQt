#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/6/11
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file:
@description: 
"""

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020'
__Version__ = 'Version 1.0'

from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QSplashScreen, QWidget


class GifSplashScreen(QSplashScreen):

    def __init__(self, *args, **kwargs):
        super(GifSplashScreen, self).__init__(*args, **kwargs)
        self.movie = QMovie('Data/splash.gif')
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.movie.start()

    def onFrameChanged(self, _):
        self.setPixmap(self.movie.currentPixmap())

    def finish(self, widget):
        self.movie.stop()
        super(GifSplashScreen, self).finish(widget)


class BusyWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(BusyWindow, self).__init__(*args, **kwargs)
        # 模 模 操作 操作, 일반적으로 시간 소모적 인로드 데이터가 스레드에 넣어야합니다. 
        for i in range(5):
            sleep(1)
            splash.showMessage('加载进度: %d' % i, Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
            QApplication.instance().processEvents()

        splash.showMessage('初始化完成', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        splash.finish(self)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(1, None, 5, '')

    app = QApplication(sys.argv)

    global splash
    splash = GifSplashScreen()
    splash.show()

    w = BusyWindow()
    w.show()

    # 테스트 2. 
    # def createWindow():
    #     app.w = QWidget()
    # # # 模 模 初 初 后 
    # splash.showmessage ( '대기 인터페이스 디스플레이', qt.alignhcenter | qt.alignbottom, qt.white) 
    #     QTimer.singleShot(3000, lambda: (
    # splash.showmessage ( '초기화 완료', qt.alignhcenter | qt.alignbottom, qt.white), app.w.show (), 
    #         splash.finish(app.w)))

    # 模 模 耗 5 초. 하지만 잠을 잘 수 없어 
    # 하위 스레드로드 베어링 시간 소모 데이터를 사용할 수 있습니다. 
    # 主 线 の 中 の の u 设置 设置 可以 qpplication.instance (). ProcessEvents () 
    # QTimer.singleShot(3000, createWindow)

    splash.showMessage('等待创建界面', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)

    sys.exit(app.exec_())
