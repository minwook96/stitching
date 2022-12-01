import datetime
import logging
import os
import sys
from time import sleep

import cv2
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QShortcut,
                             QTreeWidgetItem)
from qt_material import apply_stylesheet

import stitching
import ui.ui_main as ui_main
from del_dialog import DeleteCCTVDialog
from onvif import ONVIFCamera
from set_cctv_dialog import SetCCTVDialog
from streaming_player import StreamingThread

logger = logging.getLogger()  # 로그 생성
logger.setLevel(logging.INFO)  # 로그의 출력 기준 설정
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')  # log 출력 형식
stream_handler = logging.StreamHandler()  # log 출력
stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        QApplication.processEvents()
        self.threads = []
        self.trigger = True
        self.channel_file = os.path.join(os.path.abspath(''), 'channel.conf')
        self.cctv = ['CCTV1', 'CCTV2', 'CCTV3', 'CCTV4', 'CCTV5', 'CCTV6',
                     'CCTV7', 'CCTV8', 'CCTV9', 'CCTV10', 'CCTV11', 'CCTV12']

        # 로고
        self.ci.setPixmap(QPixmap(os.path.join(
            os.path.abspath('ui'), 'skysys.png')))
        self.setWindowIcon(
            QIcon(os.path.join(os.path.abspath('ui'), 'skysysIcon.png')))

        # 버튼 기능 구현
        self.panoramaButton.clicked.connect(self.panorama_start)
        self.addCCTVBtn.clicked.connect(self.add_cctv)
        self.rmvCCTVBtn.clicked.connect(self.delete_cctv)
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
        self.chComboBox.activated.connect(self.ptz_setting)
        self.chTreeWidget.itemDoubleClicked.connect(self.edit_cctv)  # CCTV 수정

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

        self.showMaximized()  # 실행 시 최대화면

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
        self.streaming_thread['11'] = StreamingThread()
        self.streaming_thread['12'] = StreamingThread()

        self.ptz_Thread = {}
        self.ptz_Thread['1'] = None
        self.ptz_Thread['2'] = None
        self.ptz_Thread['3'] = None
        self.ptz_Thread['4'] = None
        self.ptz_Thread['5'] = None
        self.ptz_Thread['6'] = None
        self.ptz_Thread['7'] = None
        self.ptz_Thread['8'] = None
        self.ptz_Thread['9'] = None
        self.ptz_Thread['10'] = None
        self.ptz_Thread['11'] = None
        self.ptz_Thread['12'] = None

        self.set_cctv_tree()
        
        self.setFullscreen = QShortcut(QKeySequence('F11'), self)
        self.setFullscreen.activated.connect(self.toggleFullScreen)

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # CCTV Tree UI에 트리구조로 표시
    def set_cctv_tree(self):
        self.chTreeWidget.clear()
        self.cctv_list = []
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
                    numbers.append(
                        [int(sLine[0][4:]), sLine[0], sLine[1], sLine[2]])

                numbers.sort()
                for num, cctv, rtsp, ip in numbers:
                    item = QTreeWidgetItem(self.chTreeWidget)
                    self.chComboBox.addItem(cctv)
                    self.chComboBox_2.addItem(cctv)
                    item.setText(0, cctv)
                    item.setText(1, rtsp)
                    self.cctv_list.append(cctv)
                    self.ip_list.append(ip[:-1])
                    self.rtsp_list.append(rtsp)
                    self.chTreeWidget.addTopLevelItem(item)

                    # setItem = [x for x in self.cctv if x not in self.cctv_list]
                    # print(setItem)

                    if self.trigger:
                        self.start_cctv(int(num), rtsp)
            self.ptzButton.pressed.connect(self.ptz_start)
        self.trigger = False

    # CCTV 등록 다이얼로그 실행
    def add_cctv(self):
        item = QTreeWidgetItem(self.chTreeWidget)
        set_cctv_dlg = SetCCTVDialog(self.channel_file)
        set_cctv_dlg.editBtn.setHidden(True)
        set_cctv_dlg.exec_()
        item.setText(0, set_cctv_dlg.cctv)
        item.setText(1, set_cctv_dlg.rtsp)
        self.chComboBox.addItem(set_cctv_dlg.cctv)
        self.chComboBox_2.addItem(set_cctv_dlg.cctv)
        self.chTreeWidget.addTopLevelItem(item)
        if set_cctv_dlg.rtsp != None:
            num = set_cctv_dlg.cctv[4:]
            self.streaming_thread[num].set_url(set_cctv_dlg.rtsp)
            self.streaming_thread[num].set_cctv(num)
            self.streaming_thread[num].set_label(eval('self.viewLabel_'+num), eval(
                'self.viewLabel_'+num).width(), eval('self.viewLabel_'+num).height())
            self.streaming_thread[num].change_pixmap.connect(self.set_image)
            self.streaming_thread[num].start()
        self.set_cctv_tree()

    # 등록된 CCTV 수정
    def edit_cctv(self, it):
        set_cctv_dlg = SetCCTVDialog(self.channel_file)
        set_cctv_dlg.cctvCombo.clear()
        set_cctv_dlg.saveBtn.setHidden(True)
        cctv = it.text(0)
        channel_file = self.channel_file
        set_cctv_dlg.get_name(cctv, channel_file)
        temp = []  # 저장된 cctv list 임시 저장
        if os.path.exists(self.channel_file):
            with open(self.channel_file, 'r') as file:
                lines = file.readlines()
                set_cctv_dlg.rtspEdit.clear()
                set_cctv_dlg.ipEdit.clear()
                if lines != "":
                    for line in lines:
                        sLine = line.split(',')
                        temp.append(sLine[0])
                        if sLine[0] == cctv:
                            cctv = sLine[0]
                            set_cctv_dlg.cctvCombo.addItem(cctv)
                            set_cctv_dlg.rtspEdit.setText(sLine[1])
                            set_cctv_dlg.ipEdit.setText(sLine[2])

                setItem = [x for x in self.cctv if x not in temp]
                # setItem.append(cctv)
                # setItem.sort()
                for i in setItem:
                    set_cctv_dlg.cctvCombo.addItem(i)
                set_cctv_dlg.cctvCombo.setCurrentText(cctv)
        set_cctv_dlg.exec_()

        if set_cctv_dlg.state:
            num = str(set_cctv_dlg.cctv[4:])
            cctv = cctv[4:]
            if num != cctv:
                self.streaming_thread[cctv].stop()
                self.streaming_thread[cctv] = StreamingThread()
                # 라벨 초기화 스케줄러
                sched = BackgroundScheduler()
                sched.add_job(self.clear_channel, 'date', run_date=datetime.datetime.now(
                ) + datetime.timedelta(seconds=1), args=[eval('self.viewLabel_'+cctv)])
                sched.start()

                self.streaming_thread[num].set_url(set_cctv_dlg.rtsp)
                self.streaming_thread[num].set_cctv(num)
                self.streaming_thread[num].set_label(eval('self.viewLabel_'+num), eval(
                    'self.viewLabel_'+num).width(), eval('self.viewLabel_'+num).height())
                self.streaming_thread[num].change_pixmap.connect(
                    self.set_image)
                self.streaming_thread[num].start()
        self.set_cctv_tree()

    # cctv 삭제
    def delete_cctv(self):
        delete_cctv_dlg = DeleteCCTVDialog(self.channel_file)
        if delete_cctv_dlg.set_cctv_list():
            delete_cctv_dlg.exec_()
            if delete_cctv_dlg.num != '':
                num = str(delete_cctv_dlg.num)
                self.streaming_thread[num].stop()
                self.streaming_thread[num] = StreamingThread()
                # 라벨 초기화 스케줄러
                sched = BackgroundScheduler()
                sched.add_job(self.clear_channel, 'date', run_date=datetime.datetime.now(
                ) + datetime.timedelta(seconds=1), args=[eval('self.viewLabel_'+num)])
                sched.start()
        self.set_cctv_tree()

    # 메인Gui화면에 영상 부착 (스레드 실행)
    def start_cctv(self, cctv, rtsp):
        if rtsp != '' and cctv != '':
            cctv = str(cctv)
            # self.streaming_thread[cctv].stop()
            # self.streaming_thread[cctv].wait(1)
            self.streaming_thread[cctv] = StreamingThread()
            self.streaming_thread[cctv].set_url(rtsp)
            self.streaming_thread[cctv].set_cctv(cctv)
            self.streaming_thread[cctv].set_label(eval('self.viewLabel_'+cctv), eval(
                'self.viewLabel_'+cctv).width(), eval('self.viewLabel_'+cctv).height())
            self.streaming_thread[cctv].change_pixmap.connect(self.set_image)
            self.streaming_thread[cctv].start()

    # @QtCore.pyqtSlot(str, QPixmap)
    def set_image(self, cctv: str, pixmap: QPixmap):
        eval('self.viewLabel_'+cctv).setPixmap(pixmap)

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
                        cctv = sLine[0]
                        rtsp = sLine[1].strip()
                        cctv_ip = sLine[2].strip()
                        break
                    else:
                        cctv = "No Channel"

        return cctv, rtsp, cctv_ip

    # PTZ 카메라 기본 변수 선언
    def ptz_setting(self):
        channel, _, cctv_ip = self.find_rtsp(self.chComboBox)
        if channel != "No Channel":
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
                if channel != "No Channel":
                    QMessageBox.critical(
                        self, "PTZ Error", "Error PTZ Connecting")
                return False

    # PTZ 작동
    def ptz_control(self, command):
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
            self.ptz_Thread[str(i)] = self.PTZThread(
                self, self.ip_list[i], self.rtsp_list[i], i)
            # self.threads.append(self.ptz_Thread[str(i)])
            # self.ptz_Thread[str(i)].setDaemon(True)
            self.ptz_Thread[str(i)].start()

    def tour_setting(self, ip):
        if ip != "":
            try:
                cam = ONVIFCamera(ip, 80, "admin", "tmzkdl123$")
                media = cam.create_media_service()
                self.ptz = cam.create_ptz_service()
                self.media_profile = media.GetProfiles()[0]
                self.status = self.ptz.GetStatus({
                    'ProfileToken': self.media_profile.token,
                })
                return True
            except:
                QMessageBox.critical(self, "PTZ Error", "Error PTZ Connecting")
                return False

    def tour_start(self, ip, rtsp, num):
        if self.tour_setting(ip) is True:
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
                    success, frame = cap.read()
                    # 입력 영상 크기 및 출력 영상 크기
                    h, w = frame.shape[:2]

                    # 모서리 점들의 좌표, 드래그 상태 여부
                    # 나중에 미포에서 이 좌표를 변경해야함
                    srcQuad = np.array(
                        [[30, 30], [30, h-30], [w-30, h-30], [w-30, 30]], np.float32)
                    dstQuad = np.array(
                        [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]], np.float32)
                    image_folder = "imgs/{}/".format(
                        datetime.datetime.today().strftime("%Y-%m-%d"))
                    image_name = f"panorama{num+1}_{i}.jpg"
                    self.create_folder(image_folder)
                    
                    sleep(3)

                    # 투시 변환
                    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
                    frame = cv2.warpPerspective(
                        frame, pers, (w, h), flags=cv2.INTER_CUBIC)
                    cv2.imwrite(image_folder + image_name, frame)  # 이미지 캡처

                    sleep(3)

                    self.ptz.GotoHomePosition(
                        {'ProfileToken': self.media_profile.token})
            except:
                logger.error("PTZ Preset")
        else:
            logger.error("preset tour fail")

    def create_folder(self, directory_path):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
        except OSError:
            logger.error('Error: Creating directory. ' + directory_path)

    def panorama_start(self):
        try:
            print("panorama click")
            # 가져오고자 하는 폴더 주소
            path = "imgs/{}/".format(datetime.datetime.today().strftime("%Y-%m-%d"))
            file_list = os.listdir(path)

            file_list_jpg = [path + file for file in file_list if file.endswith(
                ".jpg") | file.endswith(".JPG") | file.endswith(".png")]  # 확장자명 입력
            image_folder = "imgs/result/{}/".format(
                datetime.datetime.today().strftime("%Y-%m-%d"))
            self.create_folder(image_folder)
            stitcher = stitching.Stitcher()
            panoramaImage = stitcher.stitch(file_list_jpg)
            cv2.imwrite(image_folder + "result.jpg", panoramaImage)
        except FileNotFoundError:
            QMessageBox.critical(self, "Stitching Error", "No images")
            logger.error("Stitching Error", "No images")
        except:
            logger.error("Stitching Error")

    # 프로그램 종료 이벤트
    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.addButton(
            "<P>Yes</P>", QMessageBox.YesRole)
        msgBox.addButton(
            "<P>No</P>", QMessageBox.NoRole)
        close = QMessageBox.question(
            msgBox, 'Message', "<P>Are you sure to quit?</P>", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


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
    apply_stylesheet(app, theme='dark_blue.xml')
    window.show()
    sys.exit(app.exec())
