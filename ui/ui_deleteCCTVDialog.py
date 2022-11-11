# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/skysys/stitching/ui/deleteCCTVDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(307, 82)
        Dialog.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setStyleSheet("")
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dltBtn = QtWidgets.QPushButton(Dialog)
        self.dltBtn.setStyleSheet("")
        self.dltBtn.setObjectName("dltBtn")
        self.horizontalLayout.addWidget(self.dltBtn)
        self.clsBtn = QtWidgets.QPushButton(Dialog)
        self.clsBtn.setStyleSheet("")
        self.clsBtn.setObjectName("clsBtn")
        self.horizontalLayout.addWidget(self.clsBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.dltBtn.setText(_translate("Dialog", "삭제"))
        self.clsBtn.setText(_translate("Dialog", "닫기"))
