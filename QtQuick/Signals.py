#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: QtQuick.Signals
@description: 信号槽
"""

from time import time
import sys

from PyQt5.QtCore import QCoreApplication, Qt, pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout,\
    QPushButton, QTextBrowser


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

QML = """import QtQuick 2.0
import QtQuick.Controls 1.6
import QtQuick.Layouts 1.3

ApplicationWindow {
    visible: true
    width: 400
    height: 400
    id: root
    title: "editor"

    // 定义信号槽
    signal valueChanged(int value)
    
    Component.onCompleted: {
        // 绑定信号槽到python中的函数
        valueChanged.connect(_Window.onValueChanged)
        // 绑定python中的信号到qml中的函数
        _Window.timerSignal.connect(appendText)
    }
    
    function appendText(text) {
        // 定义添加文字函数
        textArea.append(text)
    }

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        Button {
            id: button
            text: qsTr("Button")
            Layout.fillWidth: true
            onClicked: {
                // 点击按钮调用python中的函数并得到返回值
                var ret = _Window.testSlot("Button")
                textArea.append("我调用了testSlot函数得到返回值: " + ret)
            }
        }

        Slider {
            id: sliderHorizontal
            Layout.fillWidth: true
            stepSize: 1
            minimumValue: 0
            maximumValue: 100
            // 拉动条值改变时发送信号
            onValueChanged: root.valueChanged(value)
        }

        TextArea {
            id: textArea
            Layout.fillWidth: true
        }
    }

}
"""


class Window(QWidget):

    # 시간 신호를 정의하십시오 
    timerSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('Python调用qml中的函数',
                                     self, clicked=self.callQmlFunc))
        self.resultView = QTextBrowser(self)
        layout.addWidget(self.resultView)
        self._timer = QTimer(self, timeout=self.onTimeout)
        self._timer.start(2000)

    def onTimeout(self):
        # 타이머 신호 알림 QML을 보냅니다 
        self.timerSignal.emit('定时器发来:' + str(time()))

    def callQmlFunc(self):
        # qml에서 appendtext 함수를 적극적으로 호출합니다 
        engine.rootObjects()[0].appendText('我是被Python调用了')

    @pyqtSlot(int)
    def onValueChanged(self, value):
        # QML 사용자 정의 신호 ValueChanged 바인딩 슬롯 기능 
        self.resultView.append('拉动条值: %s' % value)

    @pyqtSlot(str, result=str)  # 반환 값을 얻을 수 있습니다 
    def testSlot(self, name):
        # Q 调 Q 调 调 调 
        self.resultView.append('我被主动调用: %s' % name)
        return str(len(name))


if __name__ == '__main__':
    try:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    except:
        pass

    app = QApplication(sys.argv)

    # 테스트 인터페이스 
    w = Window()
    w.resize(400, 400)
    w.show()
    w.move(400, 400)

    engine = QQmlApplicationEngine()
    # 통신 개체를 제공 _Window, Qobject를 상속하는 클래스가 있어야합니다. 
    engine.rootContext().setContextProperty('_Window', w)

    engine.objectCreated.connect(
        lambda obj, _: QMessageBox.critical(None, '错误', '运行失败，请检查') if not obj else 0)
    engine.loadData(QML.encode())

    sys.exit(app.exec_())
