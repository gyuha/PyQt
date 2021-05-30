#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月27日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: CityLinkage
@description: 下拉联动
"""
import json
import sys

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QComboBox,\
    QLabel, QSpacerItem, QSizePolicy
import chardet


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        super(SortFilterProxyModel, self).__init__(*args, **kwargs)
        self.setFilterRole(Qt.ToolTipRole)  # Qt.Tooltiprole 역할에 따라 # 필터링합니다 
        self._model = QStandardItemModel(self)
        self.setSourceModel(self._model)

    def appendRow(self, item):
        self._model.appendRow(item)

    def setFilter(self, _):
        # 필터 
        # self.sender () # 보낸 사람 
        # drop-down 상자에서 item_code 가져 오기 
        item_code = self.sender().currentData(Qt.ToolTipRole)
        if not item_code:
            return
        if item_code.endswith("0000"):  # 필터 
            self.setFilterRegExp(QRegExp(item_code[:-4] + "\d\d00"))
        elif item_code.endswith("00"):  # 다음을 필터링합니다 
            self.setFilterRegExp(QRegExp(item_code[:-2] + "\d\d"))


class CityLinkageWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(CityLinkageWindow, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        self.province_box = QComboBox(self, minimumWidth=200)  # 도시 수준 이상 
        self.city_box = QComboBox(self, minimumWidth=200)  # 市 
        self.county_box = QComboBox(self, minimumWidth=200)  # 市 아래 수준 
        layout.addWidget(QLabel("省/直辖市/特别行政区", self))
        layout.addWidget(self.province_box)
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(QLabel("市", self))
        layout.addWidget(self.city_box)
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(QLabel("区/县", self))
        layout.addWidget(self.county_box)
        self.initModel()
        self.initSignal()
        self.initData()

    def initSignal(self):
        # 초기화 신호 슬롯 
        self.province_box.currentIndexChanged.connect(
            self.city_model.setFilter)
        self.city_box.currentIndexChanged.connect(self.county_model.setFilter)

    def initModel(self):
        # 초기화 모델 
        self.province_model = SortFilterProxyModel(self)
        self.city_model = SortFilterProxyModel(self)
        self.county_model = SortFilterProxyModel(self)
        # 모델을 설정합니다 
        self.province_box.setModel(self.province_model)
        self.city_box.setModel(self.city_model)
        self.county_box.setModel(self.county_model)

    def initData(self):
        # 초기화 데이터 
        datas = open("Data/data.json", "rb").read()
        encoding = chardet.detect(datas) or {}
        datas = datas.decode(encoding.get("encoding", "utf-8"))
        datas = json.loads(datas)
        # 파싱 데이터를 시작합니다 
        for data in datas:
            item_code = data.get("item_code")  # 编 编 
            item_name = data.get("item_name")  # 이름 
            item = QStandardItem(item_name)
            item.setData(item_code, Qt.ToolTipRole)
            if item_code.endswith("0000"):  # 4 0 결말은 도시 수준입니다 
                self.province_model.appendRow(item)
            elif item_code.endswith("00"):  # 2 0 끝이 도시입니다 
                self.city_model.appendRow(item)
            else:  # 市 아래에서 
                self.county_model.appendRow(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CityLinkageWindow()
    w.show()
    sys.exit(app.exec_())
