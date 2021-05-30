#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月19日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: 
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton,\
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)
        clayout = QHBoxLayout()
        layout.addItem(clayout)
        clayout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        clayout.addWidget(QPushButton('水平翻转', self, clicked=self.doHorFilp))
        clayout.addWidget(QPushButton('垂直翻转', self, clicked=self.doVerFilp))
        clayout.addWidget(QPushButton(
            '顺时针45度', self, clicked=self.doClockwise))
        clayout.addWidget(QPushButton(
            '逆时针45度', self, clicked=self.doAnticlockwise))
        clayout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 원본 그림 
        self.srcImage = QImage('Data/fg.png')
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doHorFilp(self):
        # 가로 플립 
        self.srcImage = self.srcImage.mirrored(True, False)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doVerFilp(self):
        # 수직 플립 
        self.srcImage = self.srcImage.mirrored(False, True)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doClockwise(self):
        # 시계 방향 45도 
        image = QImage(self.srcImage.size(),
                       QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(image)
        # 原 以 
        hw = self.srcImage.width() / 2
        hh = self.srcImage.height() / 2
        painter.translate(hw, hh)
        painter.rotate(45)  # 4 45도 
        painter.drawImage(-hw, -hh, self.srcImage)  # 사진을 그립니다 
        painter.end()
        self.srcImage = image  # 
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

# #이 회전 방법 아래의 90 도의 여러도 아래로, 그렇지 않으면 그림이 더 크게 될 것입니다. 
#         trans = QTransform()
#         trans.rotate(90)
#         self.srcImage = self.srcImage.transformed(
#             trans, Qt.SmoothTransformation)
#         self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doAnticlockwise(self):
        # 시계 반대 방향 45도 
        image = QImage(self.srcImage.size(),
                       QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(image)
        # 原 以 
        hw = self.srcImage.width() / 2
        hh = self.srcImage.height() / 2
        painter.translate(hw, hh)
        painter.rotate(-45)  # - 45도 
        painter.drawImage(-hw, -hh, self.srcImage)  # 사진을 그립니다 
        painter.end()
        self.srcImage = image  # 
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

# #이 회전 방법 아래의 90 도의 여러도 아래로, 그렇지 않으면 그림이 더 크게 될 것입니다. 
#         trans = QTransform()
#         trans.rotate(90)
#         self.srcImage = self.srcImage.transformed(
#             trans, Qt.SmoothTransformation)
#         self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
