#!/usr/bin/env python
# encoding: utf-8
'''
@author: wxj
@license: (C) Hefei tongzhi electromechanical control technology co.LTD
@contact: 
@software: garner
@file: table.py
@time: 2019/4/11 21:26
@desc:
'''
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class MyTable(QTableWidget):
    def __init__(self,parent=None):
        super(MyTable, self).__init__(parent)
        self.setWindowTitle("我是一个表格")
        self.setWindowIcon(QIcon("male.png"))
        self.resize(920, 240)
        self.setColumnCount(6)
        self.setRowCount(2)
        # 두 행의 행으로 테이블을 설정합니다. 
        self.setColumnWidth(0, 200)
        self.setColumnWidth(4, 200)
        self.setRowHeight(0, 100)
        # 첫 번째 줄 높이를 100px로 설정하면 첫 번째 열 너비는 200px입니다. 

        self.table()

    def table(self):
        self.setItem(0,0,QTableWidgetItem("           你的名字"))
        self.setItem(0,1,QTableWidgetItem("性别"))
        self.setItem(0,2,QTableWidgetItem("出生日期"))
        self.setItem(0,3, QTableWidgetItem("职业"))
        self.setItem(0,4, QTableWidgetItem("收入"))
        self.setItem(0, 5, QTableWidgetItem("进度条"))
        # 테이블의 텍스트 내용을 추가하십시오. 
        self.setHorizontalHeaderLabels(["第一行", "第二行", "第三行", "第四行", "第五行","第六行"])
        self.setVerticalHeaderLabels(["第一列", "第二列"])
        # 헤더를 설정하십시오 
        lbp = QLabel()
        lbp.setPixmap(QPixmap("Male.png"))
        self.setCellWidget(1,1,lbp)
        # 표에 그림을 추가하십시오 
        twi = QTableWidgetItem("      新海诚")
        twi.setFont(QFont("Times", 10, ))
        self.setItem(1,0,twi)

        # 크기를 설정하고 직접 입력하는 텍스트를 추가하십시오. 
        dte = QDateTimeEdit()
        dte.setDateTime(QDateTime.currentDateTime())
        dte.setDisplayFormat("yyyy/MM/dd")
        dte.setCalendarPopup(True)
        self.setCellWidget(1,2,dte)
        # 팝업 날짜 선택을 추가하고 기본값을 현재 날짜로 설정하면 디스플레이 형식이 연도의 날짜입니다. 
        cbw = QComboBox()
        cbw.addItem("医生")
        cbw.addItem("老师")
        cbw.addItem("律师")
        self.setCellWidget(1,3,cbw)
        # 드롭 다운 선택 상자를 추가합니다 
        sb = QSpinBox()
        sb.setRange(1000,10000)
        sb.setValue(5000)# 디스플레이하기 시작하는 번호를 설정하십시오 
        sb.setDisplayIntegerBase(10)# 이것은 디스플레이의 응용 프로그램이며 기본값은 디메이션입니다. 
        sb.setSuffix("元")# 设置 设置 
        sb.setPrefix("RMB: ")# 设置 设置 
        sb.setSingleStep(100)
        self.setCellWidget(1,4,sb)
        # 진행률 표시 줄을 추가하십시오 

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.setCellWidget(1, 5, self.progressBar)
        self.step = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        # 그루브에 대한 신호 연결 
        self.timer.timeout.connect(self.onTimerOut)
        self.count=0
    def onTimerOut(self):  # 重 写 timeEvent. 
        self.count +=1
        if self.count >= 100:  # 값> = 100, 타이머를 중지하십시오 
            self.timer.stop()
            print("结束")
            # self.progressBar.setValue(self.step)
        else:
            print(self.count)
            self.progressBar.setValue(self.count)
            # return
            # self.step += 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myTable = MyTable()
    myTable.show()
    app.exit(app.exec_())
