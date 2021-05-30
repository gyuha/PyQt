#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月19日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, http://coding.net/u/892768447, http://github.com/892768447
@email: 892768447@qq.com
@file: CustomXYaxis
@description: 
'''
import random
import sys

from PyQt5.QtChart import QChartView, QLineSeries, QChart, QCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

__version__ = "0.0.1"

m_listCount = 3
m_valueMax = 10
m_valueCount = 7


def generateRandomData(listCount, valueMax, valueCount):
    random.seed()
    dataTable = []
    for i in range(listCount):
        dataList = []
        yValue = 0.0
        f_valueCount = float(valueCount)
        for j in range(valueCount):
            yValue += random.uniform(0, valueMax) / f_valueCount
            value = j + random.random() * m_valueMax / f_valueCount, yValue
            label = "Slice " + str(i) + ":" + str(j)
            dataList.append((value, label))
        dataTable.append(dataList)
    return dataTable


m_dataTable = generateRandomData(m_listCount, m_valueMax, m_valueCount)


def getChart(title):
    chart = QChart(title=title)
    for i, data_list in enumerate(m_dataTable):
        series = QLineSeries(chart)
        for value, _ in data_list:
            series.append(*value)
        series.setName("Series " + str(i))
        chart.addSeries(series)
    chart.createDefaultAxes()  # 기본 축을 만듭니다 
    return chart


def customAxisX(chart):
    # 사용자 정의 X 축 (000) 
    series = chart.series()
    if not series:
        return
    axisx = QCategoryAxis(
        chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
    minx = chart.axisX().min()
    maxx = chart.axisX().max()
    tickc = chart.axisX().tickCount()
    if tickc < 2:
        axisx.append("lable0", minx)
    else:
        step = (maxx - minx) / (tickc - 1)  # tickc>=2
        for i in range(0, tickc):
            axisx.append("lable%s" % i, minx + i * step)
    chart.setAxisX(axisx, series[-1])


def customTopAxisX(chart):
    # 사용자 정의 탑 x 축 
    series = chart.series()
    if not series:
        return
    category = ["%d月" % i for i in range(1, 9)]  # 1 1 8 1. 
    axisx = QCategoryAxis(
        chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
    axisx.setGridLineVisible(False)  # 숨겨진 격자 선 
    axisx.setTickCount(len(category))  # 포인트 수를 설정하십시오 
    chart.axisX().setTickCount(len(category))  # x 축에 대한 스케일 번호 수를 적용합니다. 
    minx = chart.axisX().min()
    maxx = chart.axisX().max()
    tickc = chart.axisX().tickCount()
    step = (maxx - minx) / (tickc - 1)  # tickc>=2
    for i in range(0, tickc):
        axisx.append(category[i], minx + i * step)
    chart.addAxis(axisx, Qt.AlignTop)  # 오른쪽에 추가하십시오 
    series[-1].attachAxis(axisx)  # 附 到 s 上. 


def customAxisY(chart):
    # 사용자 정의 Y 축 (불평등) 
    series = chart.series()
    if not series:
        return
    category = ["周一", "周二", "周三", "周四",
                "周五", "周六", "周日"]
    axisy = QCategoryAxis(
        chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
    axisy.setGridLineVisible(False)  # 숨겨진 격자 선 
    axisy.setTickCount(len(category))  # 포인트 수를 설정하십시오 
    miny = chart.axisY().min()
    maxy = chart.axisY().max()
    tickc = axisy.tickCount()
    if tickc < 2:
        axisy.append(category[0])
    else:
        step = (maxy - miny) / (tickc - 1)  # tickc>=2
        for i in range(0, tickc):
            axisy.append(category[i], miny + i * step)
    chart.addAxis(axisy, Qt.AlignRight)  # 오른쪽에 추가하십시오 
    series[-1].attachAxis(axisy)  # 附 到 s 上. 


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        # x 축을 사용자 정의하십시오 (원래 x 축 값에 해당). 
        chart = getChart("自定义x轴(和原来的x轴值对应等分)")
        customAxisX(chart)
        layout.addWidget(QChartView(chart, self))
        # 사용자 정의 오른쪽 축을 추가 (왼쪽에 해당하는 분취 량) 
        chart = getChart("自定义添加右侧y轴(等分,与左侧不对应)")
        customAxisY(chart)
        layout.addWidget(QChartView(chart, self))
        # 맞춤형 탑 x 축 (새로운 x 축으로 나눈) 
        chart = getChart("自定义top x轴(按现有新的x轴划分)")
        customTopAxisX(chart)
        layout.addWidget(QChartView(chart, self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = Window()
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
