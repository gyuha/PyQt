#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年4月8日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: ParsingJson
@description: 
"""
import json
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget,\
    QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
import chardet


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class ItemWidget(QWidget):
    """自定义的item"""

    def __init__(self, text, badge, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(text, self, styleSheet='color: white;'))
        layout.addSpacerItem(QSpacerItem(
            60, 1, QSizePolicy.Maximum, QSizePolicy.Minimum))
        if badge and len(badge) == 2:  # # 面 标 
            layout.addWidget(QLabel(
                badge[0], self, alignment=Qt.AlignCenter,
                styleSheet="""min-width: 80px; 
                    max-width: 80px; 
                    min-height: 38px; 
                    max-height: 38px;
                    color: white; 
                    border:none; 
                    border-radius: 4px; 
                    background: %s""" % badge[1]
            ))


class JsonTreeWidget(QTreeWidget):

    def __init__(self, *args, **kwargs):
        super(JsonTreeWidget, self).__init__(*args, **kwargs)
        self.setEditTriggers(self.NoEditTriggers)
        self.header().setVisible(False)
        # 帮 点 点 单 事 事 
        self.itemClicked.connect(self.onItemClicked)

    def onItemClicked(self, item):
        """item单击事件"""
        if item.url:  # URL을 여는 브라우저를 호출하십시오 
            webbrowser.open_new_tab(item.url)

    def parseData(self, datas, parent=None):
        """解析json数据"""
        for data in datas:
            url = data.get('url', '')
            items = data.get('items', [])
            # 生 生 I. 
            _item = QTreeWidgetItem(parent)
            _item.setIcon(0, QIcon(data.get('icon', '')))
            _widget = ItemWidget(
                data.get('name', ''),
                data.get('badge', []),
                self
            )
            _item.url = url  # 변수 값을 직접 설정할 수 있습니다 
            self.setItemWidget(_item, 0, _widget)
            if url:
                continue  # 뛰어 넘다 
            # 解析 儿子 
            if items:
                self.parseData(items, _item)

    def loadData(self, path):
        """加载json数据"""
        datas = open(path, 'rb').read()
        datas = datas.decode(chardet.detect(datas).get('encoding', 'utf-8'))
        self.parseData(json.loads(datas), self)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet("""QTreeView {
    outline: 0px;
    background: rgb(47, 64, 78);
}
QTreeView::item {
    min-height: 92px;
}
QTreeView::item:hover {
    background: rgb(41, 56, 71);
}
QTreeView::item:selected {
    background: rgb(41, 56, 71);
}

QTreeView::item:selected:active{
    background: rgb(41, 56, 71);
}
QTreeView::item:selected:!active{
    background: rgb(41, 56, 71);
}

QTreeView::branch:open:has-children {
    background: rgb(41, 56, 71);
}

QTreeView::branch:has-siblings:!adjoins-item {
    background: green;
}
QTreeView::branch:closed:has-children:has-siblings {
    background: rgb(47, 64, 78);
}

QTreeView::branch:has-children:!has-siblings:closed {
    background: rgb(47, 64, 78);
}

QTreeView::branch:open:has-children:has-siblings {
    background: rgb(41, 56, 71);
}

QTreeView::branch:open:has-children:!has-siblings {
    background: rgb(41, 56, 71);
}
QTreeView:branch:hover {
    background: rgb(41, 56, 71);
}
QTreeView:branch:selected {
    background: rgb(41, 56, 71);
}
    """)
    w = JsonTreeWidget()
    w.show()
    w.loadData('Data/data.json')
    sys.exit(app.exec_())
