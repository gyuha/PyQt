#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年5月15日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: PaintQSlider
@description: 
"""
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QSlider, QWidget, QVBoxLayout, QProxyStyle, QStyle,\
    QStyleOptionSlider


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class SliderStyle(QProxyStyle):

    def subControlRect(self, control, option, subControl, widget=None):
        rect = super(SliderStyle, self).subControlRect(
            control, option, subControl, widget)
        if subControl == QStyle.SC_SliderHandle:
            if option.orientation == Qt.Horizontal:
                # 高度 1/3. 
                radius = int(widget.height() / 3)
                offset = int(radius / 3)
                if option.state & QStyle.State_MouseOver:
                    x = min(rect.x() - offset, widget.width() - radius)
                    x = x if x >= 0 else 0
                else:
                    radius = offset
                    x = min(rect.x(), widget.width() - radius)
                rect = QRect(x, int((rect.height() - radius) / 2),
                             radius, radius)
            else:
                # 너비 1/3. 
                radius = int(widget.width() / 3)
                offset = int(radius / 3)
                if option.state & QStyle.State_MouseOver:
                    y = min(rect.y() - offset, widget.height() - radius)
                    y = y if y >= 0 else 0
                else:
                    radius = offset
                    y = min(rect.y(), widget.height() - radius)
                rect = QRect(int((rect.width() - radius) / 2),
                             y, radius, radius)
            return rect
        return rect


class PaintQSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super(PaintQSlider, self).__init__(*args, **kwargs)
        # 프록시 스타일을 설정하십시오. 주로 마우스 클릭 영역을 계산하고 해결하는 데 사용됩니다. 
        self.setStyle(SliderStyle())

    def paintEvent(self, _):
        option = QStyleOptionSlider()
        self.initStyleOption(option)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 中 の 위치 
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)

        # の 中 の の 线 
        painter.setPen(Qt.white)
        painter.setBrush(Qt.white)
        if self.orientation() == Qt.Horizontal:
            y = self.height() / 2
            painter.drawLine(QPointF(0, y), QPointF(self.width(), y))
        else:
            x = self.width() / 2
            painter.drawLine(QPointF(x, 0), QPointF(x, self.height()))
        # 画 圆 
        painter.setPen(Qt.NoPen)
        if option.state & QStyle.State_MouseOver:  # double circle. 
            # 半 透 透 透 大. 
            r = rect.height() / 2
            painter.setBrush(QColor(255, 255, 255, 100))
            painter.drawRoundedRect(rect, r, r)
            # 实心 센트 (위쪽 및 아래쪽 및 오른쪽 오프셋 4) 
            rect = rect.adjusted(4, 4, -4, -4)
            r = rect.height() / 2
            painter.setBrush(QColor(255, 255, 255, 255))
            painter.drawRoundedRect(rect, r, r)
            # 文 
            painter.setPen(Qt.white)
            if self.orientation() == Qt.Horizontal:  # 위의 텍스트를 그립니다 
                x, y = rect.x(), rect.y() - rect.height() - 2
            else:  # 왼쪽에 텍스트를 그립니다 
                x, y = rect.x() - rect.width() - 2, rect.y()
            painter.drawText(
                x, y, rect.width(), rect.height(),
                Qt.AlignCenter, str(self.value())
            )
        else:  # 实心 圆 
            r = rect.height() / 2
            painter.setBrush(Qt.white)
            painter.drawRoundedRect(rect, r, r)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(self)
        layout.addWidget(PaintQSlider(Qt.Vertical, self, minimumWidth=90))
        layout.addWidget(PaintQSlider(Qt.Horizontal, self, minimumHeight=90))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.setStyleSheet('QWidget {background: gray;}')
    w.show()
    sys.exit(app.exec_())
