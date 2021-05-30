#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月20日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: CircleImage
@description: 圆形图片
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class Label(QLabel):

    def __init__(self, *args, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(200, 200)
        self.setMinimumSize(200, 200)
        self.radius = 100

        ############## ¶ ######################## ##################################################### ##################################################### ##################################################### ##################################################### ## 
        self.target = QPixmap(self.size())  # 크기 및 제어 
        self.target.fill(Qt.transparent)  # 背景 背景 为 

        p = QPixmap("Data/Images/head.jpg").scaled(  # loading rouse and large로 확대됩니다 
            200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            # 抗锯 齿齿 
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # painter.setpen (# 테스트 서클) 
        #             QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)
        # **** 라운드로 잘라 **** # 
        painter.setClipPath(path)
        # painter.DrawPath (경로) # 테스트 서클 

        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
        ############## ¶ ######################## ##################################################### ##################################################### ##################################################### ##################################################### ## 


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(Label(self))
        layout.addWidget(Label(self, antialiasing=False))
        self.setStyleSheet("background: black;")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
