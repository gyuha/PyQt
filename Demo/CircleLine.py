#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年3月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CircleLine
@description: 
"""

from math import floor, pi, cos, sin
from random import random, randint
from time import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

# 最 최소 및 최대 반경, 반경 임계 값 및 필링 라운드의 백분율 
radMin = 10
radMax = 80
filledCircle = 30  # 百 
concentricCircle = 60  # 同心 百 
radThreshold = 25  # IFF special, over this radius concentric, otherwise filled
# 최소 및 최대 이동 속도 
speedMin = 0.3
speedMax = 0.6
# 각 원과 퍼지 효과 
maxOpacity = 0.6

colors = [
    QColor(52, 168, 83),
    QColor(117, 95, 147),
    QColor(199, 108, 23),
    QColor(194, 62, 55),
    QColor(0, 172, 212),
    QColor(120, 120, 120)
]
circleBorder = 10
backgroundLine = colors[0]
backgroundColor = QColor(38, 43, 46)
backgroundMlt = 0.85

lineBorder = 2.5

# 가장 중요한 것은 전체 동그라미와 verrandars의 수 
maxCircles = 8
points = []

# 实实 변수 
circleExp = 1
circleExpMax = 1.003
circleExpMin = 0.997
circleExpSp = 0.00004
circlePulse = False

# <= x <= b를 임의의 정수를 생성합니다. 


def randint(a, b):
    return floor(random() * (b - a + 1) + a)

# 成 成 小 


def randRange(a, b):
    return random() * (b - a) + a

# 成成 등급 


def hyperRange(a, b):
    return random() * random() * random() * (b - a) + a


class Circle:

    def __init__(self, background, width, height):
        self.background = background
        self.x = randRange(-width / 2, width / 2)
        self.y = randRange(-height / 2, height / 2)
        self.radius = hyperRange(radMin, radMax)
        self.filled = (False if randint(
            0, 100) > concentricCircle else 'full') if self.radius < radThreshold else (
                False if randint(0, 100) > concentricCircle else 'concentric')
        self.color = colors[randint(0, len(colors) - 1)]
        self.borderColor = colors[randint(0, len(colors) - 1)]
        self.opacity = 0.05
        self.speed = randRange(speedMin, speedMax)  # * (radMin / self.radius)
        self.speedAngle = random() * 2 * pi
        self.speedx = cos(self.speedAngle) * self.speed
        self.speedy = sin(self.speedAngle) * self.speed
        spacex = abs((self.x - (-1 if self.speedx < 0 else 1) *
                      (width / 2 + self.radius)) / self.speedx)
        spacey = abs((self.y - (-1 if self.speedy < 0 else 1) *
                      (height / 2 + self.radius)) / self.speedy)
        self.ttl = min(spacex, spacey)


class CircleLineWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(CircleLineWindow, self).__init__(*args, **kwargs)
        # 배경색을 설정합니다 
        palette = self.palette()
        palette.setColor(palette.Background, backgroundColor)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        # 화면 크기를 얻으십시오 
        geometry = QApplication.instance().desktop().availableGeometry()
        self.screenWidth = geometry.width()
        self.screenHeight = geometry.height()
        self._canDraw = True
        self._firstDraw = True
        self._timer = QTimer(self, timeout=self.update)
        self.init()

    def init(self):
        points.clear()
        # 최소 거리 
        self.linkDist = min(self.screenWidth, self.screenHeight) / 2.4
        # 初 初 
        for _ in range(maxCircles * 3):
            points.append(Circle('', self.screenWidth, self.screenHeight))
        self.update()

    def showEvent(self, event):
        super(CircleLineWindow, self).showEvent(event)
        self._canDraw = True

    def hideEvent(self, event):
        super(CircleLineWindow, self).hideEvent(event)
        # 最 그리기를 중지하고 CPU 직업을 줄이는 최소화 
        self._canDraw = False

    def paintEvent(self, event):
        super(CircleLineWindow, self).paintEvent(event)
        if not self._canDraw:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.draw(painter)

    def draw(self, painter):
        if circlePulse:
            if circleExp < circleExpMin or circleExp > circleExpMax:
                circleExpSp *= -1
            circleExp += circleExpSp

        painter.translate(self.screenWidth / 2, self.screenHeight / 2)

        if self._firstDraw:
            t = time()
        self.renderPoints(painter, points)
        if self._firstDraw:
            self._firstDraw = False
            #이 비례 관계는 타이머의 시간을 설정하는 데 사용됩니다. 초기 창이 작 으면 비율이 없으면 애니메이션이 매우 빠릅니다. 
            t = (time() - t) * 1000 * 2
            # 比例 大 不 님의보기 1920/800. 
            t = int(min(2.4, self.screenHeight / self.height()) * t) - 1
            t = t if t > 15 else 15  # 不 能 15 초보 다 
            print('start timer(%d msec)' % t)
            # 开 时器 
            self._timer.start(t)

    def drawCircle(self, painter, circle):
        #         circle.radius *= circleExp
        if circle.background:
            circle.radius *= circleExp
        else:
            circle.radius /= circleExp
        radius = circle.radius

        r = radius * circleExp
        # 경계 색상 투명도 설정 
        c = QColor(circle.borderColor)
        c.setAlphaF(circle.opacity)

        painter.save()
        if circle.filled == 'full':
            # 배경 브러시를 설정합니다 
            painter.setBrush(c)
            painter.setPen(Qt.NoPen)
        else:
            # 설치 브러시 
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))

        # 画实 心 心 또는 서클 
        painter.drawEllipse(circle.x - r, circle.y - r, 2 * r, 2 * r)
        painter.restore()

        if circle.filled == 'concentric':
            r = radius / 2
            # 画 
            painter.save()
            painter.setBrush(Qt.NoBrush)
            painter.setPen(
                QPen(c, max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax))))
            painter.drawEllipse(circle.x - r, circle.y - r, 2 * r, 2 * r)
            painter.restore()

        circle.x += circle.speedx
        circle.y += circle.speedy
        if (circle.opacity < maxOpacity):
            circle.opacity += 0.01
        circle.ttl -= 1

    def renderPoints(self, painter, circles):
        for i, circle in enumerate(circles):
            if circle.ttl < -20:
                # 하나를 다시 초기화하십시오 
                circle = Circle('', self.screenWidth, self.screenHeight)
                circles[i] = circle
            self.drawCircle(painter, circle)

        circles_len = len(circles)
        for i in range(circles_len - 1):
            for j in range(i + 1, circles_len):
                deltax = circles[i].x - circles[j].x
                deltay = circles[i].y - circles[j].y
                dist = pow(pow(deltax, 2) + pow(deltay, 2), 0.5)
                # if the circles are overlapping, no laser connecting them
                if dist <= circles[i].radius + circles[j].radius:
                    continue
                # otherwise we connect them only if the dist is < linkDist
                if dist < self.linkDist:
                    xi = (1 if circles[i].x < circles[j].x else -
                          1) * abs(circles[i].radius * deltax / dist)
                    yi = (1 if circles[i].y < circles[j].y else -
                          1) * abs(circles[i].radius * deltay / dist)
                    xj = (-1 if circles[i].x < circles[j].x else 1) * \
                        abs(circles[j].radius * deltax / dist)
                    yj = (-1 if circles[i].y < circles[j].y else 1) * \
                        abs(circles[j].radius * deltay / dist)
                    path = QPainterPath()
                    path.moveTo(circles[i].x + xi, circles[i].y + yi)
                    path.lineTo(circles[j].x + xj, circles[j].y + yj)
#                     samecolor = circles[i].color == circles[j].color
                    c = QColor(circles[i].borderColor)
                    c.setAlphaF(min(circles[i].opacity, circles[j].opacity)
                                * ((self.linkDist - dist) / self.linkDist))
                    painter.setPen(QPen(c, (
                        lineBorder * backgroundMlt if circles[i].background else lineBorder) * (
                        (self.linkDist - dist) / self.linkDist)))
                    painter.drawPath(path)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CircleLineWindow()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec_())
