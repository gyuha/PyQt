#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年4月6日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: CopyContent
@description: 
'''
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QApplication, QAction, QMessageBox


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class TableView(QTableView):

    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
        self.resize(800, 600)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)  # 键 메뉴 
        self.setEditTriggers(self.NoEditTriggers)  # 禁 编 编 
        self.doubleClicked.connect(self.onDoubleClick)
        self.addAction(QAction("复制", self, triggered=self.copyData))
        self.myModel = QStandardItemModel()  # model
        self.initHeader()  # 초기화 머리 
        self.setModel(self.myModel)
        self.initData()  # 아날로그 데이터를 초기화합니다 

    def onDoubleClick(self, index):
        print(index.row(), index.column(), index.data())

    def keyPressEvent(self, event):
        super(TableView, self).keyPressEvent(event)
        # Ctrl + C
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.copyData()

    def copyData(self):
        count = len(self.selectedIndexes())
        if count == 0:
            return
        if count == 1:  # 하나만 복사하십시오 
            QApplication.clipboard().setText(
                self.selectedIndexes()[0].data())  # 클립 보드에 복사 
            QMessageBox.information(self, "提示", "已复制一个数据")
            return
        rows = set()
        cols = set()
        for index in self.selectedIndexes():  # 모두 선택하십시오 
            rows.add(index.row())
            cols.add(index.column())
            # print(index.row(),index.column(),index.data())
        if len(rows) == 1:  # 一 
            QApplication.clipboard().setText("\t".join(
                [index.data() for index in self.selectedIndexes()]))  # 复 
            QMessageBox.information(self, "提示", "已复制一行数据")
            return
        if len(cols) == 1:  # 행 
            QApplication.clipboard().setText("\r\n".join(
                [index.data() for index in self.selectedIndexes()]))  # 复 
            QMessageBox.information(self, "提示", "已复制一列数据")
            return
        mirow, marow = min(rows), max(rows)  # 대부분 (덜 / 더) 라인 
        micol, macol = min(cols), max(cols)  # 대부분 (덜 / 더) 열 
        print(mirow, marow, micol, macol)
        arrays = [
            [
                "" for _ in range(macol - micol + 1)
            ] for _ in range(marow - mirow + 1)
        ]  # 2 차원 배열 생성 (및 공기 라인 및 빈 열의 전면 제외) 
        print(arrays)
        # 데이터 투입 
        for index in self.selectedIndexes():  # 선택된 모든 것을 가로 지르십시오 
            arrays[index.row() - mirow][index.column() - micol] = index.data()
        print(arrays)
        data = ""  # 마지막 결과 
        for row in arrays:
            data += "\t".join(row) + "\r\n"
        print(data)
        QApplication.clipboard().setText(data)  # 클립 보드에 복사 
        QMessageBox.information(self, "提示", "已复制")

    def initHeader(self):
        for i in range(5):
            self.myModel.setHorizontalHeaderItem(
                i, QStandardItem("表头" + str(i + 1)))

    def initData(self):
        for row in range(100):
            for col in range(5):
                self.myModel.setItem(
                    row, col, QStandardItem("row: {row},col: {col}".format(row=row + 1, col=col + 1)))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("TableView")
    w = TableView()
    w.show()
    sys.exit(app.exec_())
