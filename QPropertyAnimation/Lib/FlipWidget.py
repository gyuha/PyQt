#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: FlipWidget
@description: 动画翻转窗口
"""
from PyQt5.QtCore import pyqtSignal, Qt, QPropertyAnimation, QEasingCurve,\
    pyqtProperty, QPointF
from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtWidgets import QWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class FlipWidget(QWidget):

    Left = 0                        # 오른쪽에서 
    Right = 1                       # 왼쪽에서 오른쪽으로 
    Scale = 3                       # 이미지 줌 비율 
    finished = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(FlipWidget, self).__init__(*args, **kwargs)
        # 无球 无 无 任 
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint | Qt.SubWindow)
        # 배경 투명 
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 翻 翻 
        self._angle = 0
        # Custom Attributes` Angle`의 속성 애니메이션 
        self._animation = QPropertyAnimation(self, b'angle', self)
        self._animation.setDuration(550)
        self._animation.setEasingCurve(QEasingCurve.OutInQuad)
        self._animation.finished.connect(self.finished.emit)

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self.update()

    def updateImages(self, direction, image1, image2):
        """设置两张切换图
        :param direction:        方向
        :param image1:           图片1
        :param image2:           图片2
        """
        self.image1 = image1
        self.image2 = image2
        self.show()
        self._angle = 0
        # 방향에 따라 애니메이션의 초기 및 최종 값 설정 
        if direction == self.Right:
            self._animation.setStartValue(1)
            self._animation.setEndValue(-180)
        elif direction == self.Left:
            self._animation.setStartValue(1)
            self._animation.setEndValue(180)
        self._animation.start()

    def paintEvent(self, event):
        super(FlipWidget, self).paintEvent(event)

        if hasattr(self, 'image1') and hasattr(self, 'image2') and self.isVisible():

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            # # 变 
            transform = QTransform()
            # 센터를 사각형 센터로 설정하십시오 
            transform.translate(self.width() / 2, self.height() / 2)

            if self._angle >= -90 and self._angle <= 90:
                # 플립 각도가 범위의 첫 번째 그림과 큰 이미지에서 작은 이미지로 프로세스를 표시 할 때 # 
                painter.save()
                # 플립 각을 설정하십시오 
                transform.rotate(self._angle, Qt.YAxis)
                painter.setTransform(transform)
                # 줌 사진 높이 
                width = self.image1.width() / 2
                height = int(self.image1.height() *
                             (1 - abs(self._angle / self.Scale) / 100))
                image = self.image1.scaled(
                    self.image1.width(), height,
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(
                    QPointF(-width, -height / 2), image)
                painter.restore()
            else:
                # 플립 각도가 90 범위의 두 번째 그림을 표시하고 작은 그림에서 원본 이미지로 확대되는 프로세스 
                painter.save()
                if self._angle > 0:
                    angle = 180 + self._angle
                else:
                    angle = self._angle - 180
                # 플립 각을 설정 하고이 각도 차이에주의하십시오. 
                transform.rotate(angle, Qt.YAxis)
                painter.setTransform(transform)
                # 줌 사진 높이 
                width = self.image2.width() / 2
                height = int(self.image2.height() *
                             (1 - ((360 - abs(angle)) / self.Scale / 100)))
                image = self.image2.scaled(
                    self.image2.width(), height,
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(
                    QPointF(-width, -height / 2), image)
                painter.restore()
