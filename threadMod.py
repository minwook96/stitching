from PyQt5.QtCore import QThread, QSize, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import tkinter as tk
from time import sleep
import cv2
from threading import Thread

# 영상 실시간 스트리밍 스레드
class StreamingThread(QObject):
    changePixmap = pyqtSignal(str, QPixmap)
    
    def __init__(self):
        super(StreamingThread, self).__init__()
        self.running = True
        self.camUrl = None
        self.Qsize = None
        self.cap = None
        
    def start(self):
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def setRtsp(self, camUrl):
        self.camUrl = camUrl

    def setCctv(self, cctv):
        self.cctv = cctv
        
    def setSize(self, width, height):
        self.width = width
        self.height = height
    
    def setLabel(self, label):
        self.label_screen = label
    
    def setFullSize(self, camUrl):
        self.camUrl = camUrl
        self.windowScreenSize()
    
    def windowScreenSize(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 5
        self.Qsize = QSize(screen_width, screen_height) 
        
    def run(self):
        try:
            self.cap = cv2.VideoCapture(self.camUrl)
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
                        # pixmap.scaled(QSize(200,200), Qt.AspectRatioMode.KeepAspectRatio)
                        pixmap = pixmap.scaled(QSize(self.width, self.height), Qt.IgnoreAspectRatio)
                        # self.label_screen.setPixmap(pixmap)
                        self.changePixmap.emit(self.cctv, pixmap)
                        # sleep(.01)
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
        # self.quit()