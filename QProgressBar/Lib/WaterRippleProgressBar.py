#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2018 년 4 월 1 일에 작성되었습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: WaterRippleProgressBar
# description:

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0

import math

from PyQt5.QtCore import QTimer, Qt, QRectF, QSize
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont
from PyQt5.QtWidgets import QProgressBar


class WaterRippleProgressBar(QProgressBar):

    # 高 % 
    waterHeight = 1
    # 밀도 
    waterDensity = 1
    # 样 1은 직사각형, 0은 둥글다 
    styleType = 1
    # 文 
    textColor = Qt.white
    # 배경색 
    backgroundColor = Qt.gray
    # 물결 모양의 색상 1. 
    waterColor1 = QColor(33, 178, 148)
    # 물결 모양의 색깔 2. 
    waterColor2 = QColor(33, 178, 148, 100)

    def __init__(self, *args, **kwargs):
        super(WaterRippleProgressBar, self).__init__(*args, **kwargs)
        self._offset = 0
        # 100ms마다 파도를 새로 고침하십시오 (시뮬레이션 된 웨이브 역학) 
        self._updateTimer = QTimer(self, timeout=self.update)
        self._updateTimer.start(100)

    def setRange(self, minValue, maxValue):
        if minValue == maxValue == 0:
            return  # 不 设置 b 状态. 
        super(WaterRippleProgressBar, self).setRange(minValue, maxValue)

    def setMinimum(self, value):
        if value == self.maximum() == 0:
            return  # 不 设置 b 状态. 
        super(WaterRippleProgressBar, self).setMinimum(value)

    def setMaximum(self, value):
        if value == self.minimum() == 0:
            return  # 不 设置 b 状态. 
        super(WaterRippleProgressBar, self).setMaximum(value)

    def setWaterHeight(self, height):
        """设置浪高"""
        self.waterHeight = height
        self.update()

    def setWaterDensity(self, density):
        """设置密度"""
        self.waterDensity = density
        self.update()

    def setStyleType(self, style):
        """设置类型"""
        self.styleType = style
        self.update()

    def sizeHint(self):
        return QSize(100, 100)

    def paintEvent(self, event):
        if self.minimum() == self.maximum() == 0:
            return
        # 正弦 公 公 公 y = a * sin (ωx + φ) + k 
        # 当前 值 值 所 
        percent = 1 - (self.value() - self.minimum()) / \
            (self.maximum() - self.minimum())
        # W 표현주기, 6은 정의입니다. 
        w = 6 * self.waterDensity * math.pi / self.width()
        # 진폭 높이 백분율, 1/26은 정의입니다. 
        A = self.height() * self.waterHeight * 1 / 26
        # k 높이 백분율 
        k = self.height() * percent

        # wave 1 
        waterPath1 = QPainterPath()
        waterPath1.moveTo(0, self.height())  # 시작점이 왼쪽 하단에 있습니다. 
        # wave 2 
        waterPath2 = QPainterPath()
        waterPath2.moveTo(0, self.height())  # 시작점이 왼쪽 하단에 있습니다. 

        # 오프셋 
        self._offset += 0.6
        if self._offset > self.width() / 2:
            self._offset = 0

        for i in range(self.width() + 1):
            # x 축에서 y 축 지점을 계산합니다. 
            y = A * math.sin(w * i + self._offset) + k
            waterPath1.lineTo(i, y)

            # 相 第一 第一 第一 需要 错 错 
            y = A * math.sin(w * i + self._offset + self.width() / 2 * A) + k
            waterPath2.lineTo(i, y)

        # 두 파도를 닫고 U 형으로 닫힌 간격을 형성합니다. 
        waterPath1.lineTo(self.width(), self.height())
        waterPath1.lineTo(0, self.height())
        waterPath2.lineTo(self.width(), self.height())
        waterPath2.lineTo(0, self.height())

        # 整体 모양 (직사각형 또는 원형) 
        bgPath = QPainterPath()
        if self.styleType:
            bgPath.addRect(QRectF(self.rect()))
        else:
            radius = min(self.width(), self.height())
            bgPath.addRoundedRect(QRectF(self.rect()), radius, radius)

        # 경로를 시작하십시오 
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 브러쉬 설정 설정 
        painter.setPen(Qt.NoPen)

        if not self.styleType:
            # round. 
            painter.setClipPath(bgPath)

        # 先 整 背景 背景 背景, 그런 다음 배경에 두 개의 파도를 그립니다. 
        painter.save()
        painter.setBrush(self.backgroundColor)
        painter.drawPath(bgPath)
        painter.restore()

        # wave 1 
        painter.save()
        painter.setBrush(self.waterColor1)
        painter.drawPath(waterPath1)
        painter.restore()

        # wave 2 
        painter.save()
        painter.setBrush(self.waterColor2)
        painter.drawPath(waterPath2)
        painter.restore()

        # 文 
        if not self.isTextVisible():
            return
        painter.setPen(self.textColor)
        font = self.font() or QFont()
        font.setPixelSize(int(min(self.width(), self.height()) / 2))
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, '%d%%' %
                         (self.value() / self.maximum() * 100))
