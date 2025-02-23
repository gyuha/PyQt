#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月5日
@author: Yimelia
@site: https://github.com/yimelia
@file: DynamicSpline
@description: This example shows how to draw dynamic data. https://doc.qt.io/qt-5/qtcharts-dynamicspline-example.html
"""
import sys

from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
from PyQt5.QtCore import Qt, QTimer, QRandomGenerator
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication

__version__ = "0.0.1"


class DynamicSpline(QChart):
    def __init__(self):
        super().__init__()
        self.m_step = 0
        self.m_x = 5
        self.m_y = 1
        # 이미지를 초기화하십시오 
        self.series = QSplineSeries(self)
        green_pen = QPen(Qt.red)
        green_pen.setWidth(3)
        self.series.setPen(green_pen)
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        self.series.append(self.m_x, self.m_y)

        self.addSeries(self.series)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)
        self.axisX.setTickCount(5)
        self.axisX.setRange(0, 10)
        self.axisY.setRange(-5, 10)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start()

    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y
        # PYQT5.11.3 이상에서 QRandomGenerator.Global ()은 global_ ()로 변경됩니다. 
        self.m_y = QRandomGenerator.global_().bounded(5) - 2.5
        self.series.append(self.m_x, self.m_y)
        self.scroll(x, 0)
        if self.m_x >= 100:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chart = DynamicSpline()
    chart.setTitle("Dynamic spline chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯 齿齿 
    view.resize(400, 300)
    view.show()
    sys.exit(app.exec_())
