#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout,\
    QListWidgetItem, QLabel


# 2018 년 5 월 29 일에 작성되었습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: LeftTabWidget
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class LeftTabWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(LeftTabWidget, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 左 右 布 (q qtwidget + qstackedwidget + qstackedwidget) 
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左 목록 
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        # 层 
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)
        self.initUi()

    def initUi(self):
        # 초기화 인터페이스 
        # qlistwidget의 현재 항목에 의해 QStackedWidget의 일련 번호를 전환합니다. 
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)
        # 去 掉 掉 边 
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 스크롤 막대 숨기기 
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 이것은 일반 텍스트가있는 아이콘 모드와 함께 사용됩니다 (아이콘 모드를 직접 사용할 수도 있고 setViewMode) 
        for i in range(20):
            item = QListWidgetItem(
                QIcon('Data/0%d.ico' % randint(1, 8)), str('选 项 %s' % i), self.listWidget)
            # 항목의 기본 너비를 설정합니다 (여기에서만 유용합니다). 
            item.setSizeHint(QSize(16777215, 60))
            # 文 中 
            item.setTextAlignment(Qt.AlignCenter)

        # ename 20 페이지 오른쪽에 (위와 함께 반복되지 않음) 
        for i in range(20):
            label = QLabel('我是页面 %d' % i, self)
            label.setAlignment(Qt.AlignCenter)
            # 레이블의 배경색을 설정하십시오 (무작위) 
            # 그는 여백 마진을 추가했습니다 (qstackedwidget과 qlabel의 색상을 구별하는 것이 편리합니다) 
            label.setStyleSheet('background: rgb(%d, %d, %d);margin: 50px;' % (
                randint(0, 255), randint(0, 255), randint(0, 255)))
            self.stackedWidget.addWidget(label)


# 美 化 스타일 시트 
Stylesheet = """
/*去掉item虚线边框*/
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
/*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
QListWidget {
    min-width: 120px;
    max-width: 120px;
    color: white;
    background: black;
}
/*被选中时的背景颜色和左边框颜色*/
QListWidget::item:selected {
    background: rgb(52, 52, 52);
    border-left: 2px solid rgb(9, 187, 7);
}
/*鼠标悬停颜色*/
HistoryPanel::item:hover {
    background: rgb(52, 52, 52);
}

/*右侧的层叠窗口的背景颜色*/
QStackedWidget {
    background: rgb(30, 30, 30);
}
/*模拟的页面*/
QLabel {
    color: white;
}
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    w = LeftTabWidget()
    w.show()
    sys.exit(app.exec_())
