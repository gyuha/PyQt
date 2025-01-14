#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月28日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: charts.line.LineStack
@description: like http://echarts.baidu.com/demo.html#line-stack
'''

import sys

from PyQt5.QtChart import QChartView, QChart, QLineSeries, QLegend, \
    QCategoryAxis
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

    def updateUi(self, title, points):
        self.titleLabel.setText(title)
        for serie, point in points:
            if serie not in self.Cache:
                item = ToolTipItem(
                    serie.color(),
                    (serie.name() or "-") + ":" + str(point.y()), self)
                self.layout().addWidget(item)
                self.Cache[serie] = item
            else:
                self.Cache[serie].setText(
                    (serie.name() or "-") + ":" + str(point.y()))
            self.Cache[serie].setVisible(serie.isVisible())  # 사용할 수없는 항목을 숨 깁니다 
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

    def show(self, title, points, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, points)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯 齿齿 
        # 사용자 정의 x 축 레이블 
        self.category = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        self.initChart()

        # 提 위젯 
        self.toolTipWidget = GraphicsProxyWidget(self._chart)

        # line
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        # 일부 고정 계산, mouseMoveEvent의 계산량을 줄입니다. 
        # x 및 y 축의 최대 최대 값을 얻습니다. 
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.min_x, self.max_x = axisX.min(), axisX.max()
        self.min_y, self.max_y = axisY.min(), axisY.max()

    def resizeEvent(self, event):
        super(ChartView, self).resizeEvent(event)
        # 창 크기가 변경되면 다시 계산됩니다 
        # 上 上 上 上 上 上 上 
        self.point_top = self._chart.mapToPosition(
            QPointF(self.min_x, self.max_y))
        # 坐 原 原 点 
        self.point_bottom = self._chart.mapToPosition(
            QPointF(self.min_x, self.min_y))
        self.step_x = (self.max_x - self.min_x) / \
            (self._chart.axisX().tickCount() - 1)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 마우스 위치를 해당 XY 값으로 변환하십시오. 
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round((x - self.min_x) / self.step_x)
        # 좌표계에서 모든 일반 시리즈의 유형과 지점을 얻으십시오. 
        points = [(serie, serie.at(index))
                  for serie in self._chart.series()
                  if self.min_x <= x <= self.max_x and
                  self.min_y <= y <= self.max_y]
        if points:
            pos_x = self._chart.mapToPosition(
                QPointF(index * self.step_x + self.min_x, self.min_y))
            self.lineItem.setLine(pos_x.x(), self.point_top.y(),
                                  pos_x.x(), self.point_bottom.y())
            self.lineItem.show()
            try:
                title = self.category[index]
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
                title, points, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def handleMarkerClicked(self):
        marker = self.sender()  # 신호 보낸 사람 
        if not marker:
            return
        visible = not marker.series().isVisible()
# # 숨기기 또는 시리즈 
        marker.series().setVisible(visible)
        marker.setVisible(True)  # 마커가 항상 표시되었는지 확인하십시오 
        # 透 透 
        alpha = 1.0 if visible else 0.4
        # 레이블의 투명도를 설정하십시오 
        brush = marker.labelBrush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)
        # 마커의 투명도를 설정하십시오 
        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)
        # 브러시 투명도를 설정하십시오 
        pen = marker.pen()
        color = pen.color()
        color.setAlphaF(alpha)
        pen.setColor(color)
        marker.setPen(pen)

    def handleMarkerHovered(self, status):
        # 시리즈의 브러시 너비를 설정하십시오 
        marker = self.sender()  # 신호 보낸 사람 
        if not marker:
            return
        series = marker.series()
        if not series:
            return
        pen = series.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        series.setPen(pen)

    def handleSeriesHoverd(self, point, state):
        # 시리즈의 브러시 너비를 설정하십시오 
        series = self.sender()  # 신호 보낸 사람 
        pen = series.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if state else -1))
        series.setPen(pen)

    def initChart(self):
        self._chart = QChart(title="折线图堆叠")
        self._chart.setAcceptHoverEvents(True)
        # 시리즈 애니메이션 
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        dataTable = [
            ["邮件营销", [120, 132, 101, 134, 90, 230, 210]],
            ["联盟广告", [220, 182, 191, 234, 290, 330, 310]],
            ["视频广告", [150, 232, 201, 154, 190, 330, 410]],
            ["直接访问", [320, 332, 301, 334, 390, 330, 320]],
            ["搜索引擎", [820, 932, 901, 934, 1290, 1330, 1320]]
        ]
        for series_name, data_list in dataTable:
            series = QLineSeries(self._chart)
            for j, v in enumerate(data_list):
                series.append(j, v)
            series.setName(series_name)
            series.setPointsVisible(True)  # 점을 표시합니다 
            series.hovered.connect(self.handleSeriesHoverd)  # 
            self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 기본 축을 만듭니다 
        axisX = self._chart.axisX()  # x 축 
        axisX.setTickCount(7)  # x 축 설정 7 스케일 
        axisX.setGridLineVisible(False)  # x 축에서 선을 숨 깁니다 
        axisY = self._chart.axisY()
        axisY.setTickCount(7)  # 샤프트 설정 7 스케일 
        axisY.setRange(0, 1500)  # y 축 범위를 설정합니다 
        # 사용자 정의 x 축 
        axis_x = QCategoryAxis(
            self._chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
        axis_x.setTickCount(7)
        axis_x.setGridLineVisible(False)
        min_x = axisX.min()
        max_x = axisX.max()
        step = (max_x - min_x) / (7 - 1)  # 7 틱 
        for i in range(0, 7):
            axis_x.append(self.category[i], min_x + i * step)
        self._chart.setAxisX(axis_x, self._chart.series()[-1])
        # 차트의 전설 
        legend = self._chart.legend()
        # 스타일을 결정하기 위해 시리즈로 전설을 설정하십시오. 
        legend.setMarkerShape(QLegend.MarkerShapeFromSeries)
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
