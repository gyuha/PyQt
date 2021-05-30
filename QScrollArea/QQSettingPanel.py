#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget

from Lib.SettingUi import Ui_Setting  # @UnresolvedImport


# 2018 년 3 월 28 일에 작성되었습니다 
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: QQSettingPanel
# description:

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Window(QWidget, Ui_Setting):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(700, 435)
        self._blockSignals = False

        # 和 및 왼쪽 항목 이벤트 
        self.scrollArea.verticalScrollBar().valueChanged.connect(
            self.onValueChanged)
        self.listWidget.itemClicked.connect(self.onItemClicked)

    def onValueChanged(self, value):
        """滚动条"""
        if self._blockSignals:
            # 스크롤 막대를 변경하는 항목을 방지합니다. 
            return
        for i in range(8):  # 오른쪽에 8 개의 위젯이 있기 때문에 
            widget = getattr(self, 'widget_%d' % i, None)
            # 위젯이 비어 있지 않으며 시각적 범위 내에서 
            if widget and not widget.visibleRegion().isEmpty():
                self.listWidget.setCurrentRow(i)  # 항목 선택을 설정하십시오 
                return

    def onItemClicked(self, item):
        """左侧item"""
        row = self.listWidget.row(item)  # 항목 색인을 클릭하십시오 
        # 오른쪽 위젯이 명명 된 WIDGET_0 WIDGET_1에 따라 사양을 비교하는 방법이기 때문에 GETATTR을 통해 찾을 수 있습니다. 
        widget = getattr(self, 'widget_%d' % row, None)
        if not widget:
            return
        # 定 侧 侧 侧 
        self._blockSignals = True
        self.scrollArea.verticalScrollBar().setSliderPosition(widget.pos().y())
        self._blockSignals = False


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(open("Data/style.qss", "rb").read().decode("utf-8"))
    w = Window()
    w.show()
    sys.exit(app.exec_())
