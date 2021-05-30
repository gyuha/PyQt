#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: WorldMap
@description: 
"""
import json
import math

from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPainter, QPolygonF, QPen, QBrush
from PyQt5.QtOpenGL import QGLFormat
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class GraphicsView(QGraphicsView):

    # 배경 영역 색상 
    backgroundColor = QColor(31, 31, 47)
    # 테두리 색상 
    borderColor = QColor(58, 58, 90)

    def __init__(self, *args, **kwargs):
        super(GraphicsView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 배경색을 설정합니다 
        self.setBackgroundBrush(self.backgroundColor)
        '''
        # 参考 http://doc.qt.io/qt-5/qgraphicsview.html#cachemodeflag-enum. 
        CacheNone                    不使用缓存
        CacheBackground              缓存背景
        '''
        self.setCacheMode(self.CacheBackground)
        '''
        # 参考 http://doc.qt.io/qt-5/qgraphicsview.html#dragmode-enum. 
        NoDrag                       什么都没发生; 鼠标事件被忽略。
        ScrollHandDrag               光标变成指针，拖动鼠标将滚动滚动条。 该模式可以在交互式和非交互式模式下工作。
        RubberBandDrag               拖动鼠标将设置橡皮筋几何形状，并选择橡皮筋所覆盖的所有项目。 对于非交互式视图，此模式被禁用。
        '''
        self.setDragMode(self.ScrollHandDrag)
        '''
        # 参考 http://doc.qt.io/qt-5/qgraphicsview.html#optimizationflag-enum. 
        DontClipPainter              已过时
        DontSavePainterState         渲染时，QGraphicsView在渲染背景或前景时以及渲染每个项目时保护painter状态（请参阅QPainter.save()）。 这允许你离开painter处于改变状态（即你可以调用QPainter.setPen()或QPainter.setBrush()，而不需要在绘制之后恢复状态）。 但是，如果项目一致地恢复状态，则应启用此标志以防止QGraphicsView执行相同的操作。
        DontAdjustForAntialiasing    禁用QGraphicsView的抗锯齿自动调整曝光区域。 在QGraphicsItem.boundingRect()的边界上渲染反锯齿线的项目可能会导致渲染部分线外。 为了防止渲染失真，QGraphicsView在所有方向上将所有曝光区域扩展2个像素。 如果启用此标志，QGraphicsView将不再执行这些调整，最大限度地减少需要重绘的区域，从而提高性能。 一个常见的副作用是，使用抗锯齿功能进行绘制的项目可能会在移动时在画面上留下绘画痕迹。
        IndirectPainting             从Qt 4.6开始，恢复调用QGraphicsView.drawItems()和QGraphicsScene.drawItems()的旧绘画算法。 仅用于与旧代码的兼容性。
        '''
        self.setOptimizationFlag(self.DontSavePainterState)
        '''
        # 参考 http://doc.qt.io/qt-5/qpainter.html#RenderHint-enum. 
        Antialiasing                 抗锯齿
        TextAntialiasing             文本抗锯齿
        SmoothPixmapTransform        平滑像素变换算法
        HighQualityAntialiasing      请改用Antialiasing
        NonCosmeticDefaultPen        已过时
        Qt4CompatiblePainting        从Qt4移植到Qt5可能有用
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)
        if QGLFormat.hasOpenGL():
            self.setRenderHint(QPainter.HighQualityAntialiasing)
        '''
        # 뷰가 조정되면보기가 장면을 찾습니다. 뷰포트 제어의 크기가 변경되면 뷰포트에서 장면을 찾는 방법을 결정하려면이 속성을 사용하십시오. 기본 동작 Noanchor는 조정 크기 중에 장면의 위치를 ​​변경하지 않습니다. 뷰의 왼쪽 상단 모서리가 조정 크기에 고정 된 것으로 표시됩니다. 장면의 일부가 표시되는 경우 (즉, 스크롤 막대가있을 때)이 속성의 효과는 분명합니다. 그렇지 않으면 전체 장면이 뷰에 적합한 경우 QGraphicsScene이 뷰를 사용하여보기의 장면을 정렬합니다. 
        # 参考 http://doc.qt.io/qt-5/qgraphicsview.html#vortanchor-enum. 
        NoAnchor                     视图保持场景的位置不变
        AnchorViewCenter             视图中心被用作锚点。
        AnchorUnderMouse             鼠标当前位置被用作锚点
        '''
        self.setResizeAnchor(self.AnchorUnderMouse)
        '''
        Rubber选择模式
        # 参考 http://doc.qt.io/qt-5/qt.html#itemselectionMode-Enum. 
        ContainsItemShape            输出列表仅包含形状完全包含在选择区域内的项目。 不包括与区域轮廓相交的项目。
        IntersectsItemShape          默认，输出列表包含其形状完全包含在选择区域内的项目以及与区域轮廓相交的项目。
        ContainsItemBoundingRect     输出列表仅包含边界矩形完全包含在选择区域内的项目。 不包括与区域轮廓相交的项目。
        IntersectsItemBoundingRect   输出列表包含边界矩形完全包含在选择区域内的项目以及与区域轮廓相交的项目。 这种方法通常用于确定需要重绘的区域。
        '''
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        '''
        # 변환 프로세스 중에보기를 찾는 방법. QGraphicsView이 속성을 사용하여 변환 행렬이 변경 될 때 장면을 찾는 방법을 결정하고보기의 좌표계가 변형됩니다. 기본 동작 anchorViewCenter 변환 중에보기 중앙의 장면이 변경되지 않은지 (예 : 회전시, 장면이보기의 중심을 중심으로 회전합니다). 장면의 일부가 표시되는 경우 (즉, 스크롤 막대가있을 때)이 속성의 효과는 분명합니다. 그렇지 않으면 전체 장면이 뷰에 적합한 경우 QGraphicsScene이 뷰를 사용하여보기의 장면을 정렬합니다. 
        # 参考 http://doc.qt.io/qt-5/qgraphicsview.html#vortanchor-enum. 
        NoAnchor                     视图保持场景的位置不变
        AnchorViewCenter             视图中心被用作锚点。
        AnchorUnderMouse             鼠标当前位置被用作锚点
        '''
        self.setTransformationAnchor(self.AnchorUnderMouse)
# qglformat.hasopengl () : OpenGL이 켜져 있으면 OpenGL 위젯을 사용하십시오. 
#             self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        '''
        # 参考 http://doc.qt.io/qt-5/qgraphicsview.html#ViewPortUpdateMode-Enum. 
        FullViewportUpdate           当场景的任何可见部分改变或重新显示时，QGraphicsView将更新整个视口。 当QGraphicsView花费更多的时间来计算绘制的内容（比如重复更新很多小项目）时，这种方法是最快的。 这是不支持部分更新（如QGLWidget）的视口以及需要禁用滚动优化的视口的首选更新模式。
        MinimalViewportUpdate        QGraphicsView将确定需要重绘的最小视口区域，通过避免重绘未改变的区域来最小化绘图时间。 这是QGraphicsView的默认模式。 虽然这种方法提供了一般的最佳性能，但如果场景中有很多小的可见变化，QGraphicsView最终可能花费更多的时间来寻找最小化的方法。
        SmartViewportUpdate          QGraphicsView将尝试通过分析需要重绘的区域来找到最佳的更新模式。
        BoundingRectViewportUpdate   视口中所有更改的边界矩形将被重绘。 这种模式的优点是，QGraphicsView只搜索一个区域的变化，最大限度地减少了花在确定需要重绘的时间。 缺点是还没有改变的地方也需要重新绘制。
        NoViewportUpdate             当场景改变时，QGraphicsView将永远不会更新它的视口。 预计用户将控制所有更新。 此模式禁用QGraphicsView中的所有（可能较慢）项目可见性测试，适用于要求固定帧速率或视口以其他方式在外部进行更新的场景。
        '''
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        # 장면을 설정하십시오 (지도의 위도와 경도에 따라 화면에 원본을 표시하십시오) 
        self._scene = QGraphicsScene(-180, -90, 360, 180, self)
        self.setScene(self._scene)

        #지도 초기화 
        self.initMap()

    def wheelEvent(self, event):
        # 滑 轮 이벤트 
        if event.modifiers() & Qt.ControlModifier:
            self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))
            return event.accept()
        super(GraphicsView, self).wheelEvent(event)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(
            scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def initMap(self):
        features = json.load(
            open("Data/world.json", encoding="utf8")).get("features")
        for feature in features:
            geometry = feature.get("geometry")
            if not geometry:
                continue
            _type = geometry.get("type")
            coordinates = geometry.get("coordinates")
            for coordinate in coordinates:
                if _type == "Polygon":
                    polygon = QPolygonF(
                        [QPointF(latitude, -longitude) for latitude, longitude in coordinate])
                    item = QGraphicsPolygonItem(polygon)
                    item.setPen(QPen(self.borderColor, 0))
                    item.setBrush(QBrush(self.backgroundColor))
                    item.setPos(0, 0)
                    self._scene.addItem(item)
                elif _type == "MultiPolygon":
                    for _coordinate in coordinate:
                        polygon = QPolygonF(
                            [QPointF(latitude, -longitude) for latitude, longitude in _coordinate])
                        item = QGraphicsPolygonItem(polygon)
                        item.setPen(QPen(self.borderColor, 0))
                        item.setBrush(QBrush(self.backgroundColor))
                        item.setPos(0, 0)
                        self._scene.addItem(item)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    print("OpenGL Status:", QGLFormat.hasOpenGL())
    view = GraphicsView()
    view.setWindowTitle("世界地图")
    view.show()
    sys.exit(app.exec_())
