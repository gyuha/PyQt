#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月29日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: FacePoints
@description: 人脸特征点
'''
from bz2 import BZ2Decompressor
import cgitb
import os
import sys

from PyQt5.QtCore import QTimer, QUrl, QFile, QIODevice
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QLabel, QMessageBox, QApplication
import cv2  # @UnresolvedImport
import dlib
import numpy


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

DOWNSCALE = 4
URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'


class OpencvWidget(QLabel):

    def __init__(self, *args, **kwargs):
        super(OpencvWidget, self).__init__(*args, **kwargs)
        self.httpRequestAborted = False
        self.fps = 24
        self.resize(800, 600)

        if not os.path.exists("Data/shape_predictor_68_face_landmarks.dat"):
            self.setText("正在下载数据文件。。。")
            self.outFile = QFile(
                "Data/shape_predictor_68_face_landmarks.dat.bz2")
            if not self.outFile.open(QIODevice.WriteOnly):
                QMessageBox.critical(self, '错误', '无法写入文件')
                return
            self.qnam = QNetworkAccessManager(self)
            self._reply = self.qnam.get(QNetworkRequest(QUrl(URL)))
            self._reply.finished.connect(self.httpFinished)
            self._reply.readyRead.connect(self.httpReadyRead)
            self._reply.downloadProgress.connect(self.updateDataReadProgress)
        else:
            self.startCapture()

    def httpFinished(self):
        self.outFile.close()
        if self.httpRequestAborted or self._reply.error():
            self.outFile.remove()
        self._reply.deleteLater()
        del self._reply
        # # 下载 압축 해제 된 파일을 완성하고 카메라를로드하십시오. 
        self.setText("正在解压数据。。。")
        try:
            bz = BZ2Decompressor()
            data = bz.decompress(
                open('Data/shape_predictor_68_face_landmarks.dat.bz2', 'rb').read())
            open('Data/shape_predictor_68_face_landmarks.dat', 'wb').write(data)
        except Exception as e:
            self.setText('解压失败：' + str(e))
            return
        self.setText('正在开启摄像头。。。')
        self.startCapture()

    def httpReadyRead(self):
        self.outFile.write(self._reply.readAll())
        self.outFile.flush()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        self.setText('已下载：{} %'.format(round(bytesRead / 64040097 * 100, 2)))

    def startCapture(self):
        self.setText("请稍候，正在初始化数据和摄像头。。。")
        try:
            # # 相关 相关 
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor(
                "Data/shape_predictor_68_face_landmarks.dat")
            cascade_fn = "Data/lbpcascades/lbpcascade_frontalface.xml"
            self.cascade = cv2.CascadeClassifier(cascade_fn)
            if not self.cascade:
                return QMessageBox.critical(self, "错误", cascade_fn + " 无法找到")
            self.cap = cv2.VideoCapture(0)
            if not self.cap or not self.cap.isOpened():
                return QMessageBox.critical(self, "错误", "打开摄像头失败")
            # 开 开 타이머 타이머 캡처 
            self.timer = QTimer(self, timeout=self.onCapture)
            self.timer.start(1000 / self.fps)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def closeEvent(self, event):
        if hasattr(self, "_reply") and self._reply:
            self.httpRequestAborted = True
            self._reply.abort()
            try:
                os.unlink("Data/shape_predictor_68_face_landmarks.dat.bz2")
            except:
                pass
            try:
                os.unlink("Data/shape_predictor_68_face_landmarks.dat")
            except:
                pass
        if hasattr(self, "timer"):
            self.timer.stop()
            self.timer.deleteLater()
            self.cap.release()
            del self.predictor, self.detector, self.cascade, self.cap
        super(OpencvWidget, self).closeEvent(event)
        self.deleteLater()

    def onCapture(self):
        _, frame = self.cap.read()

        minisize = (
            int(frame.shape[1] / DOWNSCALE), int(frame.shape[0] / DOWNSCALE))
        tmpframe = cv2.resize(frame, minisize)
        tmpframe = cv2.cvtColor(tmpframe, cv2.COLOR_BGR2GRAY)  # 회색 치료를하십시오 
        tmpframe = cv2.equalizeHist(tmpframe)

        # minneighbors 각 목표는 적어도 5 번이고 
        faces = self.cascade.detectMultiScale(tmpframe, minNeighbors=5)
        del tmpframe
        if len(faces) < 1:  # 아무 얼굴도 없어 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(
                frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            del frame
            return self.setPixmap(QPixmap.fromImage(img))
        # 特征点 검출 묘사 
        for x, y, w, h in faces:
            x, y, w, h = x * DOWNSCALE, y * DOWNSCALE, w * DOWNSCALE, h * DOWNSCALE
            # 画脸 
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
            # 人 
            tmpframe = frame[y:y + h, x:x + w]
            # 기능 포인트 묘사를 취하십시오 
            rects = self.detector(tmpframe, 1)
            if len(rects) > 0:
                landmarks = numpy.matrix(
                    [[p.x, p.y] for p in self.predictor(tmpframe, rects[0]).parts()])
                for _, point in enumerate(landmarks):
                    pos = (point[0, 0] + x, point[0, 1] + y)
                    # 원래의 그림에 플리가 가리 킵니다 
                    cv2.circle(frame, pos, 3, color=(0, 255, 0))
            # 转 q q 能 能. 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(
                frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            del frame
            self.setPixmap(QPixmap.fromImage(img))


if __name__ == "__main__":
    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = OpencvWidget()
    w.show()
    sys.exit(app.exec_())
