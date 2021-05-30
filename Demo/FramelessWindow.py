#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

from Lib.FramelessWindow import FramelessWindow  # @UnresolvedImport


# 2018 년 4 월 30 일에 만들어졌습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: Test
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QPushButton('按钮', self))
        layout.addWidget(QTextEdit(self))


# 스타일 
StyleSheet = """
/*标题栏*/
TitleBar {
    background-color: rgb(54, 157, 180);
}

/*最小化最大化关闭按钮通用默认背景*/
#buttonMinimum,#buttonMaximum,#buttonClose {
    border: none;
    background-color: rgb(54, 157, 180);
}

/*悬停*/
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}

/*鼠标按下不放*/
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = FramelessWindow()
    w.setWindowTitle('测试标题栏')
    w.setWindowIcon(QIcon('Data/Qt.ico'))
    w.setWidget(MainWindow(w))  # 자신의 창을 추가하십시오 
    w.show()
    sys.exit(app.exec_())
