#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月26日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: FileSystemModel
@description: 
"""
import sys

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel, QFileIconProvider, QApplication,\
    QTreeView


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

# 图 图 图 提供 


class FileIconProvider(QFileIconProvider):

    def __init__(self, *args, **kwargs):
        super(FileIconProvider, self).__init__(*args, **kwargs)
        self.DirIcon = QIcon("Data/icons/folder.png")
        self.TxtIcon = QIcon("Data/icons/file.png")

    def icon(self, type_info):
        '''
        :param fileInfo: 参考http://doc.qt.io/qt-5/qfileinfo.html
        '''
        if isinstance(type_info, QFileInfo):
            # type_info가 QFileInfo 유형 인 경우 GetInfoIcon을 사용하여 아이콘을 반환합니다. 
            return self.getInfoIcon(type_info)
        # type_info가 QFileIconProvider의 자체 iContype 열거 형 유형의 유형이면 다음 메소드가 수행됩니다. 
        # 이것은 단지 여러 유형의 범용, 참조 http : //doc.qt.io/qt-5/qfileiconprovider.html#icondype-enum 
        '''
        QFileIconProvider::Computer     0
        QFileIconProvider::Desktop      1
        QFileIconProvider::Trashcan     2
        QFileIconProvider::Network      3
        QFileIconProvider::Drive        4
        QFileIconProvider::Folder       5
        QFileIconProvider::File         6
        '''
        if type_info == QFileIconProvider.Folder:
            # 폴더 인 경우 # 
            return self.DirIcon
        return super(FileIconProvider, self).icon(type_info)

    def getInfoIcon(self, type_info):
        if type_info.isDir():  # 폴더 
            return self.DirIcon
        if type_info.isFile() and type_info.suffix() == "txt":  # 파일과 txt입니다 
            return self.TxtIcon
        return super(FileIconProvider, self).icon(type_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = QFileSystemModel()
    model.setIconProvider(FileIconProvider())  # 클래스를 제공하는 사용자 정의 아이콘으로 설정합니다 
    model.setRootPath("")
    tree = QTreeView()
    tree.setModel(model)

    tree.setAnimated(False)
    tree.setIndentation(20)
    tree.setSortingEnabled(True)

    tree.setWindowTitle("Dir View")
    tree.resize(640, 480)
    tree.show()

    sys.exit(app.exec_())
