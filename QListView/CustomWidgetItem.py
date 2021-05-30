#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView, QWidget, QHBoxLayout, QLineEdit,\
    QPushButton


# 2018 년 8 월 4 일에 만들어졌습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# 파일 : QListView. 사용자 정의 위젯을 표시합니다 
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


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


class ListView(QListView):

    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        # 모델 
        self._model = QStandardItemModel(self)
        self.setModel(self._model)

        # 循 生 生 10 10 自 控 
        for i in range(10):
            item = QStandardItem()
            self._model.appendRow(item)  # 아이템 추가 

            # 색인을 얻으십시오 
            index = self._model.indexFromItem(item)
            widget = CustomWidget(str(i))
            item.setSizeHint(widget.sizeHint())  # 주로 항목의 높이를 조정합니다 
            # 사용자 정의 위젯을 설정합니다 
            self.setIndexWidget(index, widget)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ListView()
    w.show()
    sys.exit(app.exec_())
