# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/skysys/stitching/ui/setCCTVDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(683, 346)
        Dialog.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cctvCombo = QtWidgets.QComboBox(Dialog)
        self.cctvCombo.setStyleSheet("")
        self.cctvCombo.setObjectName("cctvCombo")
        self.gridLayout.addWidget(self.cctvCombo, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ipEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ipEdit.sizePolicy().hasHeightForWidth())
        self.ipEdit.setSizePolicy(sizePolicy)
        self.ipEdit.setStyleSheet("")
        self.ipEdit.setObjectName("ipEdit")
        self.gridLayout.addWidget(self.ipEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setStyleSheet("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setStyleSheet("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.rtspEdit = QtWidgets.QLineEdit(Dialog)
        self.rtspEdit.setStyleSheet("")
        self.rtspEdit.setObjectName("rtspEdit")
        self.verticalLayout_2.addWidget(self.rtspEdit)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.saveBtn = QtWidgets.QPushButton(Dialog)
        self.saveBtn.setStyleSheet("")
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout_5.addWidget(self.saveBtn, 0, 1, 1, 1)
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        self.cancelBtn.setStyleSheet("")
        self.cancelBtn.setObjectName("cancelBtn")
        self.gridLayout_5.addWidget(self.cancelBtn, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 4, 1, 1)
        self.editBtn = QtWidgets.QPushButton(Dialog)
        self.editBtn.setStyleSheet("")
        self.editBtn.setObjectName("editBtn")
        self.gridLayout_5.addWidget(self.editBtn, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "채널 번호"))
        self.label_2.setText(_translate("Dialog", "채널 IP"))
        self.label_3.setText(_translate("Dialog", "CCTV 주소"))
        self.saveBtn.setText(_translate("Dialog", "등록"))
        self.cancelBtn.setText(_translate("Dialog", "취소"))
        self.editBtn.setText(_translate("Dialog", "수정"))