#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月27日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: FoldWidget
@description: 自定义item折叠控件仿QTreeWidget
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout,\
    QLineEdit, QListWidget, QListWidgetItem, QCheckBox


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"
__Version__ = "Version 1.0"


class CustomWidget(QWidget):

    def __init__(self, item, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        self.oldSize = None
        self.item = item
        layout = QFormLayout(self)
        layout.addRow('我是label', QLineEdit(self))
        layout.addRow('点击', QCheckBox(
            '隐藏下面的按钮', self, toggled=self.hideChild))
        self.button = QPushButton('我是被隐藏的', self)
        layout.addRow(self.button)

    def hideChild(self, v):
        self.button.setVisible(not v)
        # 내부 하위 컨트롤을 숨기면 높이를 다시 계산하는 데 중요합니다. 
        self.adjustSize()

    def resizeEvent(self, event):
        # 아이템의 높이 문제를 해결하십시오 
        super(CustomWidget, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))


class CustomButton(QPushButton):
    # 버튼 스위치로 

    def __init__(self, item, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.item = item
        self.setCheckable(True)  # 선택 사항 선택 사항 

    def resizeEvent(self, event):
        # 아이템의 높이 문제를 해결하십시오 
        super(CustomButton, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))


class Window(QListWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        for _ in range(3):
            # 开关 
            item = QListWidgetItem(self)
            btn = CustomButton(item, '折叠', self, objectName='testBtn')
            self.setItemWidget(item, btn)

            # 접이식 제어 
            item = QListWidgetItem(self)
            # 隐 选 选 选 选 选 I. 
            btn.toggled.connect(item.setHidden)
            self.setItemWidget(item, CustomWidget(item, self))


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # QSS를 통해 버튼의 높이 변경 
    app.setStyleSheet('#testBtn{min-height:40px;}')
    w = Window()
    w.show()
    sys.exit(app.exec_())
