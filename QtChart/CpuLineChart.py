#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/5/13
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: CpuLineChart
@description: 
"""

import sys

from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication
from psutil import cpu_percent


class CpuLineChart(QChart):

    def __init__(self, *args, **kwargs):
        super(CpuLineChart, self).__init__(*args, **kwargs)
        self.m_count = 10
        # 隐 图 
        self.legend().hide()
        self.m_series = QSplineSeries(self)
        # 설치 브러시 
        self.m_series.setPen(QPen(QColor('#3B8CFF'), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.addSeries(self.m_series)
        # x 축 
        self.m_axisX = QDateTimeAxis(self)
        self.m_axisX.setTickCount(self.m_count + 1)  # 분 수를 설정합니다 
        self.m_axisX.setFormat('hh:mm:ss')  # 시간 표시 형식을 설정하십시오 
        now = QDateTime.currentDateTime()  # 前 10 초 
        self.m_axisX.setRange(now.addSecs(-self.m_count), now)
        self.addAxis(self.m_axisX, Qt.AlignBottom)
        self.m_series.attachAxis(self.m_axisX)
        # y. 
        self.m_axisY = QValueAxis(self)
        self.m_axisY.setLabelFormat('%d')  # 텍스트 형식을 설정합니다 
        self.m_axisY.setMinorTickCount(4)  # 작은 타이 선의 수를 설정하십시오 
        self.m_axisY.setTickCount(self.m_count + 1)
        self.m_axisY.setRange(0, 100)
        self.addAxis(self.m_axisY, Qt.AlignLeft)
        self.m_series.attachAxis(self.m_axisY)

        # 11 초기 점을 채우고, X 축의 시간 소인에주의를 기울여 두 번째로 변환해야합니다. 
        self.m_series.append(
            [QPointF(now.addSecs(-i).toMSecsSinceEpoch(), 0) for i in range(self.m_count, -1, -1)])

        # 타이머 데이터 가져 오기 
        self.m_timer = QTimer()
        self.m_timer.timeout.connect(self.update_data)
        self.m_timer.start(1000)

    def update_data(self):
        value = cpu_percent()
        now = QDateTime.currentDateTime()
        self.m_axisX.setRange(now.addSecs(-self.m_count), now)  # x 축의 시간 범위를 다시 조정합니다. 
        # 모든 포인트 가져 오기, 먼저 제거하고 새 것을 추가하십시오. 
        points = self.m_series.pointsVector()
        points.pop(0)
        points.append(QPointF(now.toMSecsSinceEpoch(), value))
        # 换 法 速 
        self.m_series.replace(points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chart = CpuLineChart()
    chart.setTitle('cpu')
    # chart.setAnimationOptions(QChart.SeriesAnimations)

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯 齿齿 
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
