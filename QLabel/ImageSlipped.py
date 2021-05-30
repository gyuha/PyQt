#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月18日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: ImageSlipped
@description: 
"""
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QWidget


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class SlippedImgWidget(QWidget):

    def __init__(self, bg, fg, *args, **kwargs):
        super(SlippedImgWidget, self).__init__(*args, **kwargs)
        # 开 跟 跟 
        self.setMouseTracking(True)
        # 배경 
        self.bgPixmap = QPixmap(bg)
        # 前 
        self.pePixmap = QPixmap(fg)
        # 최소 크기 (백그라운드 오른쪽 및 아래의 10 픽셀 숨기기) 
        size = self.bgPixmap.size()
        self.setMinimumSize(size.width() - 10, size.height() - 10)
        self.setMaximumSize(size.width() - 10, size.height() - 10)
        # 分成 마우스 이동 판단을위한 10 부분 
        self.stepX = size.width() / 10
        self.stepY = size.height() / 10
        # 오프셋 
        self._offsets = [-4, -4, -4, -4]  # 背景 背景 (-4, -4), 잠재 고객 (-4, -4) 

    def mouseMoveEvent(self, event):
        super(SlippedImgWidget, self).mouseMoveEvent(event)
        pos = event.pos()

        # 오프셋 
        offsetX = 5 - int(pos.x() / self.stepX)
        offsetY = 5 - int(pos.y() / self.stepY)
        self._offsets[0] = offsetX
        self._offsets[1] = offsetY
        self._offsets[2] = offsetX
        self._offsets[3] = offsetY
        # 새로 고침 
        self.update()

    def paintEvent(self, event):
        super(SlippedImgWidget, self).paintEvent(event)
        # 图 图形 
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 上 5 像 像 图片 图片 
        painter.drawPixmap(
            -5 + self._offsets[0],
            -5 + self._offsets[1], self.bgPixmap)
        # 一 右 角 5 Pictograph의 Pictographs 
        painter.drawPixmap(
            self.width() - self.pePixmap.width() + 5 - self._offsets[2],
            self.height() - self.pePixmap.height() + 5 - self._offsets[3],
            self.pePixmap
        )


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = SlippedImgWidget('Data/bg1.jpg', 'Data/fg1.png')
    w.show()
    sys.exit(app.exec_())
