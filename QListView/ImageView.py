#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/4/15
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: ImageView
@description: 
"""
import os

from PyQt5.QtCore import QPointF, Qt, QRectF, QSizeF
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPainter, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QListView, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

ScrollPixel = 40


class BigImageView(QGraphicsView):
    """图片查看控件"""

    def __init__(self, *args, **kwargs):
        image = kwargs.pop('image', None)
        background = kwargs.pop('background', None)
        super(BigImageView, self).__init__(*args, **kwargs)
        self.setCursor(Qt.OpenHandCursor)
        self.setBackground(background)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.setCacheMode(self.CacheBackground)
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self._item = QGraphicsPixmapItem()  # 이미지를 배치합니다 
        self._item.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                            QGraphicsPixmapItem.ItemIsMovable)
        self._scene = QGraphicsScene(self)  # 장면 
        self.setScene(self._scene)
        self._scene.addItem(self._item)
        rect = QApplication.instance().desktop().availableGeometry()
        self.resize(int(rect.width() * 2 / 3), int(rect.height() * 2 / 3))

        self.pixmap = None
        self._delta = 0.1  # 줌 
        self.setPixmap(image)

    def setBackground(self, color):
        """设置背景颜色
        :param color: 背景颜色
        :type color: QColor or str or GlobalColor
        """
        if isinstance(color, QColor):
            self.setBackgroundBrush(color)
        elif isinstance(color, (str, Qt.GlobalColor)):
            color = QColor(color)
            if color.isValid():
                self.setBackgroundBrush(color)

    def setPixmap(self, pixmap, fitIn=True):
        """加载图片
        :param pixmap: 图片或者图片路径
        :param fitIn: 是否适应
        :type pixmap: QPixmap or QImage or str
        :type fitIn: bool
        """
        if isinstance(pixmap, QPixmap):
            self.pixmap = pixmap
        elif isinstance(pixmap, QImage):
            self.pixmap = QPixmap.fromImage(pixmap)
        elif isinstance(pixmap, str) and os.path.isfile(pixmap):
            self.pixmap = QPixmap(pixmap)
        else:
            return
        self._item.setPixmap(self.pixmap)
        self._item.update()
        self.setSceneDims()
        if fitIn:
            self.fitInView(QRectF(self._item.pos(), QSizeF(
                self.pixmap.size())), Qt.KeepAspectRatio)
        self.update()

    def setSceneDims(self):
        if not self.pixmap:
            return
        self.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixmap.width(), self.pixmap.height())))

    def fitInView(self, rect, flags=Qt.IgnoreAspectRatio):
        """剧中适应
        :param rect: 矩形范围
        :param flags:
        :return:
        """
        if not self.scene() or rect.isNull():
            return
        unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewRect = self.viewport().rect()
        sceneRect = self.transform().mapRect(rect)
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        if flags == Qt.KeepAspectRatio:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        self.scale(x_ratio, y_ratio)
        self.centerOn(rect.center())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1 + self._delta)

    def zoomOut(self):
        """缩小"""
        self.zoom(1 - self._delta)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        _factor = self.transform().scale(
            factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if _factor < 0.07 or _factor > 100:
            # 너무 많이 예방하십시오 
            return
        self.scale(factor, factor)


class ImageView(QListView):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.setFrameShape(self.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(self.NoEditTriggers)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(Qt.IgnoreAction)
        self.setSelectionMode(self.ExtendedSelection)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(6)
        self.setViewMode(self.IconMode)
        self.setWordWrap(True)
        self.setSelectionRectVisible(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 끌기를 맨 위로 또는 자동 스크롤 해결 
        self.setAutoScrollMargin(150)
        self.verticalScrollBar().setSingleStep(ScrollPixel)
        # setupel. 
        self.dmodel = QStandardItemModel(self)
        self.setModel(self.dmodel)

        # 大 图 조절기 
        self.bigView = BigImageView(background='#323232')

    def addItem(self, image):
        if isinstance(image, str):
            image = QPixmap(image)
        # 항목을 추가하십시오 
        item = QStandardItem()
        # 원래 그림을 녹화하십시오 
        item.setData(image, Qt.UserRole + 1)  # 取 用 用 双 
        # 작은 그림과 디스플레이로 확대하십시오 
        item.setData(image.scaled(60, 60, Qt.IgnoreAspectRatio, Qt.SmoothTransformation), Qt.DecorationRole)
        # 인터페이스에 항목을 추가하십시오 
        self.dmodel.appendRow(item)

    def count(self):
        return self.dmodel.rowCount()

    def setCurrentRow(self, row):
        self.setCurrentIndex(self.dmodel.index(row, 0))

    def currentRow(self):
        return self.currentIndex().row()

    def updateGeometries(self):
        # 一 滑 20 20px. 
        super(ImageView, self).updateGeometries()
        self.verticalScrollBar().setSingleStep(ScrollPixel)

    def closeEvent(self, event):
        # 미리보기 창을 닫습니다 
        self.bigView.close()
        super(ImageView, self).closeEvent(event)

    def wheelEvent(self, event):
        # 修 修 滑 B. 
        if self.flow() == QListView.LeftToRight:
            bar = self.horizontalScrollBar()
            value = ScrollPixel if event.angleDelta().y() < 0 else (0 - ScrollPixel)
            bar.setSliderPosition(bar.value() + value)
        else:
            super(ImageView, self).wheelEvent(event)

    def mouseDoubleClickEvent(self, event):
        # 萱 ✍ 항목 처리 프로세스를 입력 할 항목이있는 경우 두 번 클릭합니다. 그렇지 않으면 그림 기능을 호출합니다. 
        index = self.indexAt(event.pos())
        if index and index.isValid():
            item = self.dmodel.itemFromIndex(index)
            if item:
                # 새 창을 표시하려면 원본 이미지를 제거하십시오 
                image = item.data(Qt.UserRole + 1)
                self.bigView.setPixmap(image)
                self.bigView.show()
            return
        super(ImageView, self).mouseDoubleClickEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ImageView()
    w.show()

    # 아날로그 이미지를 추가하십시오 
    for i in range(3):
        for name in os.listdir('ScreenShot'):
            w.addItem(os.path.join('ScreenShot', name))
    sys.exit(app.exec_())
