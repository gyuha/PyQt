#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/10/2
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: PieChart
@description: 饼状图表
"""
from PyQt5.QtChart import QChartView, QChart, QPieSeries
from PyQt5.QtGui import QPainter, QColor


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
        chart.setTitle('Simple piechart example')
        # 加 ses. 
        chart.addSeries(self.getSeries())

    def getSeries(self):
        series = QPieSeries()
        slice0 = series.append('10%', 1)
        series.append('20%', 2)
        series.append('70%', 7)
        # 레이블 텍스트 표시 
        series.setLabelsVisible()
        series.setPieSize(0.5)
        # 첫 번째 블록을 제거하십시오 
        slice0.setLabelVisible()
        slice0.setExploded()
        # 첫 번째 색상을 설정하십시오 
        slice0.setColor(QColor(255, 0, 0, 100))
        return series


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
