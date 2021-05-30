#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月9日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: moveToThread
@description: moveToThread
"""
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPushButton


__Author__ = 'By: Irony\nQQ: 892768447\nEmail: 892768447@qq.com'
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Worker(QObject):

    valueChanged = pyqtSignal(int)  # 값 변경 신호 

    def run(self):
        print('thread id', int(QThread.currentThreadId()))
        for i in range(1, 101):
            print('value', i)
            self.valueChanged.emit(i)
            QThread.sleep(1)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        layout.addWidget(self.progressBar)
        layout.addWidget(QPushButton('开启线程', self, clicked=self.onStart))

        # 현재 스레드 ID. 
        print('main id', int(QThread.currentThreadId()))

        # 스레드 업데이트 일정을 시작합니다 
        self._thread = QThread(self)
        self._worker = Worker()
        self._worker.moveToThread(self._thread)  # 스레드로 이동합니다 
        self._thread.finished.connect(self._worker.deleteLater)
        self._worker.valueChanged.connect(self.progressBar.setValue)

    def onStart(self):
        print('main id', int(QThread.currentThreadId()))
        self._thread.started.connect(self._worker.run)
        self._thread.start()  # 启 线 线程 

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
            # 强 强 
            # self._thread.terminate()
        del self._thread
        del self._worker
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
