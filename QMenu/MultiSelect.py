#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月24日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: MultiSelect
@description: 
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMenu,\
    QAction


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.labelInfo = QLabel(self)
        self.button = QPushButton('带按钮的菜单', self)
        layout.addWidget(self.labelInfo)
        layout.addWidget(self.button)

        # 추가 메뉴 
        self._initMenu()

    def _initMenu(self):
        # 메뉴를 만듭니다 
        self._menu = QMenu(self.button)
        # 대체 메뉴 마우스 릴리스 이벤트를 사용하여 선택도가 닫히지 않음 메뉴 
        self._menu.mouseReleaseEvent = self._menu_mouseReleaseEvent
        self._menu.addAction('菜单1', self._checkAction)
        self._menu.addAction('菜单2', self._checkAction)
        self._menu.addAction(
            QAction('菜单3', self._menu, triggered=self._checkAction))
        action = QAction('菜单4', self._menu, triggered=self._checkAction)
        # 사용자 지정 속성을 추가하고 속성이 메뉴를 닫을 수 있음을 판별합니다. 
        action.setProperty('canHide', True)
        self._menu.addAction(action)
        for action in self._menu.actions():
            # 循 设置 可 
            action.setCheckable(True)
        self.button.setMenu(self._menu)

    def _menu_mouseReleaseEvent(self, event):
        action = self._menu.actionAt(event.pos())
        if not action:
            # q 找 a q q q 自己 自己 
            return QMenu.mouseReleaseEvent(self._menu, event)
        if action.property('canHide'):  #이 속성이 있으면 메뉴를 직접 제공하십시오. 
            return QMenu.mouseReleaseEvent(self._menu, event)
        # qaction을 찾으십시오, 그냥 행동을 유발합니다 
        action.activate(action.Trigger)

    def _checkAction(self):
        # 3 개의 부작용이 함수에 응답합니다 
        self.labelInfo.setText('\n'.join(['{}\t选中：{}'.format(
            action.text(), action.isChecked()) for action in self._menu.actions()]))


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.resize(400, 400)
    w.show()
    sys.exit(app.exec_())
