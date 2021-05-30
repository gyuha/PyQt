#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/7/31
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: ClipboardMaster
@description: 
"""
from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal, QLoggingCategory, QVariant, QMimeData
from PyQt5.QtRemoteObjects import QRemoteObjectHost
from PyQt5.QtWidgets import QTextBrowser

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

import sys


class WindowMaster(QTextBrowser):
    SignalUpdateMimeData = pyqtSignal(
        bool, QVariant,  # color
        bool, QVariant,  # html
        bool, QVariant,  # image
        bool, QVariant,  # text
        bool, QVariant,  # urls
    )

    def __init__(self, *args, **kwargs):
        super(WindowMaster, self).__init__(*args, **kwargs)
        # 监 板 
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.on_data_changed)
        # 开 节点 
        host = QRemoteObjectHost(QUrl('tcp://0.0.0.0:' + sys.argv[1]), parent=self)
        host.enableRemoting(self, 'WindowMaster')
        self.append('开启节点完成')

    def on_data_changed(self):
        # 服务 服务 端 端 变 变 发化 发 到 
        clipboard = QApplication.clipboard()
        clipboard.blockSignals(True)
        mime_data = clipboard.mimeData()
        self.SignalUpdateMimeData.emit(
            mime_data.hasColor(), mime_data.colorData(),
            mime_data.hasHtml(), mime_data.html(),
            mime_data.hasImage(), mime_data.imageData(),
            mime_data.hasText(), mime_data.text(),
            mime_data.hasUrls(), mime_data.urls(),
        )
        clipboard.blockSignals(False)

    @pyqtSlot(
        bool, QVariant,  # color
        bool, QVariant,  # html
        bool, QVariant,  # image
        bool, QVariant,  # text
        bool, QVariant,  # urls
        bool, QVariant  # files
    )
    def updateMimeData(self,
                       hasColor, color,
                       hasHtml, html,
                       hasImage, image,
                       hasText, text,
                       hasUrls, urls,
                       hasFiles, files,
                       ):
        # 客户户 板 서버와 동기화하십시오 
        self.append('收到客户端发送的剪贴板')
        clipboard = QApplication.clipboard()
        clipboard.blockSignals(True)
        data = QMimeData()
        if hasColor:
            data.setColorData(color)
        if hasHtml:
            data.setHtml(html)
        if hasImage:
            data.setImageData(image)
        if hasText:
            data.setText(text)
        # if hasUrls:
        #     data.setUrls(urls)
        if hasFiles:
            data.setData('')
        clipboard.setMimeData(data)
        clipboard.blockSignals(False)


if __name__ == '__main__':
    import cgitb

    cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication

    QLoggingCategory.setFilterRules('qt.remoteobjects.debug=true\n'
                                    'qt.remoteobjects.warning=true')

    app = QApplication(sys.argv)
    w = WindowMaster()
    w.show()
    sys.exit(app.exec_())
