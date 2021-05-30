#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月10日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: ChineseText
@description: 修改消息对话框文字汉化
"""
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

TextStyle = """
QMessageBox QPushButton[text="OK"] {
    qproperty-text: "好的";
}
QMessageBox QPushButton[text="Open"] {
    qproperty-text: "打开";
}
QMessageBox QPushButton[text="Save"] {
    qproperty-text: "保存";
}
QMessageBox QPushButton[text="Cancel"] {
    qproperty-text: "取消";
}
QMessageBox QPushButton[text="Close"] {
    qproperty-text: "关闭";
}
QMessageBox QPushButton[text="Discard"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Don't Save"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Apply"] {
    qproperty-text: "应用";
}
QMessageBox QPushButton[text="Reset"] {
    qproperty-text: "重置";
}
QMessageBox QPushButton[text="Restore Defaults"] {
    qproperty-text: "恢复默认";
}
QMessageBox QPushButton[text="Help"] {
    qproperty-text: "帮助";
}
QMessageBox QPushButton[text="Save All"] {
    qproperty-text: "保存全部";
}
QMessageBox QPushButton[text="&Yes"] {
    qproperty-text: "是";
}
QMessageBox QPushButton[text="Yes to &All"] {
    qproperty-text: "全部都是";
}
QMessageBox QPushButton[text="&No"] {
    qproperty-text: "不";
}
QMessageBox QPushButton[text="N&o to All"] {
    qproperty-text: "全部都不";
}
QMessageBox QPushButton[text="Abort"] {
    qproperty-text: "终止";
}
QMessageBox QPushButton[text="Retry"] {
    qproperty-text: "重试";
}
QMessageBox QPushButton[text="Ignore"] {
    qproperty-text: "忽略";
}
"""

app = QApplication(sys.argv)

# QSS 스타일을 통해 버튼 텍스트를 설정하십시오 
app.setStyleSheet(TextStyle)

# 오랜 기록으로 인해 QT5의 번역 기능이 업데이트되지 않았거나 사용할 때 사용되는 이전 구조를 번역 할 수 없습니다. 
# 这里 不 不 (QM에 다시 컴파일 할 TS 소스 코드를 수정해야합니다) 
# translator = QTranslator()
# print(translator.load(QLocale(), 'qt', '_', QLibraryInfo.location(
#     QLibraryInfo.TranslationsPath)))
# app.installTranslator(translator)

QMessageBox.information(
    None, 'information', '消息',
    QMessageBox.Ok |
    QMessageBox.Open |
    QMessageBox.Save |
    QMessageBox.Cancel |
    QMessageBox.Close |
    QMessageBox.Discard |
    QMessageBox.Apply |
    QMessageBox.Reset |
    QMessageBox.RestoreDefaults |
    QMessageBox.Help |
    QMessageBox.SaveAll |
    QMessageBox.Yes |
    QMessageBox.YesToAll |
    QMessageBox.No |
    QMessageBox.NoToAll |
    QMessageBox.Abort |
    QMessageBox.Retry |
    QMessageBox.Ignore
)
sys.exit()
