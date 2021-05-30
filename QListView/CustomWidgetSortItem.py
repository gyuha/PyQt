#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice, randint
import string
from time import time

from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListView,\
    QHBoxLayout, QLineEdit


# 2018 년 8 월 4 일에 만들어졌습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# 파일 : QListview. 사용자 정의 위젯 및 정렬 표시 
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


def randomChar(y):
    # 임의의 문자열을 반환합니다 
    return ''.join(choice(string.ascii_letters) for _ in range(y))


class CustomWidget(QWidget):

    def __init__(self, text, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLineEdit(text, self))
        layout.addWidget(QPushButton('x', self))

    def sizeHint(self):
        # 항목의 높이를 결정하십시오 
        return QSize(200, 40)


class SortFilterProxyModel(QSortFilterProxyModel):

    def lessThan(self, source_left, source_right):
        if not source_left.isValid() or not source_right.isValid():
            return False
        # 데이터 검색 
        leftData = self.sourceModel().data(source_left)
        rightData = self.sourceModel().data(source_right)
        if self.sortOrder() == Qt.DescendingOrder:
            # 시간별로 정렬하십시오 
            leftData = leftData.split('-')[-1]
            rightData = rightData.split('-')[-1]
            return leftData < rightData
#         elif self.sortOrder() == Qt.AscendingOrder:
# # 정렬 기준 오름차순으로 정렬합니다 
#             leftData = leftData.split('-')[0]
#             rightData = rightData.split('-')[0]
#             return leftData < rightData
        return super(SortFilterProxyModel, self).lessThan(source_left, source_right)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        # 名字 排序 
        layout.addWidget(QPushButton('以名字升序', self, clicked=self.sortByName))
        # 时 时间 序 
        layout.addWidget(QPushButton('以时间倒序', self, clicked=self.sortByTime))
        # listview
        self.listView = QListView(self)
        layout.addWidget(self.listView)
        # 데이터 모델 
        self.dmodel = QStandardItemModel(self.listView)
        # 排 代 代理 모델 
        self.fmodel = SortFilterProxyModel(self.listView)
        self.fmodel.setSourceModel(self.dmodel)
        self.listView.setModel(self.fmodel)

        # 시뮬레이션 50 데이터 
        for _ in range(50):
            name = randomChar(5)
            times = time() + randint(0, 30)  # 현재 시간 무작위 + 
            value = '{}-{}'.format(name, times)  # 内容 内容 - 별도로 
            item = QStandardItem(value)
#             item.setData(value, Qt.UserRole + 2)
            self.dmodel.appendRow(item)
            # 인덱스 
            index = self.fmodel.mapFromSource(item.index())
            # 맞춤 위젯 
            widget = CustomWidget(value, self)
            item.setSizeHint(widget.sizeHint())
            self.listView.setIndexWidget(index, widget)

    def sortByTime(self):
        # 시간별로 정렬하십시오 
        self.fmodel.sort(0, Qt.DescendingOrder)

    def sortByName(self):
        # 이름으로 정렬합니다 
        self.fmodel.sort(0, Qt.AscendingOrder)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
