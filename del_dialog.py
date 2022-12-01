from PyQt5.QtWidgets import QDialog, QMessageBox

import ui.ui_deleteCCTVDialog as ui_deleteCCTVDialog
import os

class DeleteCCTVDialog(QDialog, ui_deleteCCTVDialog.Ui_Dialog):  # CCTV 삭제 다이얼로그
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
            msgBox.setStyleSheet(
                'QMessageBox {background-color:#2E3436 }' '\nQPushButton {background-color:#2E3436; color:#FFFFFF}')
            msgBox.addButton(
                "<P><FONT COLOR='#FFFFFF'>OK</FONT></P>", QMessageBox.YesRole)
            close = QMessageBox.information(
                msgBox, 'Message', "<P><FONT COLOR='#FFFFFF'>저장된 CCTV 채널 정보가 없습니다.</FONT></P>", QMessageBox.Ok)
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
