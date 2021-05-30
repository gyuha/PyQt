#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月23日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: ShowImage
@description: 
'''
import sys

from PyQt5.QtCore import QResource
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel

from Lib import res_rc  # @UnresolvedImport @UnusedImport
from Lib.xpmres import image_head  # @UnresolvedImport


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ImageView(QWidget):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QHBoxLayout(self)

        # 파일에서 이미지로드 
        layout.addWidget(QLabel(self, pixmap=QPixmap("Data/head.jpg")))

        # qResource 참조 http://doc.qt.io/qt-5/resources.html. 

        # load 1 자원 파일에서 py 파일에서 1 
        # 转 p pyrcc5 res.qrc -o res_rc.py. 
        #이 방법은 RES.QRC를 PROCC5에서 RES_RC.PY 파일로 전송하는 것입니다. 직접로드 할 수 있습니다. 
        # 경로를 전달할 수 있습니다 : / images/head.jpg에 액세스 할 수 있습니다. 
        layout.addWidget(QLabel(self, pixmap=QPixmap(":/images/head.jpg")))

        # 바이너리 자원 파일 res에서 # RCC. 
        # 转 ts o r 2. B. 
        # 여기서 자원 접두사가 수정 (/ myfile), res2.qrc 파일을 참조하십시오. 
        # 이번에는 등록해야합니다 
        QResource.registerResource("Data/res.rcc")
        # 小 注意 前 
        layout.addWidget(
            QLabel(self, pixmap=QPixmap(":/myfile/images/head.jpg")))

        # XPM 배열에서로드합니다 
        # 도구 도구 / image2xpm.exe로 변환하십시오 
        # 여기서 변환 된 XPM 배열을 PY 파일에 변수로 직접 놓습니다. 
        # xpmres.py에서 image_head를 참조하십시오 
        layout.addWidget(QLabel(self, pixmap=QPixmap(image_head)))

        # 加载 图片 
        movie = QMovie("Data/loading.gif")
        label = QLabel(self)
        label.setMovie(movie)
        layout.addWidget(label)
        movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageView()
    w.show()
    sys.exit(app.exec_())
