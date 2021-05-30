#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


# 2018 년 6 월 14 일에 작성되었습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: FadeInOut
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('退出', self, clicked=self.doClose))

        # 透 透 动 动 动. 
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(1000)  # 持 时间 1. 

        # 执行 入 
        self.doShow()

    def doShow(self):
        try:
            # 애니메이션이 완료된 후 # 창의 창을 닫으려고합니다. 
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透 透 范围 范围 0에서 점차적으로 1로 증가합니다. 
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动 动 完成 完成 则. 
        # 透 透 范围 范围 1에서 점차적으로 0으로 감소했습니다. 
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
