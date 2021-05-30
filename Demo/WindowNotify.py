#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年3月30日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: WindowNotify
@description: 右下角弹窗
'''
import webbrowser

from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton

from Lib.UiNotify import Ui_NotifyForm  # @UnresolvedImport


__version__ = "0.0.1"


class WindowNotify(QWidget, Ui_NotifyForm):

    SignalClosed = pyqtSignal()  # 弹窗 关 关 信号 

    def __init__(self, title="", content="", timeout=5000, *args, **kwargs):
        super(WindowNotify, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setTitle(title).setContent(content)
        self._timeout = timeout
        self._init()

    def setTitle(self, title):
        if title:
            self.labelTitle.setText(title)
        return self

    def title(self):
        return self.labelTitle.text()

    def setContent(self, content):
        if content:
            self.labelContent.setText(content)
        return self

    def content(self):
        return self.labelContent.text()

    def setTimeout(self, timeout):
        if isinstance(timeout, int):
            self._timeout = timeout
        return self

    def timeout(self):
        return self._timeout

    def onView(self):
        print("onView")
        webbrowser.open_new_tab("http://alyl.vip")

    def onClose(self):
        # 종료 버튼을 클릭하십시오 
        print("onClose")
        self.isShow = False
        QTimer.singleShot(100, self.closeAnimation)# 启 弹 弹 回 

    def _init(self):
        # 隐 隐 任栏 | | 테두리 제거 | 탑 플래시 디스플레이 
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 닫기 버튼 이벤트 
        self.buttonClose.clicked.connect(self.onClose)
        #보기 버튼을 클릭하십시오 
        self.buttonView.clicked.connect(self.onView)
        # 是 是 是 显示 
        self.isShow = True
        # 시간 초과 
        self._timeouted = False
        # 데스크탑 
        self._desktop = QApplication.instance().desktop()
        # 初 初 开始 开始 开始. 
        self._startPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 5,
            self._desktop.screenGeometry().height()
        )
        # 弹 弹 结 结 结. 
        self._endPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 5,
            self._desktop.availableGeometry().height() - self.height() - 5
        )
        # 초기화 위치 하단의 오른쪽 구석 
        self.move(self._startPos)

        # 动画 
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.finished.connect(self.onAnimationEnd)
        self.animation.setDuration(1000)  # 1s

        # 弹 回 回 定 
        self._timer = QTimer(self, timeout=self.closeAnimation)

    def show(self, title="", content="", timeout=5000):
        self._timer.stop()  # 停 时器, 두 번째 팝업 창 앞에 타이머를 방지하십시오. 
        self.hide()  # 先 隐 隐 隐 
        self.move(self._startPos)  # 초기화 위치 하단의 오른쪽 구석 
        super(WindowNotify, self).show()
        self.setTitle(title).setContent(content).setTimeout(timeout)
        return self

    def showAnimation(self):
        print("showAnimation isShow = True")
        # 애니메이션을 표시합니다 
        self.isShow = True
        self.animation.stop()# 먼저 이전 애니메이션을 중지하고 다시 시작하십시오 
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._endPos)
        self.animation.start()
        # 5 초 후, 초점이 없으면 재생됩니다. 
        self._timer.start(self._timeout)
#         QTimer.singleShot(self._timeout, self.closeAnimation)

    def closeAnimation(self):
        print("closeAnimation hasFocus", self.hasFocus())
        # 애니메이션을 닫습니다 
        if self.hasFocus():
            # 팝업 카운트 다운 5 초 동안, 여전히 초점이 있으면 손실 될 때 활성 트리거가 있습니다. 
            self._timeouted = True
            return  # 초점이 있으면 닫지 마십시오 
        self.isShow = False
        self.animation.stop()
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._startPos)
        self.animation.start()

    def onAnimationEnd(self):
        # 结 动 
        print("onAnimationEnd isShow", self.isShow)
        if not self.isShow:
            print("onAnimationEnd close()")
            self.close()
            print("onAnimationEnd stop timer")
            self._timer.stop()
            print("onAnimationEnd close and emit signal")
            self.SignalClosed.emit()

    def enterEvent(self, event):
        super(WindowNotify, self).enterEvent(event)
        # 포커스 설정 (사용되는 것처럼 보이지만 마우스 클릭,이 방법은 유용합니다) 
        print("enterEvent setFocus Qt.MouseFocusReason")
        self.setFocus(Qt.MouseFocusReason)

    def leaveEvent(self, event):
        super(WindowNotify, self).leaveEvent(event)
        # 取 点 
        print("leaveEvent clearFocus")
        self.clearFocus()
        if self._timeouted:
            QTimer.singleShot(1000, self.closeAnimation)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QHBoxLayout
    app = QApplication(sys.argv)

    window = QWidget()
    notify = WindowNotify(parent=window)

    layout = QHBoxLayout(window)

    b1 = QPushButton(
        "弹窗1", window, clicked=lambda: notify.show(content=b1.text()).showAnimation())
    b2 = QPushButton(
        "弹窗2", window, clicked=lambda: notify.show(content=b2.text()).showAnimation())

    layout.addWidget(b1)
    layout.addWidget(b2)

    window.show()

    sys.exit(app.exec_())
