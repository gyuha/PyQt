#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月4日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: 删除Item
@description: 
"""
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton,\
    QListWidgetItem, QVBoxLayout, QListWidget


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class ItemWidget(QWidget):

    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, text, item, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self._item = item  # 保 l 的 对 对 对 引 引 引 
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLineEdit(text, self))
        layout.addWidget(QPushButton('x', self, clicked=self.doDeleteItem))

    def doDeleteItem(self):
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        # 항목의 높이를 결정하십시오 
        return QSize(200, 40)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        # land. 
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)

        # 清 按 버튼 
        self.clearBtn = QPushButton('清空', self, clicked=self.doClearItem)
        layout.addWidget(self.clearBtn)

        # 테스트 데이터 추가 
        self.testData()

    def doDeleteItem(self, item):
        # 항목에 따라 해당 행 수를 가져옵니다. 
        row = self.listWidget.indexFromItem(item).row()
        # 삭제 항목 
        item = self.listWidget.takeItem(row)
        # 위젯 삭제 
        self.listWidget.removeItemWidget(item)
        del item

    def doClearItem(self):
        # 모든 항목을 지우십시오 
        for _ in range(self.listWidget.count()):
            # 삭제 항목 
            # 一 是 0 이유는 첫 번째 줄에서 첫 번째 줄의 두 번째 삭제 라인이 첫 번째 줄이되었습니다. 
            # 本 和 和 l l l 数据 数据 数据 理 道 
            item = self.listWidget.takeItem(0)
            # 위젯 삭제 
            self.listWidget.removeItemWidget(item)
            del item

    def testData(self):
        # 테스트 데이터 생성 
        for i in range(100):
            item = QListWidgetItem(self.listWidget)
            widget = ItemWidget('item: {}'.format(i), item, self.listWidget)
            # 삭제 신호 
            widget.itemDeleted.connect(self.doDeleteItem)
            self.listWidget.setItemWidget(item, widget)


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
