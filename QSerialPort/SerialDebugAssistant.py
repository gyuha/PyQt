#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月6日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: SerialDebugAssistant
@description: 串口调试小助手
"""
from PyQt5.QtCore import pyqtSlot, QIODevice, QByteArray
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QWidget, QMessageBox

from Lib.UiSerialPort import Ui_FormSerialPort  # @UnresolvedImport


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Window(QWidget, Ui_FormSerialPort):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._serial = QSerialPort(self)  # # 用 连接 连接 对 
        self._serial.readyRead.connect(self.onReadyRead)  # 定 数据 数据 读 信号 信号 
        # 먼저 사용 가능한 직렬 포트 목록을 가져옵니다 
        self.getAvailablePorts()

    @pyqtSlot()
    def on_buttonConnect_clicked(self):
        # 직렬 버튼을 열거 나 닫습니다 
        if self._serial.isOpen():
            # 직렬 포트가 열려 있으면 끄기 
            self._serial.close()
            self.textBrowser.append('串口已关闭')
            self.buttonConnect.setText('打开串口')
            self.labelStatus.setProperty('isOn', False)
            self.labelStatus.style().polish(self.labelStatus)  # 새로 고침 스타일 
            return

        # 구성 연결 직렬 포트에 따라 다릅니다 
        name = self.comboBoxPort.currentText()
        if not name:
            QMessageBox.critical(self, '错误', '没有选择串口')
            return
        port = self._ports[name]
#         self._serial.setPort(port)
        # 이름에 따라 직렬 포트를 설정하십시오 (위 기능을 사용할 수도 있습니다) 
        self._serial.setPortName(port.systemLocation())
        # 전송 속도를 설정합니다 
        self._serial.setBaudRate(  #Traffled, QSerialPort :: Baud9600과 유사합니다 
            getattr(QSerialPort, 'Baud' + self.comboBoxBaud.currentText()))
        # 확인 비트를 설정하십시오 
        self._serial.setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, self.comboBoxParity.currentText() + 'Parity'))
        # 데이터 비트를 설정하십시오 
        self._serial.setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + self.comboBoxData.currentText()))
        # 정지 비트를 설정하십시오 
        self._serial.setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, self.comboBoxStop.currentText()))

        # noflowcontrol 프로세스 제어가 없습니다 
        # HardWareControl 하드웨어 흐름 제어 (RTS / CTS) 
        # SoftwareControl 소프트웨어 흐름 제어 (XON / XOFF) 
        # UnknownFlowControl 알 수없는 컨트롤 
        self._serial.setFlowControl(QSerialPort.NoFlowControl)
        # 读 写 写 方式 打开 口 
        ok = self._serial.open(QIODevice.ReadWrite)
        if ok:
            self.textBrowser.append('打开串口成功')
            self.buttonConnect.setText('关闭串口')
            self.labelStatus.setProperty('isOn', True)
            self.labelStatus.style().polish(self.labelStatus)  # 새로 고침 스타일 
        else:
            self.textBrowser.append('打开串口失败')
            self.buttonConnect.setText('打开串口')
            self.labelStatus.setProperty('isOn', False)
            self.labelStatus.style().polish(self.labelStatus)  # 새로 고침 스타일 

    @pyqtSlot()
    def on_buttonSend_clicked(self):
        # 메시지를 보냅니다 
        if not self._serial.isOpen():
            print('串口未连接')
            return
        text = self.plainTextEdit.toPlainText()
        if not text:
            return
        text = QByteArray(text.encode('gb2312'))  # EMM Windows 테스트 도구이 코드처럼 보입니다 
        if self.checkBoxHexSend.isChecked():
            # 16 진수가 확인 된 경우 
            text = text.toHex()
        # 데이터 보내기 
        print('发送数据:', text)
        self._serial.write(text)

    def onReadyRead(self):
        # 데이터 수신 응답 
        if self._serial.bytesAvailable():
            # 데이터가 읽을 수있는 경우 
            # 이것은 소량의 데이터에 대한 짧은 대답입니다. 데이터의 양이 너무 많으면 ReadAll은 실제로 완료되지 않았습니다. 
            # 자신의 본드 프로토콜을 설정해야합니다 
            data = self._serial.readAll()
            if self.checkBoxHexView.isChecked():
                # 16 진수가 확인 된 경우 
                data = data.toHex()
            data = data.data()
            # 디코딩 된 디스플레이 (啥 啥) 
            try:
                self.textBrowser.append('我收到了: ' + data.decode('gb2312'))
            except:
                # 디코딩에 실패했습니다 
                self.textBrowser.append('我收到了: ' + repr(data))

    def getAvailablePorts(self):
        # 사용할 수있는 직렬 포트 가져 오기 
        self._ports = {}  # 信息 保 保 保 信息. 
        infos = QSerialPortInfo.availablePorts()
        infos.reverse()  # 逆 
        for info in infos:
            # 직렬 포트 이름 -> 연관된 직렬 포트 변수를 통해 
            self._ports[info.portName()] = info
            self.comboBoxPort.addItem(info.portName())

    def closeEvent(self, event):
        if self._serial.isOpen():
            self._serial.close()
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
