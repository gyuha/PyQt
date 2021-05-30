#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月14日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: DragListWidget
@description: 
"""
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QColor, QPixmap, QDrag, QPainter, QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class DropListWidget(QListWidget):
    # QListWidget에서 끌 수 있습니다 

    def __init__(self, *args, **kwargs):
        super(DropListWidget, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        self.setAcceptDrops(True)
        # 왼쪽에서 오른쪽으로 설정, 자동으로 랩, 배열 
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # 特 e 间 间 
        self.setSpacing(5)

    def makeItem(self, size, cname):
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, cname)  # 사용자 정의 데이터에 색상을 넣으십시오 
        item.setSizeHint(size)
        label = QLabel(self)  # 사용자 정의 컨트롤 
        label.setMargin(2)  # 往 内 进 2. 
        label.resize(size)
        pixmap = QPixmap(size.scaled(96, 96, Qt.IgnoreAspectRatio))  # 크기 조정 
        pixmap.fill(QColor(cname))
        label.setPixmap(pixmap)
        self.setItemWidget(item, label)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if not mimeData.property('myItems'):
            event.ignore()
        else:
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 드래그와 드롭 항목을 얻으십시오 
        items = event.mimeData().property('myItems')
        event.accept()
        for item in items:
            # 항목의 데이터를 제거하고 항목 생성 
            self.makeItem(QSize(100, 100), item.data(Qt.UserRole + 1))


class DragListWidget(QListWidget):
    # qlistwidget. 

    def __init__(self, *args, **kwargs):
        super(DragListWidget, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        # 가로 스크롤 막대를 숨 깁니다 
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 편집 할 수 없습니다 
        self.setEditTriggers(self.NoEditTriggers)
        # 开 功 
        self.setDragEnabled(True)
        # # 外 外 外. 
        self.setDragDropMode(self.DragOnly)
        # 略 放 
        self.setDefaultDropAction(Qt.IgnoreAction)
        # **** 중요한 문장 (함수는 사용할 수 있으며 다중 선택, 시프트 다중 선택, 빈 위치에서 선택할 수 있음) **** 
        # **** 항목을 선택한 후 상자 선택 및 드래그 앤 드롭 충돌이므로 ExtendedSelection을 사용할 수 없습니다. 
        self.setSelectionMode(self.ContiguousSelection)
        # 왼쪽에서 오른쪽으로 설정, 자동으로 랩, 배열 
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # 特 e 间 间 
        self.setSpacing(5)
        # 筋 (상자 선택 효과 용) 
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        self.initItems()

    # 드래그 할 때 렌더링 미리보기 
    # 这里 演 演 i (또는 스태킹 효과를 달성하기 위해 자체 쓰기 알고리즘을 작성하십시오) 
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        drag = QDrag(self)
        mimeData = self.mimeData(items)
        # qmimedata는 이미지, URL, STR, 바이트 등을 설정할 수 있습니다. 
        # 여기에서 추가 속성을 직접 추가 한 다음 항목에 따라 데이터를 제거합니다. 
        mimeData.setProperty('myItems', items)
        drag.setMimeData(mimeData)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        for item in items:
            rect = self.visualRect(self.indexFromItem(item))
            painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
        drag.exec_(supportedActions)

    def mousePressEvent(self, event):
        # 列表 点 一个 事, 상자 선택 도구의 시작 위치를 설정하는 데 사용 
        super(DragListWidget, self).mousePressEvent(event)
        if event.buttons() != Qt.LeftButton or self.itemAt(event.pos()):
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
        self._rubberBand.show()

    def mouseReleaseEvent(self, event):
        # 列表 框 点 事, 隐 工 工 
        super(DragListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        #list 마우스 안개 모바일 이벤트, 설정 상자 선택 도구 용 사각형 범위 
        super(DragListWidget, self).mouseMoveEvent(event)
        if self._rubberPos:
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))

    def makeItem(self, size, cname):
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, cname)  # 사용자 정의 데이터에 색상을 넣으십시오 
        item.setSizeHint(size)
        label = QLabel(self)  # 사용자 정의 컨트롤 
        label.setMargin(2)  # 往 内 进 2. 
        label.resize(size)
        pixmap = QPixmap(size.scaled(96, 96, Qt.IgnoreAspectRatio))  # 크기 조정 
        pixmap.fill(QColor(cname))
        label.setPixmap(pixmap)
        self.setItemWidget(item, label)

    def initItems(self):
        size = QSize(100, 100)
        for cname in QColor.colorNames():
            self.makeItem(size, cname)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet("""QListWidget {
        outline: 0px;
        background-color: transparent;
    }
    QListWidget::item:selected {
        border-radius: 2px;
        border: 1px solid rgb(0, 170, 255);
    }
    QListWidget::item:selected:!active {
        border-radius: 2px;
        border: 1px solid transparent;
    }
    QListWidget::item:selected:active {
        border-radius: 2px;
        border: 1px solid rgb(0, 170, 255);
    }
    QListWidget::item:hover {
        border-radius: 2px;
        border: 1px solid rgb(0, 170, 255);
    }"""
                      )
    wa = DragListWidget()
    wa.show()
    wo = DropListWidget()
    wo.show()
    sys.exit(app.exec_())
