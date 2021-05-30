#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月28日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: charts.bar.BarStack
@description: like http://echarts.baidu.com/demo.html#bar-stack
'''

import sys
from random import randint

from PyQt5.QtChart import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsLineItem, QWidget, \
    QHBoxLayout, QLabel, QVBoxLayout, QGraphicsProxyWidget

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):

    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50, 50, 50, 100);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, bars):
        self.titleLabel.setText(title)
        for bar, value in bars:
            if bar not in self.Cache:
                item = ToolTipItem(
                    bar.color(),
                    (bar.label() or "-") + ":" + str(value), self)
                self.layout().addWidget(item)
                self.Cache[bar] = item
            else:
                self.Cache[bar].setText(
                    (bar.label() or "-") + ":" + str(value))
            brush = bar.brush()
            color = brush.color()
            self.Cache[bar].setVisible(color.alphaF() == 1.0)  # 사용할 수없는 항목을 숨 깁니다 
        self.adjustSize()  # 크기 조정 


class GraphicsProxyWidget(QGraphicsProxyWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def width(self):
        return self.size().width()

    def height(self):
        return self.size().height()

    def show(self, title, bars, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, bars)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯 齿齿 
        self.initChart()

        # 提 위젯 
        self.toolTipWidget = GraphicsProxyWidget(self._chart)

        # 선 너비를 조정해야합니다 
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        # 일부 고정 계산, mouseMoveEvent의 계산량을 줄입니다. 
        # x 및 y 축의 최대 최대 값을 얻습니다. 
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.category_len = len(axisX.categories())
        self.min_x, self.max_x = -0.5, self.category_len - 0.5
        self.min_y, self.max_y = axisY.min(), axisY.max()
        # 上 上 上 上 上 上 上 
        self.point_top = self._chart.mapToPosition(
            QPointF(self.min_x, self.max_y))

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 마우스 위치를 해당 XY 값으로 변환하십시오. 
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round(x)
        # 좌표계에서 모든 막대의 유형과 지점을 가져옵니다. 
        serie = self._chart.series()[0]
        bars = [(bar, bar.at(index))
                for bar in serie.barSets() if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y]
#         print(bars)
        if bars:
            right_top = self._chart.mapToPosition(
                QPointF(self.max_x, self.max_y))
            # 等 分 비율 
            step_x = round(
                (right_top.x() - self.point_top.x()) / self.category_len)
            posx = self._chart.mapToPosition(QPointF(x, self.min_y))
            self.lineItem.setLine(posx.x(), self.point_top.y(),
                                  posx.x(), posx.y())
            self.lineItem.show()
            try:
                title = self.categories[index]
            except:
                title = ""
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            # 오른쪽에서의 거리가 팁 너비보다 작 으면 
            x = pos.x() - t_width if self.width() - \
                pos.x() - 20 < t_width else pos.x()
            # 하단의 높은 높이가 팁 높이보다 작은 경우 # 
            y = pos.y() - t_height if self.height() - \
                pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(
                title, bars, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def handleMarkerClicked(self):
        marker = self.sender()  # 신호 보낸 사람 
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        #bar 투명성 
        brush = bar.brush()
        color = brush.color()
        alpha = 0.0 if color.alphaF() == 1.0 else 1.0
        color.setAlphaF(alpha)
        brush.setColor(color)
        bar.setBrush(brush)
        # marker
        brush = marker.labelBrush()
        color = brush.color()
        alpha = 0.4 if color.alphaF() == 1.0 else 1.0
        # 레이블의 투명도를 설정하십시오 
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)
        # 마커의 투명도를 설정하십시오 
        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)

    def handleMarkerHovered(self, status):
        # 바의 브러시 너비를 설정합니다 
        marker = self.sender()  # 신호 보낸 사람 
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def handleBarHoverd(self, status, index):
        # 바의 브러시 너비를 설정합니다 
        bar = self.sender()  # 신호 보낸 사람 
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def initChart(self):
        self._chart = QChart(title="柱状图堆叠")
        self._chart.setAcceptHoverEvents(True)
        # 시리즈 애니메이션 
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self.categories = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        names = ["邮件营销", "联盟广告", "视频广告", "直接访问", "搜索引擎"]
        series = QBarSeries(self._chart)
        for name in names:
            bar = QBarSet(name)
            # 랜덤 데이터 
            for _ in range(7):
                bar.append(randint(0, 10))
            series.append(bar)
            bar.hovered.connect(self.handleBarHoverd)  # 
        self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 기본 축을 만듭니다 
        # x 축 
        axis_x = QBarCategoryAxis(self._chart)
        axis_x.append(self.categories)
        self._chart.setAxisX(axis_x, series)
        # 차트의 전설 
        legend = self._chart.legend()
        legend.setVisible(True)
        # 전설에서 표시를 거래하고 신호를 바인딩합니다. 
        for marker in legend.markers():
            # 点击 事 事 
            marker.clicked.connect(self.handleMarkerClicked)
            # 事 事 事 
            marker.hovered.connect(self.handleMarkerHovered)
        self.setChart(self._chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ChartView()
    view.show()
    sys.exit(app.exec_())
