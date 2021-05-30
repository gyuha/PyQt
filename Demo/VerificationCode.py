#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年4月5日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: widgets.WidgetCode
@description: 
'''
from random import sample
import string

from PyQt5.QtCore import Qt, qrand, QPointF, QPoint, QBasicTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QPalette, QFontMetrics
from PyQt5.QtWidgets import QLabel


__version__ = "0.0.1"

DEF_NOISYPOINTCOUNT = 60  # 点 数 
COLORLIST = ("black", "gray", "red", "green", "blue", "magenta")
TCOLORLIST = (Qt.black, Qt.gray, Qt.red, Qt.green, Qt.blue, Qt.magenta)
QTCOLORLIST = (Qt.darkGray, Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkMagenta)
HTML = "<html><body>{html}</body></html>"
FONT = "<font color=\"{color}\">{word}</font>"
WORDS = list(string.ascii_letters + string.digits)
SINETABLE = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)

class WidgetCode(QLabel):
    
    def __init__(self, *args, **kwargs):
        super(WidgetCode, self).__init__(*args, **kwargs)
        self._sensitive = False  # 是 大 大 小 
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setBackgroundRole(QPalette.Midlight)
        self.setAutoFillBackground(True)
        # 폰트 
        newFont = self.font()
        newFont.setPointSize(16)
        newFont.setFamily("Kristen ITC")
        newFont.setBold(True)
        self.setFont(newFont)
        self.reset()
        # 타이머 
        self.step = 0
        self.timer = QBasicTimer()
        self.timer.start(60, self)
        
    def reset(self):
        self._code = "".join(sample(WORDS, 4))  # 무작위 4 자 
        self.setText(self._code)
    
    def check(self, code):
        return self._code == str(code) if self._sensitive else self._code.lower() == str(code).lower()
    
    def setSensitive(self, sensitive):
        self._sensitive = sensitive
    
#     def setText(self, text):
# text = 텍스트 (텍스트 및 len (텍스트) == 4) else "" "" "" "" "" "" "" "" ""랜덤 4 자) 
#         self._code = str(text)
#         html = "".join([FONT.format(color=COLORLIST[qrand() % 6], word=t) for t in text])
#         super(WidgetCode, self).setText(HTML.format(html=html))
    
    def mouseReleaseEvent(self, event):
        super(WidgetCode, self).mouseReleaseEvent(event)
        self.reset()
    
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step += 1
            return self.update()
        return super(WidgetCode, self).timerEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 배경 흰색 
        painter.fillRect(event.rect(), QBrush(Qt.white))
        # 여백의 가장자리를 그립니다 
        painter.setPen(Qt.DashLine)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.rect())
        # 임의의 도면 
        for _ in range(3):
            painter.setPen(QPen(QTCOLORLIST[qrand() % 5], 1, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawLine(QPoint(0, qrand() % self.height()),
                             QPoint(self.width(), qrand() % self.height()))
            painter.drawLine(QPoint(qrand() % self.width(), 0),
                             QPoint(qrand() % self.width(), self.height()))
        #draw 소음 
        painter.setPen(Qt.DotLine)
        painter.setBrush(Qt.NoBrush)
        for _ in range(self.width()):  #draw 소음 
            painter.drawPoint(QPointF(qrand() % self.width(), qrand() % self.height()))
        # 슈퍼 (위젯 코드, 자체) .painTevent (이벤트) #draw 텍스트 
        # beating text를 그립니다 
        metrics = QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text())) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        for i, ch in enumerate(self.text()):
            index = (self.step + i) % 16
            painter.setPen(TCOLORLIST[qrand() % 6])
            painter.drawText(x, y - ((SINETABLE[index] * metrics.height()) / 400), ch)
            x += metrics.width(ch)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
    from PyQt5.QtGui import QFontDatabase
    from PyQt5.QtWidgets import QLineEdit
    app = QApplication(sys.argv)
    app.setApplicationName("Validate Code")
    QFontDatabase.addApplicationFont("Data/itckrist.ttf")
    w = QWidget()
    layout = QHBoxLayout(w)
    
    cwidget = WidgetCode(w, minimumHeight=35, minimumWidth=80)
    layout.addWidget(cwidget)
    lineEdit = QLineEdit(w, maxLength=4, placeholderText="请输入验证码并按回车验证",
            returnPressed=lambda:print(cwidget.check(lineEdit.text())))
    layout.addWidget(lineEdit)
    w.show()
    sys.exit(app.exec_())
