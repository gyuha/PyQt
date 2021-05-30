#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年12月27日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: QListView.SortItemByRole
@description: 
"""
from random import choice

from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        super(SortFilterProxyModel, self).__init__(*args, **kwargs)
        self._topIndex = 0

    def setSortIndex(self, index):
        self._topIndex = index
        print('在最前面的序号为:', index)

    def lessThan(self, source_left, source_right):
        if not source_left.isValid() or not source_right.isValid():
            return False

        if self.sortRole() == ClassifyRole and \
                source_left.column() == self.sortColumn() and \
                source_right.column() == self.sortColumn():
            # 获 获 分 分 分. 
            leftIndex = source_left.data(ClassifyRole)
            rightIndex = source_right.data(ClassifyRole)

            # 升序 
            if self.sortOrder() == Qt.AscendingOrder:
                # 최전선에 유지하십시오 
                if leftIndex == self._topIndex:
                    leftIndex = -1
                if rightIndex == self._topIndex:
                    rightIndex = -1

                return leftIndex < rightIndex

        return super(SortFilterProxyModel, self).lessThan(source_left, source_right)


NameDict = {
    '唐': ['Tang', 0],
    '宋': ['Song', 1],
    '元': ['Yuan', 2],
    '明': ['Ming', 3],
    '清': ['Qing', 4],
}
IndexDict = {
    0: '唐',
    1: '宋',
    2: '元',
    3: '明',
    4: '清',
}

IdRole = Qt.UserRole + 1            # 정렬을 다시 시작하는 데 사용됩니다 
ClassifyRole = Qt.UserRole + 2      # 분류 시퀀스 번호로 정렬합니다 


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(600, 400)
        layout = QVBoxLayout(self)
        self.listView = QListView(self)
        self.listView.setEditTriggers(QListView.NoEditTriggers)
        layout.addWidget(self.listView)
        layout.addWidget(QPushButton('恢复默认顺序', self, clicked=self.restoreSort))
        layout.addWidget(QPushButton('唐', self, clicked=self.sortByClassify))
        layout.addWidget(QPushButton('宋', self, clicked=self.sortByClassify))
        layout.addWidget(QPushButton('元', self, clicked=self.sortByClassify))
        layout.addWidget(QPushButton('明', self, clicked=self.sortByClassify))
        layout.addWidget(QPushButton('清', self, clicked=self.sortByClassify))

        self._initItems()

    def restoreSort(self):
        # 기본 정렬 복원 
        self.fmodel.setSortRole(IdRole)     # 정렬 역할을 설정해야합니다 
        self.fmodel.sort(0)                 ID 오름차순에 따라 # 排 첫 번째 열 

    def sortByClassify(self):
        self.fmodel.setSortIndex(NameDict.get(
            self.sender().text(), ['', 100])[1])
        # self.restoreSort()
        self.fmodel.setSortRole(IdRole)
        # 주어진 분류로 정렬 (여기서는 최전선에서 주어진 분류를 보낼 수있는주의를 기울이십시오) 
        self.fmodel.setSortRole(ClassifyRole)
        self.fmodel.sort(0)

    def _initItems(self):
        # 항목 초기화 
        self.dmodel = QStandardItemModel(self.listView)
        self.fmodel = SortFilterProxyModel(self.listView)
        self.fmodel.setSourceModel(self.dmodel)
        self.listView.setModel(self.fmodel)

        keys = list(NameDict.keys())
        print(keys)  # [ 'Q QING', 'YUAN', 'TANG', 'MIND', 'SONG'] 
        classifies = [v[1] for v in NameDict.values()]
        for i in range(5):
            # 5 100을 추가하고, 분류를 시뮬레이션하는 데 사용되며, 마지막에 주문이 표시됩니다. 
            classifies.append(100)
        print(classifies)  # [4, 2, 0, 3, 1, 100, 100, 100, 100, 100]

        # 生 生 50 품목 
        for i in range(50):
            # Name = Keys [I % 4] # 무작위로 왕조를 찍었습니다. 
            item = QStandardItem()
            # ID 문자 설정 
            item.setData(i, IdRole)
            # 분류 역할을 설정합니다 
            c = choice(classifies)
            item.setData(c, ClassifyRole)
            # 디스플레이 콘텐츠를 설정합니다 
            item.setText('Name: {}\t\tId: {}\t\tClassify: {}'.format(
                IndexDict.get(c, '其它'), i, c))
            self.dmodel.appendRow(item)


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
