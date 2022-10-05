from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread
from qt_material import apply_stylesheet
import ui.ui_main as ui_main
from onvif import ONVIFCamera
from threadMod import StreamingThread
import stitching
from time import sleep
import datetime
import logging
import os
import sys
import cv2

# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.threads = []
        self.channelFile = os.path.join(os.path.abspath(''), 'channel.conf')

        # 첫번째 탭으로 시작
        self.QStackedWidget.setCurrentIndex(0)

        # 버튼 기능 구현
        self.nextButton.clicked.connect(self.nextpage)
        self.previousButton.clicked.connect(self.prevpage)
        # self.previousButton.setEnabled(False)
        self.panoramaButton.clicked.connect(self.panorama)
        self.upButton.pressed.connect(lambda: self.ptzControl('up'))
        self.downButton.pressed.connect(lambda: self.ptzControl('down'))
        self.leftButton.pressed.connect(lambda: self.ptzControl('left'))
        self.rightButton.pressed.connect(lambda: self.ptzControl('right'))
        self.zoomOutButton.pressed.connect(lambda: self.ptzControl('zoomOut'))
        self.zoomInButton.pressed.connect(lambda: self.ptzControl('zoomIn'))
        self.homeButton.clicked.connect(lambda: self.ptzControl('home'))
        self.upButton.released.connect(lambda: self.ptzControl('stop'))
        self.downButton.released.connect(lambda: self.ptzControl('stop'))
        self.leftButton.released.connect(lambda: self.ptzControl('stop'))
        self.rightButton.released.connect(lambda: self.ptzControl('stop'))
        self.zoomOutButton.released.connect(lambda: self.ptzControl('stop'))
        self.zoomInButton.released.connect(lambda: self.ptzControl('stop'))
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        self.zoomOutButton.setEnabled(False)
        self.zoomInButton.setEnabled(False)
        self.homeButton.setEnabled(False)
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        self.zoomOutButton.setEnabled(False)
        self.zoomInButton.setEnabled(False)
        self.chComboBox.activated.connect(self.setCCTV)

        self.mStreamingThread = StreamingThread()
        self.setCCTVTree()

    # CCTV Tree UI에 트리구조로 표시
    def setCCTVTree(self):
        self.chTreeWidget.clear()
        self.cctvIpList = []
        self.rtspList = []
        if os.path.exists(self.channelFile):
            with open(self.channelFile, 'r') as file:
                numbers = []
                lines = file.readlines()
                String = 'No Channel'
                self.chComboBox.clear()
                self.chComboBox_2.clear()
                self.chComboBox.addItem(String)
                self.chComboBox_2.addItem(String)

                for line in lines:
                    sLine = line.split(',')
                    numbers.append([sLine[0], sLine[1], sLine[2]])

                numbers.sort()

                for cctv, rtsp, ip in numbers:
                    item = QTreeWidgetItem(self.chTreeWidget)
                    self.chComboBox.addItem(cctv)
                    self.chComboBox_2.addItem(cctv)
                    item.setText(0, cctv)
                    item.setText(1, rtsp)
                    self.cctvIpList.append(ip[:-1])
                    self.rtspList.append(rtsp)
                    self.chTreeWidget.addTopLevelItem(item)
            self.ptzButton.pressed.connect(self.panoramaPTZ)

    # QThread 클래스 선언하기, QThread 클래스를 쓰려면 QtCore 모듈을 import 해야함.
    class Panorama(QThread):
        def __init__(self, parent, cctvIp, rtsp, num): # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
            super().__init__(parent)
            self.parent = parent # self.parent를 사용하여 WindowClass 위젯을 제어할 수 있다.
            self.cctvIp = cctvIp
            self.rtsp = rtsp
            self.num = num
            
        def run(self):
            self.parent.tourStart(self.cctvIp, self.rtsp, self.num)

    def panoramaPTZ(self):        
        print(self.cctvIpList)
        for i in range(0, len(self.cctvIpList)):
            self.panorama = self.Panorama(self, self.cctvIpList[i], self.rtspList[i], i)
            self.threads.append(self.panorama)
            self.panorama.start()

    # 화면에 영상 부착 (스레드 실행)
    def setCCTV(self):
        # Index 0: No Channel
        if self.chComboBox.currentIndex() == 0:
            self.mStreamingThread.stop()
            self.mStreamingThread = StreamingThread()
            # 라벨 초기화 스케줄러
            sched = BackgroundScheduler()
            sched.add_job(self.clearChannel, 'date', run_date=datetime.datetime.now(
            ) + datetime.timedelta(seconds=1), args=[self.viewLabel])
            sched.start()
        else:
            channel, rtsp, cctvIp = self.findRtsp(self.chComboBox)
            if rtsp != '' and channel != '':
                self.mStreamingThread.stop()
                self.mStreamingThread.wait(1)
                self.mStreamingThread = StreamingThread()
                self.mStreamingThread.setRtsp(rtsp)
                self.mStreamingThread.setSize(
                    self.viewLabel.width(), self.viewLabel.height())
                self.mStreamingThread.setLabel(self.viewLabel)
                self.mStreamingThread.start()
                self.ptzSetting(cctvIp)
                logger.info("Channel Streaming Success")

    # NoChannel => 라벨 초기화
    def clearChannel(self, cctv):
        cctv.clear()
        cctv.setText('No Channel')

    # ComboBox에서 CCTV 선택했을 때 rtsp 주소 검색
    def findRtsp(self, qComboBox):
        rtsp = ''
        if os.path.exists(self.channelFile):
            with open(self.channelFile, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    sLine = line.split(',')
                    if sLine[0] == qComboBox.currentText():
                        rtsp = sLine[1].strip()
                        cctvIp = sLine[2].strip()
                        break
        cctv = sLine[0]
        return cctv, rtsp, cctvIp

    # PTZ 카메라 기본 변수 선언
    def ptzSetting(self, cctvIp):
        if cctvIp != "":
            try:
                cam = ONVIFCamera(cctvIp, 80, "admin", "tmzkdl123$")
                media = cam.create_media_service()
                self.ptz = cam.create_ptz_service()
                self.media_profile = media.GetProfiles()[0]
                self.status = self.ptz.GetStatus({
                    'ProfileToken': self.media_profile.token,
                })
                self.upButton.setEnabled(True)
                self.downButton.setEnabled(True)
                self.leftButton.setEnabled(True)
                self.rightButton.setEnabled(True)
                self.zoomOutButton.setEnabled(True)
                self.zoomInButton.setEnabled(True)
                self.homeButton.setEnabled(True)
                self.upButton.setEnabled(True)
                self.downButton.setEnabled(True)
                self.leftButton.setEnabled(True)
                self.rightButton.setEnabled(True)
                self.zoomOutButton.setEnabled(True)
                self.zoomInButton.setEnabled(True)
                logger.info(self.status)
                return True
            except:
                self.upButton.setEnabled(False)
                self.downButton.setEnabled(False)
                self.leftButton.setEnabled(False)
                self.rightButton.setEnabled(False)
                self.zoomOutButton.setEnabled(False)
                self.zoomInButton.setEnabled(False)
                self.homeButton.setEnabled(False)
                self.upButton.setEnabled(False)
                self.downButton.setEnabled(False)
                self.leftButton.setEnabled(False)
                self.rightButton.setEnabled(False)
                self.zoomOutButton.setEnabled(False)
                self.zoomInButton.setEnabled(False)
                logger.error("Error PTZ Connecting")
                return False

    # PTZ 작동
    def ptzControl(self, command):
        # if self.ptzSetting(self.chComboBox.currentText()) is True:
            if command == "stop":
                self.ptz.Stop({'ProfileToken': self.media_profile.token})

            else:
                if command == "up":
                    self.ptz.ContinuousMove({
                        'ProfileToken': self.media_profile.token,
                        'Velocity': {
                            'PanTilt': {
                                'x': 0,
                                'y': 0.1
                            },
                            'Zoom': {
                                'x': 0
                            }
                        }
                    })
                if command == "down":
                    self.ptz.ContinuousMove({
                        'ProfileToken': self.media_profile.token,
                        'Velocity': {
                            'PanTilt': {
                                'x': 0,
                                'y': -0.1
                            },
                            'Zoom': {
                                'x': 0
                            }
                        }
                    })
                if command == "left":
                    self.ptz.ContinuousMove({
                        'ProfileToken': self.media_profile.token,
                        'Velocity': {
                            'PanTilt': {
                                'x': -0.1,
                                'y': 0
                            },
                            'Zoom': {
                                'x': 0
                            }
                        }
                    })
                if command == "right":
                    self.ptz.ContinuousMove({
                        'ProfileToken': self.media_profile.token,
                        'Velocity': {
                            'PanTilt': {
                                'x': 0.1,
                                'y': 0
                            },
                            'Zoom': {
                                'x': 0
                            }
                        }
                    })
                if command == "home":
                    self.ptz.GotoHomePosition(
                        {'ProfileToken': self.media_profile.token})
                if command == "zoomIn":
                    self.ptz.ContinuousMove({
                        'ProfileToken': self.media_profile.token,
                        'Velocity': {
                            'Zoom': {
                                'x': 1
                            }
                        }
                    })
                if command == "zoomOut":
                    self.ptz.ContinuousMove({
                        'ProfileToken': self.media_profile.token,
                        'Velocity': {
                            'Zoom': {
                                'x': -1
                            }
                        }
                    })

    def tourStart(self, ipList, rtsp, num):
        ip = ipList
        if self.ptzSetting(ip) is True:
            try:
                preset = self.ptz.GetPresets({
                'ProfileToken': self.media_profile.token
                })
                for i in range(0, len(preset)):
                    self.ptz.GotoPreset({
                        'ProfileToken': self.media_profile.token,
                        'PresetToken': preset[i].token
                    })
                    cap = cv2.VideoCapture(rtsp)
                    # 이미지 캡처
                    success, frame = cap.read()
                    image_folder = "imgs/{}/".format(datetime.datetime.today().strftime("%Y-%m-%d"))
                    image_name = f"panorama{num+1}_{i}.jpg"
                    self.create_folder(image_folder)
                    sleep(3)

                    cv2.imwrite(image_folder + image_name, frame)

                    sleep(3)

                    self.ptz.GotoHomePosition(
                        {'ProfileToken': self.media_profile.token})
                    eval('self.label_'+str(num+1)).setText("Success")
            except:
                logger.error("PTZ Preset")

        else:
            eval('self.label_'+str(num+1)).setText("Fail")
            logger.error("preset tour fail")

    def create_folder(self, directory_path):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
        except OSError:
            logger.error('Error: Creating directory. ' + directory_path)

    def panorama(self):
        print("panorama click")
        ## 가져오고자 하는 폴더 주소
        path="imgs/{}/".format(datetime.datetime.today().strftime("%Y-%m-%d"))
        file_list=os.listdir(path)
        ## 확장자명 입력
        file_list_jpg=[path + file for file in file_list if file.endswith(".jpg")]
        print(file_list_jpg)
        image_folder = "imgs/result/{}/".format(datetime.datetime.today().strftime("%Y-%m-%d"))
        self.create_folder(image_folder)
        stitcher = stitching.Stitcher()
        panoramaImage = stitcher.stitch(file_list_jpg)
        cv2.imwrite(image_folder + "result.jpg", panoramaImage)
        sleep(2)
        self.panoramaLabel.setPixmap(QPixmap(image_folder + "result.jpg").scaled(
            self.panoramaLabel.width(), self.panoramaLabel.height()))

    # 메인 탭 변경 버튼 클릭
    def nextpage(self):
        currentpage = self.QStackedWidget.currentIndex()
        self.QStackedWidget.setCurrentIndex(currentpage+1)
        if currentpage+1 > 2:
            self.QStackedWidget.setCurrentIndex(0)
            # self.nextButton.setEnabled(False)
            # self.previousButton.setEnabled(True)
        # else:
        #     self.previousButton.setEnabled(True)
        #     self.nextButton.setEnabled(True)

    def prevpage(self):
        currentpage = self.QStackedWidget.currentIndex()
        self.QStackedWidget.setCurrentIndex(currentpage-1)
        if currentpage-1 < 0:
            self.QStackedWidget.setCurrentIndex(2)
        #     self.previousButton.setEnabled(False)
        #     self.nextButton.setEnabled(True)
        # else:
        #     self.previousButton.setEnabled(True)
        #     self.nextButton.setEnabled(True)


# class Panorama(QThread):
#     def __init__(self, cctvIpList):
#         super().__init__(cctvIpList)
#         self.temp = cctvIpList
        

#     def run(self):
#         print(self.temp.cctvIpList)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    """
    setup stylesheet
    qt-material
    https://pypi.org/project/qt-material/
    ['dark_amber.xml',
    'dark_blue.xml',
    'dark_cyan.xml',
    'dark_lightgreen.xml',
    'dark_pink.xml',
    'dark_purple.xml',
    'dark_red.xml',
    'dark_teal.xml',
    'dark_yellow.xml',
    'light_amber.xml',
    'light_blue.xml',
    'light_cyan.xml',
    'light_cyan_500.xml',
    'light_lightgreen.xml',
    'light_pink.xml',
    'light_purple.xml',
    'light_red.xml',
    'light_teal.xml',
    'light_yellow.xml']
    """
    apply_stylesheet(app, theme='dark_lightgreen.xml')
    window.show()
    sys.exit(app.exec())