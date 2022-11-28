from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QMessageBox, QDialog
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from qt_material import apply_stylesheet
import ui.ui_main as ui_main
import ui.ui_setCCTVDialog as ui_setCCTVDialog
import ui.ui_deleteCCTVDialog as ui_deleteCCTVDialog
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

# CCTV 등록 다이얼로그
class SetCCTVDialog(QDialog, ui_setCCTVDialog.Ui_Dialog):
    def __init__(self, channel_file):
        super(SetCCTVDialog, self).__init__()
        self.setupUi(self)
        self.cctv = None
        self.rtsp = None
        self.ip = None
        self.state = None
        self.channel_file = channel_file
        self.saveBtn.clicked.connect(self.save_btn_clicked)
        self.cancelBtn.clicked.connect(self.close)
        self.editBtn.clicked.connect(self.edit_cctv)
        self.set_cctvCombo(['CCTV1', 'CCTV2', 'CCTV3', 'CCTV4', 'CCTV5', 'CCTV6', 'CCTV7', 'CCTV8', 'CCTV9', 'CCTV10', 'CCTV11', 'CCTV12'])

    # CCTV 채널 ComboBox 세팅
    def set_cctvCombo(self, cctv_list):
        if os.path.exists(self.channel_file):
            temp = []
            with open(self.channel_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    sLine = line.split(",")
                    temp.append(sLine[0])
                setItem = [x for x in cctv_list if x not in temp]
                for i in setItem:
                    self.cctvCombo.addItem(i)
        else:
            for i in cctv_list:
                self.cctvCombo.addItem(i)

    def save_btn_clicked(self):
        self.cctv = self.cctvCombo.currentText()
        self.rtsp = self.rtspEdit.text()
        self.ip = self.ipEdit.text()
        if not os.path.exists(self.channel_file):
            file = open(self.channel_file, 'w')
        else:
            file = open(self.channel_file, 'a')

        file.write(self.cctv + ',' + self.rtsp + ',' + self.ip + '\n')
        file.close()
        self.close()

    def getName(self, cctv, channel_file):
        self.cctv = cctv
        self.channel_file = channel_file

    def edit_cctv(self):
        listOfFile = []
        if os.path.exists(self.channel_file):
            with open(self.channel_file, 'rt') as file:
                lines = file.readlines()
                if lines != "":
                    for line in lines:
                        sLine = line.split(',')
                        if sLine[0] != self.cctv:
                            listOfFile.append(line.strip())
                        else:
                            listOfFile.append(self.cctvCombo.currentText() + "," + self.rtspEdit.text() + "," + self.ipEdit.text())
                            self.cctv = self.cctvCombo.currentText()
                            self.rtsp = self.rtspEdit.text()
                            self.ip = self.ipEdit.text()
                            self.state = True
                            
            with open(self.channel_file, 'w') as file:
                for line in listOfFile:
                    if "\n" in line:
                        file.writelines("%s" % line)
                    else:
                        file.writelines("%s\n" % line)
        self.close()

# CCTV 삭제 다이얼로그
class DeleteCCTVDialog(QDialog, ui_deleteCCTVDialog.Ui_Dialog):
    def __init__(self, channel_file):
        super(DeleteCCTVDialog, self).__init__()
        self.setupUi(self)
        self.channel_file = channel_file
        self.num = ""
        self.flag = False
        self.dltBtn.clicked.connect(self.delete_cctv)
        self.clsBtn.clicked.connect(self.close)

    def set_cctv_list(self):
        if os.path.exists(self.channel_file):
            with open(self.channel_file, 'r') as file:
                cctvList = []
                lines = file.readlines()
                for line in lines:
                    sLine = line.split(",")
                    cctvList.append([int(sLine[0][4:]), sLine[0]])
                cctvList.sort()
                for num, item in cctvList:                   
                    self.comboBox.addItem(item)
                    self.flag = True
                    
        if not self.flag:
            msgBox = QMessageBox()
            msgBox.setStyleSheet('QMessageBox {background-color:#2E3436 }' '\nQPushButton {background-color:#2E3436; color:#FFFFFF}')
            msgBox.addButton("<P><FONT COLOR='#FFFFFF'>OK</FONT></P>", QMessageBox.YesRole)
            close = QMessageBox.information(msgBox, 'Message', "<P><FONT COLOR='#FFFFFF'>저장된 CCTV 채널 정보가 없습니다.</FONT></P>", QMessageBox.Ok)
            if close == QMessageBox.Ok:
                return False
        else:
            return True

    def delete_cctv(self):
        with open(self.channel_file, 'r+') as file:
            lines = file.readlines()
            self.num = self.comboBox.currentText()[4:]
            file.truncate(0)
        with open(self.channel_file, 'r+') as file:
            for line in lines:
                sLine = line.split(',')
                if sLine[0] != self.comboBox.currentText():
                    file.write(line)
        self.close()
        
class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        QApplication.processEvents()
        self.threads = []
        self.trigger = True
        self.channel_file = os.path.join(os.path.abspath(''), 'channel.conf')
        self.cctv = ['CCTV1', 'CCTV2', 'CCTV3', 'CCTV4', 'CCTV5', 'CCTV6', 'CCTV7', 'CCTV8', 'CCTV9', 'CCTV10', 'CCTV11', 'CCTV12']

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
        # CCTV 수정
        self.chTreeWidget.itemDoubleClicked.connect(self.edit_cctv)
        
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
        
        # self.clickable(self.viewLabel_1).connect(lambda: self.set_fullscreen(self.rtsp_list[0], self.viewLabel_1, self.streaming_thread['1']))
        self.set_cctv_tree()

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
                    numbers.append([int(sLine[0][4:]), sLine[0], sLine[1], sLine[2]])

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
                    
                    setItem = [x for x in self.cctv if x not in self.cctv_list]
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
            self.streaming_thread[num].setRtsp(set_cctv_dlg.rtsp)
            self.streaming_thread[num].setCctv(num)
            self.streaming_thread[num].setSize(eval('self.viewLabel_'+num).width(), eval('self.viewLabel_'+num).height())
            self.streaming_thread[num].setLabel(eval('self.viewLabel_'+num))
            self.streaming_thread[num].changePixmap.connect(self.set_image)

            self.streaming_thread[num].start()
        self.set_cctv_tree()

    # 등록된 CCTV 수정
    def edit_cctv(self, it):
        set_cctv_dlg = SetCCTVDialog(self.channel_file)
        set_cctv_dlg.cctvCombo.clear()
        set_cctv_dlg.saveBtn.setHidden(True)
        cctv = it.text(0)
        channel_file = self.channel_file
        set_cctv_dlg.getName(cctv, channel_file)
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
            print(cctv)
            if num != cctv:
                self.streaming_thread[cctv].stop()                
                self.streaming_thread[cctv] = StreamingThread()
                # 라벨 초기화 스케줄러
                sched = BackgroundScheduler()
                sched.add_job(self.clear_channel, 'date', run_date=datetime.datetime.now(
                ) + datetime.timedelta(seconds=1), args=[eval('self.viewLabel_'+cctv)])
                sched.start()
                
                self.streaming_thread[num].setRtsp(set_cctv_dlg.rtsp)
                self.streaming_thread[num].setCctv(num)
                self.streaming_thread[num].setSize(eval('self.viewLabel_'+num).width(), eval('self.viewLabel_'+num).height())
                self.streaming_thread[num].setLabel(eval('self.viewLabel_'+num))
                self.streaming_thread[num].changePixmap.connect(self.set_image)
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
            self.streaming_thread[cctv].setRtsp(rtsp)
            self.streaming_thread[cctv].setCctv(cctv)
            self.streaming_thread[cctv].setSize(eval('self.viewLabel_'+cctv).width(), eval('self.viewLabel_'+cctv).height())
            self.streaming_thread[cctv].setLabel(eval('self.viewLabel_'+cctv))
            self.streaming_thread[cctv].changePixmap.connect(self.set_image)
            self.streaming_thread[cctv].start()
    
    # @QtCore.pyqtSlot(str, QPixmap)
    def set_image(self, cctv:str, pixmap:QPixmap):
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
        channel, rtsp, cctv_ip = self.find_rtsp(self.chComboBox)
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
                    QtWidgets.QMessageBox.critical(self, "PTZ Error", "Error PTZ Connecting")
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
            self.threads.append(self.ptz_Thread[str(i)])
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
                QtWidgets.QMessageBox.critical(self, "PTZ Error", "Error PTZ Connecting")
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
        except FileNotFoundError:
            QMessageBox.critical(self, "Stitching Error", "No images")
        except:
            print("Stitching Error")

    # 프로그램 종료 이벤트
    # def closeEvent(self, event):
    #     msgBox = QMessageBox()
    #     msgBox.setStyleSheet('QMessageBox {background-color:#2E3436 }\nQPushButton {background-color:#2E3436; color:#FFFFFF}')
    #     msgBox.addButton("<P><FONT COLOR='#FFFFFF'>Yes</FONT></P>", QMessageBox.YesRole)
    #     msgBox.addButton("<P><FONT COLOR='#FFFFFF'>No</FONT></P>", QMessageBox.NoRole)
    #     close = QMessageBox.question(msgBox, 'Message', "<P><FONT COLOR='#FFFFFF'>Are you sure to quit?</FONT></P>", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if close == QMessageBox.Yes:
    #         self.flag = 1
    #         self.stopStreamingThread()
    #         event.accept()
    #     else:
    #         event.ignore()
            
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
