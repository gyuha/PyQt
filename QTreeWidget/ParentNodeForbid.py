#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年11月8日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QTreeWidget.ParentNodeForbid
@description: 父节点不可选中
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate,\
    QStyle


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 1.0


class NoColorItemDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        if option.state & QStyle.State_HasFocus:
            # 取 消 消 虚 
            option.state = option.state & ~ QStyle.State_HasFocus
        if option.state & QStyle.State_MouseOver and index.data(Qt.UserRole + 1):
            # 마우스 호버 색상을 표시하지 마십시오 
            option.state = option.state & ~ QStyle.State_MouseOver
        super(NoColorItemDelegate, self).paint(painter, option, index)


class Window(QTreeWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setItemDelegateForColumn(0, NoColorItemDelegate(self))

        # 体 节 (不 选) 
        pitem1 = QTreeWidgetItem(self, ['parent item 1'])
        # 设置 不 不 
        pitem1.setFlags(pitem1.flags() & ~Qt.ItemIsSelectable)
        # 마우스 이벤트를 차폐하기위한 식별자를 설정합니다 
        pitem1.setData(0, Qt.UserRole + 1, True)

        pitem2 = QTreeWidgetItem(self, ['parent item 2'])
        pitem2.setFlags(pitem2.flags() & ~Qt.ItemIsSelectable)
        pitem2.setData(0, Qt.UserRole + 1, True)

        # 하위 노드 (선택 사항) 
        citem1 = QTreeWidgetItem(pitem1, ['child item 1'])
        citem2 = QTreeWidgetItem(pitem2, ['child item 2'])

        self.expandAll()

        # 신호 슬롯 
        self.itemActivated.connect(self.onItemActivated)
        self.itemClicked.connect(self.onItemClicked)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.itemPressed.connect(self.onItemPressed)

    def mousePressEvent(self, event):
        # 点 点 事, 当 点 点 位置 位置 有 有 则 i 
        item = self.itemAt(event.pos())
        if item and item.data(0, Qt.UserRole + 1):
            event.accept()
            return
        super(Window, self).mousePressEvent(event)

    def onItemActivated(self, item, column):
        print('Activated', item.text(0), item, column)

    def onItemClicked(self, item, column):
        print('Clicked', item.text(0), item, column)

    def onItemDoubleClicked(self, item, column):
        print('DoubleClicked', item.text(0), item, column)

    def onItemPressed(self, item, column):
        print('Pressed', item.text(0), item, column)


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
