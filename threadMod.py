from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
import cv2

# 영상 실시간 스트리밍 스레드
class StreamingThread(QThread):

    def __init__(self):
        super(StreamingThread, self).__init__()
        self.running = True
        self.camUrl = None
        self.Qsize = None
        self.cap = None

    def setRtsp(self, camUrl):
        self.camUrl = camUrl

    def setSize(self, width, height):
        self.width = width
        self.height = height
    
    def setLabel(self, label):
        self.label_screen = label
        
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
                        # pixmap.scaled(QSize(200,200), aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
                        self.label_screen.setPixmap(pixmap)
                        #time.sleep(.01)
            else:
                print("RTSP(RTMP) Video Streaming Fail")
                self.stop()
        except Exception as e:
            print(e)
            self.stop()

    def stop(self):
        if self.running:
            self.running = False
            print("Streaming Stop")
        self.quit()