#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月27日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: BubbleTips
@description: 
'''
import sys

from PyQt5.QtCore import QRectF, Qt, QPropertyAnimation, pyqtProperty, \
    QPoint, QParallelAnimationGroup, QEasingCurve
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication,\
    QLineEdit, QPushButton


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class BubbleLabel(QWidget):

    BackgroundColor = QColor(195, 195, 195)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text", "")
        super(BubbleLabel, self).__init__(*args, **kwargs)
        # 무한한 프레임을 설정합니다 
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # 최소 너비와 높이를 설정하십시오 
        self.setMinimumWidth(200)
        self.setMinimumHeight(48)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout(self)
        # 왼쪽 상단의 여백 (하위 16 아래의 삼각형 때문에) 
        layout.setContentsMargins(8, 8, 8, 16)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.setText(text)
        # 스크린을 높이고 넓게하십시오 
        self._desktop = QApplication.instance().desktop()

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.close()

    def show(self):
        super(BubbleLabel, self).show()
        # 창 시작 위치 
        startPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 100,
            self._desktop.availableGeometry().height() - self.height())
        endPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 100,
            self._desktop.availableGeometry().height() - self.height() * 3 - 5)
        print(startPos, endPos)
        self.move(startPos)
        # 초기화 애니메이션 
        self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        # 투명성 애니메이션 
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        # 애니메이션 곡선을 설정하십시오 
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(4000)  # 4 초 이내에 완료되었습니다 
        # 움직이는 애니메이션 
        moveAnimation = QPropertyAnimation(self, b"pos")
        moveAnimation.setStartValue(startPos)
        moveAnimation.setEndValue(endPos)
        moveAnimation.setEasingCurve(QEasingCurve.InQuad)
        moveAnimation.setDuration(5000)  # 5 초 이내에 완료되었습니다 
        # 병렬 애니메이션 그룹 (목적은 위의 두 애니메이션을 설정하는 것입니다) 
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(moveAnimation)
        self.animationGroup.finished.connect(self.close)  # 애니메이션의 끝에 창을 닫습니다 
        self.animationGroup.start()

    def paintEvent(self, event):
        super(BubbleLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티 앨리어싱 

        rectPath = QPainterPath()  # 둥근 사각형 
        triPath = QPainterPath()  # 하단 삼각형 

        height = self.height() - 8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 5, 5)
        x = self.width() / 5 * 4
        triPath.moveTo(x, height)  # 아래쪽 수평선 4/5로 이동하십시오 
        # 화면 삼각형 
        triPath.lineTo(x + 6, height + 8)
        triPath.lineTo(x + 12, height)

        rectPath.addPath(triPath)  # 이전 사각형에 삼각형을 추가하십시오 

        # 테두리 브러쉬 
        painter.setPen(QPen(self.BorderColor, 1, Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        # 배경 그림 브러시 
        painter.setBrush(self.BackgroundColor)
        # 모양의 모양 
        painter.drawPath(rectPath)
        # 三 边 边 边保 
        painter.setPen(QPen(self.BackgroundColor, 1,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(x, height, x + 12, height)

    def windowOpacity(self):
        return super(BubbleLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(BubbleLabel, self).setWindowOpacity(opacity)

    # 불투명도 속성으로 인해 qwidget에서 하나를 재정의 할 필요가 없습니다. 
    opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)


class TestWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.msgEdit = QLineEdit(self, returnPressed=self.onMsgShow)
        self.msgButton = QPushButton("显示内容", self, clicked=self.onMsgShow)
        layout.addWidget(self.msgEdit)
        layout.addWidget(self.msgButton)

    def onMsgShow(self):
        msg = self.msgEdit.text().strip()
        if not msg:
            return
        if hasattr(self, "_blabel"):
            self._blabel.stop()
            self._blabel.deleteLater()
            del self._blabel
        self._blabel = BubbleLabel()
        self._blabel.setText(msg)
        self._blabel.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWidget()
    w.show()
    sys.exit(app.exec_())
