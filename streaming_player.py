from threading import Thread

import cv2
from PyQt5.QtCore import QObject, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


# 영상 실시간 스트리밍 스레드
class StreamingThread(QObject):
    change_pixmap = pyqtSignal(str, QPixmap)

    def __init__(self):
        super(StreamingThread, self).__init__()
        self.running = True
        self.url = None
        self.Qsize = None
        self.cap = None

    def start(self):
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def set_url(self, url):
        self.url = url

    def set_cctv(self, cctv):
        self.cctv = cctv

    def set_label(self, label, width, height):
        self.label_screen = label
        self.width = width
        self.height = height

    def run(self):
        try:
            # self.cap = cv2.VideoCapture(self.url)
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                while self.running:
                    success, frame = self.cap.read()
                    if success:
                        img = cv2.resize(frame, (self.width, self.height))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        h, w, c = img.shape
                        qImg = QImage(
                            img.data, w, h, w * c, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(qImg)
                        pixmap = pixmap.scaled(
                            QSize(self.width, self.height), Qt.IgnoreAspectRatio)
                        self.change_pixmap.emit(self.cctv, pixmap)
            else:
                # print("RTSP(RTMP) Video Streaming Fail")
                self.stop()
        except Exception as e:
            print(e)
            self.stop()

    def stop(self):
        if self.running:
            self.running = False
            # print("Streaming Stop")
