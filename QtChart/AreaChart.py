#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/10/2
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: AreaChart
@description: 区域图表
"""
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QAreaSeries
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QGradient, QLinearGradient, QPainter, QPen


class Window(QChartView):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 300)
        # 抗锯 齿齿 
        self.setRenderHint(QPainter.Antialiasing)

        # 图片 
        chart = QChart()
        self.setChart(chart)
        # 제목을 설정하십시오 
        chart.setTitle('Simple areachart example')
        # 加 ses. 
        chart.addSeries(self.getSeries())
        # 기본 축을 만듭니다 
        chart.createDefaultAxes()
        # xy 축의 범위를 설정하십시오 
        chart.axisX().setRange(0, 20)
        chart.axisY().setRange(0, 10)

    def getSeries(self):
        # 생성 시리즈 
        series0 = QLineSeries(self)
        series1 = QLineSeries(self)

        # 데이터 추가 
        series0 << QPointF(1, 5) << QPointF(3, 7) << QPointF(7, 6) << QPointF(9, 7) \
                << QPointF(12, 6) << QPointF(16, 7) << QPointF(18, 5)
        series1 << QPointF(1, 3) << QPointF(3, 4) << QPointF(7, 3) << QPointF(8, 2) \
                << QPointF(12, 3) << QPointF(16, 4) << QPointF(18, 3)

        # 지역 맵을 만드십시오 
        series = QAreaSeries(series0, series1)
        series.setName('Batman')

        #부시 
        pen = QPen(0x059605)
        pen.setWidth(3)
        series.setPen(pen)

        # 회화 브러시를 설정합니다 
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(0x3cc63c))
        gradient.setColorAt(1.0, QColor(0x26f626))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        series.setBrush(gradient)

        return series


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
