#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/10/2
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: SplineChart
@description: 样条图表
"""
from PyQt5.QtChart import QChartView, QChart, QSplineSeries
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter


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
        chart.setTitle('Simple splinechart example')
        # 加 ses. 
        self.getSeries(chart)
        # 기본 XY 축을 만듭니다 
        chart.createDefaultAxes()
        chart.legend().setVisible(False)

    def getSeries(self, chart):
        # 첫 번째 그룹 
        series = QSplineSeries(chart)
        series << QPointF(1, 5) << QPointF(3, 7) << QPointF(7, 6) << QPointF(9, 7) \
        << QPointF(12, 6) << QPointF(16, 7) << QPointF(18, 5)
        chart.addSeries(series)

        # 두 번째 그룹 
        series = QSplineSeries(chart)
        series << QPointF(1, 3) << QPointF(3, 4) << QPointF(7, 3) << QPointF(8, 2) \
        << QPointF(12, 3) << QPointF(16, 4) << QPointF(18, 3)
        chart.addSeries(series)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
