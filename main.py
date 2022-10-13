from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QLabel, QAction
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, Qt
from PyQt5 import QtCore, QtWidgets
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

# scroll version
# class MainWindow(QMainWindow, ui_scroll_main.Ui_MainWindow):


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.threads = []
        self.scroll = False

        self.channel_file = os.path.join(os.path.abspath(''), 'channel.conf')

        # 첫번째 탭으로 시작
        self.QStackedWidget.setCurrentIndex(0)

        # Scroll version
        if self.scroll:
            self.scaleFactor = 0.0
            self.panoramaLabel = QLabel()
            # self.panoramaLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.panoramaLabel.setScaledContents(True)
            self.scrollArea.setWidget(self.panoramaLabel)
            self.panoramaLabel.setCursor(Qt.OpenHandCursor)
            self.scrollAreaLeft.mouseMoveEvent = self.mouse_move_event_left
            self.scrollAreaLeft.mousePressEvent = self.mouse_press_event_left
            self.scrollAreaLeft.mouseReleaseEvent = self.mouse_release_event_left
            self.create_actions()

        # 버튼 기능 구현
        self.nextButton.clicked.connect(self.next_page)
        self.previousButton.clicked.connect(self.prev_page)
        self.panoramaButton.clicked.connect(self.panorama_start)
        self.upButton.pressed.connect(lambda: self.ptz_control('up'))
        self.downButton.pressed.connect(lambda: self.ptz_control('down'))
        self.leftButton.pressed.connect(lambda: self.ptz_control('left'))
        self.rightButton.pressed.connect(lambda: self.ptz_control('right'))
        self.zoomOutButton.pressed.connect(
            lambda: self.ptz_control('zoom_out'))
        self.zoomInButton.pressed.connect(lambda: self.ptz_control('zoom_in'))
        self.homeButton.clicked.connect(lambda: self.ptz_control('home'))
        self.upButton.released.connect(lambda: self.ptz_control('stop'))
        self.downButton.released.connect(lambda: self.ptz_control('stop'))
        self.leftButton.released.connect(lambda: self.ptz_control('stop'))
        self.rightButton.released.connect(lambda: self.ptz_control('stop'))
        self.zoomOutButton.released.connect(lambda: self.ptz_control('stop'))
        self.zoomInButton.released.connect(lambda: self.ptz_control('stop'))
        self.chComboBox.activated.connect(self.set_CCTV)

        # PTZ Control Button
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
        
        # 실행 시 최대화면
        self.showMaximized()

        self.streaming_thread = {}
        self.streaming_thread['1'] = StreamingThread()
        self.streaming_thread['2'] = StreamingThread()
        self.streaming_thread['3'] = StreamingThread()
        self.streaming_thread['4'] = StreamingThread()
        self.streaming_thread['5'] = StreamingThread()
        self.streaming_thread['6'] = StreamingThread()
        self.streaming_thread['7'] = StreamingThread()
        self.streaming_thread['8'] = StreamingThread()
        self.streaming_thread['9'] = StreamingThread()
        self.streaming_thread['10'] = StreamingThread()
        self.set_CCTV_tree()

    # CCTV Tree UI에 트리구조로 표시
    def set_CCTV_tree(self):
        self.chTreeWidget.clear()
        self.ip_list = []
        self.rtsp_list = []
        if os.path.exists(self.channel_file):
            with open(self.channel_file, 'r') as file:
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

                # numbers.sort()
                i = 1
                for cctv, rtsp, ip in numbers:
                    item = QTreeWidgetItem(self.chTreeWidget)
                    self.chComboBox.addItem(cctv)
                    self.chComboBox_2.addItem(cctv)
                    item.setText(0, cctv)
                    item.setText(1, rtsp)
                    self.ip_list.append(ip[:-1])
                    self.rtsp_list.append(rtsp)
                    self.chTreeWidget.addTopLevelItem(item)
                    self.set_CCTV(cctv, rtsp, ip, i)
                    i = i + 1
            self.ptzButton.pressed.connect(self.ptz_start)

    # QThread 클래스 선언하기, QThread 클래스를 쓰려면 QtCore 모듈을 import 해야함.
    # Gui에서 응답없음 방지하기 위해 QThread 사용
    class PTZThread(QThread):
        # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        def __init__(self, parent, cctv_ip, rtsp, num):
            super().__init__(parent)
            self.parent = parent  # self.parent를 사용하여 WindowClass 위젯을 제어할 수 있다.
            self.cctv_ip = cctv_ip
            self.rtsp = rtsp
            self.num = num

        def run(self):
            self.parent.tour_start(self.cctv_ip, self.rtsp, self.num)

    # PTZ Thread 실행, cctv ptz 여러대 동시 실행
    def ptz_start(self):
        print(self.ip_list)
        for i in range(0, len(self.ip_list)):
            self.ptz_Thread = self.PTZThread(
                self, self.ip_list[i], self.rtsp_list[i], i)
            self.threads.append(self.ptz_Thread)
            self.ptz_Thread.start()

    # 메인Gui화면에 영상 부착 (스레드 실행)
    def set_CCTV(self, channel, rtsp, cctv_ip, num):
        # Index 0: No Channel
        # if self.chComboBox.currentIndex() == 0:
        #     self.streaming_thread.stop()
        #     self.streaming_thread = StreamingThread()
        #     # 라벨 초기화 스케줄러
        #     sched = BackgroundScheduler()
        #     sched.add_job(self.clear_channel, 'date', run_date=datetime.datetime.now(
        #     ) + datetime.timedelta(seconds=1), args=[self.viewLabel])
        #     sched.start()
        # else:
        #     channel, rtsp, cctv_ip = self.find_rtsp(self.chComboBox)
        #     if rtsp != '' and channel != '':
        #         self.streaming_thread.stop()
        #         self.streaming_thread.wait(1)
        #         self.streaming_thread = StreamingThread()
        #         self.streaming_thread.setRtsp(rtsp)
        #         self.streaming_thread.setSize(
        #             self.viewLabel.width(), self.viewLabel.height())
        #         self.streaming_thread.setLabel(self.viewLabel)
        #         self.streaming_thread.start()
        #         self.ptz_setting(cctv_ip)
        #         logger.info("Channel Streaming Success")
     
        print(num)
        num = str(num)
        self.streaming_thread[num].stop()
        self.streaming_thread[num].wait(1)
        self.streaming_thread[num] = StreamingThread()
        self.streaming_thread[num].setRtsp(rtsp)
        self.streaming_thread[num].setSize(eval('self.viewLabel_'+num).width(), eval('self.viewLabel_'+num).height())
        self.streaming_thread[num].setSize(self.viewLabel_1.width(), self.viewLabel_1.height())
        self.streaming_thread[num].setLabel(eval('self.viewLabel_'+num))
        self.streaming_thread[num].start()
        self.ptz_setting(cctv_ip)
        logger.info("Channel Streaming Success")

    # NoChannel => 라벨 초기화
    def clear_channel(self, cctv):
        cctv.clear()
        cctv.setText('No Channel')

    # ComboBox에서 CCTV 선택했을 때 rtsp 주소 검색
    def find_rtsp(self, qComboBox):
        rtsp = ''
        cctv_ip = ''
        if os.path.exists(self.channel_file):
            with open(self.channel_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    sLine = line.split(',')
                    if sLine[0] == qComboBox.currentText():
                        rtsp = sLine[1].strip()
                        cctv_ip = sLine[2].strip()
                        break
        cctv = sLine[0]
        return cctv, rtsp, cctv_ip

    # PTZ 카메라 기본 변수 선언
    def ptz_setting(self, cctv_ip):
        if cctv_ip != "":
            try:
                cam = ONVIFCamera(cctv_ip, 80, "admin", "tmzkdl123$")
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
    def ptz_control(self, command):
        # 시작 시 ptz 에러 수정완료
        # if self.ptz_setting(self.chComboBox.currentText()) is True:
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
            if command == "zoom_in":
                self.ptz.ContinuousMove({
                    'ProfileToken': self.media_profile.token,
                    'Velocity': {
                        'Zoom': {
                            'x': 1
                        }
                    }
                })
            if command == "zoom_out":
                self.ptz.ContinuousMove({
                    'ProfileToken': self.media_profile.token,
                    'Velocity': {
                        'Zoom': {
                            'x': -1
                        }
                    }
                })

    def tour_start(self, ip, rtsp, num):
        # label에 표시하는 방법 다시 고안해야함
        ip = ip
        if self.ptz_setting(ip) is True:
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
                    image_folder = "imgs/{}/".format(
                        datetime.datetime.today().strftime("%Y-%m-%d"))
                    image_name = f"panorama{num+1}_{i}.jpg"
                    self.create_folder(image_folder)
                    sleep(3)

                    cv2.imwrite(image_folder + image_name, frame)

                    sleep(3)

                    self.ptz.GotoHomePosition(
                        {'ProfileToken': self.media_profile.token})
                    eval('self.label_'+str(num+1)).setText("running")
            except:
                logger.error("PTZ Preset")
                
            eval('self.label_'+str(num+1)).setText("Success")

        else:
            eval('self.label_'+str(num+1)).setText("Fail")
            logger.error("preset tour fail")

    def create_folder(self, directory_path):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
        except OSError:
            logger.error('Error: Creating directory. ' + directory_path)

    # --------------------------ScrollArea--------------------------------------------
    def adjust_scroll_bar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def normal_size(self):
        print("nomal")
        self.panoramaLabel.adjustSize()
        self.scaleFactor = 1.0

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def fit_to_window(self):
        fit_to_window = self.fit_to_windowAct.isChecked()
        self.scrollArea.setWidgetResizable(fit_to_window)
        if not fit_to_window:
            self.normal_size()
        self.update_actions()

    def scale_image(self, factor):
        self.scaleFactor *= factor
        self.panoramaLabel.resize(
            self.scaleFactor * self.panoramaLabel.pixmap().size())

        self.adjust_scroll_bar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scrollArea.verticalScrollBar(), factor)

        self.zoom_inAct.setEnabled(self.scaleFactor < 3.0)
        self.zoom_outAct.setEnabled(self.scaleFactor > 0.333)

    # 현재 작동안함 이유 모름
    def create_actions(self):
        self.normal_sizeAct = QAction(
            "&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normal_size)
        self.zoom_inAct = QAction(
            "Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoom_in)
        self.zoom_outAct = QAction(
            "Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoom_out)
        self.fit_to_windowAct = QAction("&Fit to Window", self, enabled=False,
                                        checkable=True, shortcut="Ctrl+F", triggered=self.fit_to_window)

    def update_actions(self):
        self.normal_sizeAct.setEnabled(not self.fit_to_windowAct.isChecked())
        self.zoom_inAct.setEnabled(not self.fit_to_windowAct.isChecked())
        self.zoom_outAct.setEnabled(not self.fit_to_windowAct.isChecked())

    def mouse_press_event_left(self, event):
        self.pressed = True
        self.panoramaLabel.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value() + \
            event.pos().x()
        self.initialPosY = self.scrollArea.verticalScrollBar().value() + \
            event.pos().y()

    def mouse_release_event_left(self, event):
        self.pressed = False
        self.panoramaLabel.setCursor(Qt.OpenHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value()
        self.initialPosY = self.scrollArea.verticalScrollBar().value()

    def mouse_move_event_left(self, event):
        if self.pressed:
            self.scrollArea.horizontalScrollBar().setValue(
                self.initialPosX - event.pos().x())
            self.scrollArea.verticalScrollBar().setValue(self.initialPosY - event.pos().y())
    # --------------------------ScrollArea--------------------------------------------

    def panorama_start(self):
        print("panorama click")
        # 가져오고자 하는 폴더 주소
        path = "imgs/{}/".format(datetime.datetime.today().strftime("%Y-%m-%d"))
        # path="imgs/"
        file_list = os.listdir(path)
        # 확장자명 입력
        file_list_jpg = [
            path + file for file in file_list if file.endswith(".jpg")]
        print(file_list_jpg)
        image_folder = "imgs/result/{}/".format(
            datetime.datetime.today().strftime("%Y-%m-%d"))
        self.create_folder(image_folder)
        stitcher = stitching.Stitcher()
        panoramaImage = stitcher.stitch(file_list_jpg)
        cv2.imwrite(image_folder + "result.jpg", panoramaImage)
        sleep(2)

        self.panoramaLabel.setPixmap(QPixmap(image_folder + "result.jpg").scaled(
            self.panoramaLabel.width(), self.panoramaLabel.height()))
                

        if self.scroll:
            self.scaleFactor = 1.0

            self.fit_to_windowAct.setEnabled(True)
            self.update_actions()

            if not self.fit_to_windowAct.isChecked():
                self.panoramaLabel.adjustSize()

    # 메인 탭 변경 버튼 클릭
    def next_page(self):
        currentpage = self.QStackedWidget.currentIndex()
        self.QStackedWidget.setCurrentIndex(currentpage+1)
        if currentpage+1 > 2:
            self.QStackedWidget.setCurrentIndex(0)

    def prev_page(self):
        currentpage = self.QStackedWidget.currentIndex()
        self.QStackedWidget.setCurrentIndex(currentpage-1)
        if currentpage-1 < 0:
            self.QStackedWidget.setCurrentIndex(2)


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
    'light_blue.xml', --> secondaryLightColor #000000 변경해야함
    'light_cyan.xml',
    'light_cyan_500.xml',
    'light_lightgreen.xml',
    'light_pink.xml',
    'light_purple.xml',
    'light_red.xml',
    'light_teal.xml',
    'light_yellow.xml']
    """
    apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    sys.exit(app.exec())
