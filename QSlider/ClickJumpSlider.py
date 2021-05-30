#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月5日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: ClickJumpSlider
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle, QWidget,\
    QFormLayout, QLabel


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class ClickJumpSlider(QSlider):

    def mousePressEvent(self, event):
        # 获取 上 上 拉 块 위치 
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        if rect.contains(event.pos()):
            # 슬라이더를 마우스 클릭하는 위치가있는 경우 QT 셀프 처리로 손을 긋습니다. 
            super(ClickJumpSlider, self).mousePressEvent(event)
            return
        if self.orientation() == Qt.Horizontal:
            # 向, 인수 웨이브 칸아가 반전되었는지 여부를 고려해야합니까? 
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                event.x() if not self.invertedAppearance() else (self.width(
                ) - event.x()), self.width()))
        else:
            #ir. 
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance(
                ) else event.y(), self.height()))


class DemoWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(DemoWindow, self).__init__(*args, **kwargs)
        self.resize(600, 600)
        layout = QFormLayout(self)

        self.label1 = QLabel('0', self)
        layout.addRow(self.label1, ClickJumpSlider(
            Qt.Horizontal, valueChanged=lambda v: self.label1.setText(str(v))))

        # 横 - 역전 
        self.label2 = QLabel('0', self)
        layout.addRow(self.label2, ClickJumpSlider(
            Qt.Horizontal, invertedAppearance=True,
            valueChanged=lambda v: self.label2.setText(str(v))))

        self.label3 = QLabel('0', self)
        layout.addRow(self.label3, ClickJumpSlider(
            Qt.Vertical, minimumHeight=200, valueChanged=lambda v: self.label3.setText(str(v))))

        #ir 종 방향 역전 
        self.label4 = QLabel('0', self)
        layout.addRow(self.label4, ClickJumpSlider(
            Qt.Vertical, invertedAppearance=True,
            minimumHeight=200, valueChanged=lambda v: self.label4.setText(str(v))))


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec_())
