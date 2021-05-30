#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/10/2
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: PercentBarChart
@description: 百分比柱状图表
"""
from PyQt5.QtChart import QChartView, QChart, QBarSet, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
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
        chart.setTitle('Simple percentbarchart example')
        # 애니메이션 효과를 엽니 다 
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # 加 ses. 
        series = self.getSeries()
        chart.addSeries(series)
        # 분류 
        categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        # 분류 된 X 축 
        axis = QBarCategoryAxis()
        axis.append(categories)
        # 기본 축을 만듭니다 
        chart.createDefaultAxes()
        # 기본 X 축장 
        chart.setAxisX(axis, series)
        # 전설 전설 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

    def getSeries(self):
        # 5 기둥을 만듭니다 
        set0 = QBarSet('Jane')
        set1 = QBarSet('John')
        set2 = QBarSet('Axel')
        set3 = QBarSet('Mary')
        set4 = QBarSet('Samantha')

        # 데이터 추가 
        set0 << 1 << 2 << 3 << 4 << 5 << 6
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2

        # 역사적인 스트립을 만드십시오 
        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
        return series


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
