#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年8月7日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QtRemoteObjects.SyncUi.WindowSlave
@description: 备窗口
"""
from PyQt5.QtCore import QUrl
from PyQt5.QtRemoteObjects import QRemoteObjectNode, QRemoteObjectReplica
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QCheckBox,\
    QProgressBar, QMessageBox


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class WindowSlave(QWidget):

    def __init__(self, *args, **kwargs):
        super(WindowSlave, self).__init__(*args, **kwargs)
        self.setupUi()
        # 마스터 노드 가입 
        node = QRemoteObjectNode(parent=self)
        node.connectToNode(QUrl('local:WindowMaster'))
        # windowmaster object를 얻으십시오 
        self.windowMaster = node.acquireDynamic('WindowMaster')
        # 초기화, 바인딩 신호 등으로 이동할 수 있습니다. 
        self.windowMaster.initialized.connect(self.onInitialized)
        # 상태 변경 https://doc.qt.io/qt-5/qremoteobjectreplica.html#State-Enum. 
        self.windowMaster.stateChanged.connect(self.onStateChanged)

    def setupUi(self):
        self.setWindowTitle('WindowSlave')
        self.resize(300, 400)
        layout = QVBoxLayout(self)
        # 상자 (양방향 동기화) 
        self.lineEdit = QLineEdit(self)
        # (양방향 동기화) 
        self.checkBox = QCheckBox('来勾我啊', self)
        # 成度 (마스터 업데이트 슬레이브) 
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.progressBar)

    def onStateChanged(self, newState, oldState):
        if newState == QRemoteObjectReplica.Suspect:
            QMessageBox.critical(self, '错误', '连接丢失')

    def onInitialized(self):
        # 마스터와 슬레이브 Enter 상자 바인드 
        self.windowMaster.editValueChanged.connect(self.lineEdit.setText)
        self.lineEdit.textChanged.connect(self.windowMaster.updateEdit)

        # 마스터 및 슬레이브 확인란 바인딩 
        self.windowMaster.checkToggled.connect(self.checkBox.setChecked)
        self.checkBox.toggled.connect(self.windowMaster.updateCheck)

        # 마스터 일정은 슬레이브에 동기화됩니다 
        self.windowMaster.progressValueChanged.connect(
            self.progressBar.setValue)
        
        print('绑定信号槽完成')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = WindowSlave()
    w.show()
    sys.exit(app.exec_())
