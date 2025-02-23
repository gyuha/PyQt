#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年6月22日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: MessageBox
@description: 
"""
from random import randrange

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class MessageBox(QMessageBox):

    def __init__(self, *args, count=5, time=1000, auto=False, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self._count = count
        self._time = time
        self._auto = auto  # 是 자동 닫기 
        assert count > 0  # 0보다 커야합니다 
        assert time >= 500  # = 500ms = ms. 
        self.setStandardButtons(self.Close)  # 关 闭 按 
        self.closeBtn = self.button(self.Close)  # 获 关 关 关 按. 
        self.closeBtn.setText('关闭(%s)' % count)
        self.closeBtn.setEnabled(False)
        self._timer = QTimer(self, timeout=self.doCountDown)
        self._timer.start(self._time)
        print('是否自动关闭', auto)

    def doCountDown(self):
        self.closeBtn.setText('关闭(%s)' % self._count)
        self._count -= 1
        if self._count <= 0:
            self.closeBtn.setText('关闭')
            self.closeBtn.setEnabled(True)
            self._timer.stop()
            if self._auto:  # 자동 종료 
                self.accept()
                self.close()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QPushButton
    app = QApplication(sys.argv)
    w = QPushButton('点击弹出对话框')
    w.resize(200, 200)
    w.show()
    w.clicked.connect(lambda: MessageBox(
        w, text='倒计时关闭对话框', auto=randrange(0, 2)).exec_())
    sys.exit(app.exec_())
