import os

from PyQt5.QtWidgets import QDialog

import ui.ui_setCCTVDialog as ui_setCCTVDialog


class SetCCTVDialog(QDialog, ui_setCCTVDialog.Ui_Dialog):  # CCTV 등록 다이얼로그
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
        self.set_cctv_combo(['CCTV1', 'CCTV2', 'CCTV3', 'CCTV4', 'CCTV5',
                            'CCTV6', 'CCTV7', 'CCTV8', 'CCTV9', 'CCTV10', 'CCTV11', 'CCTV12'])

    # CCTV 채널 ComboBox 세팅
    def set_cctv_combo(self, cctv_list):
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

    def get_name(self, cctv, channel_file):
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
                            listOfFile.append(self.cctvCombo.currentText(
                            ) + "," + self.rtspEdit.text() + "," + self.ipEdit.text())
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
