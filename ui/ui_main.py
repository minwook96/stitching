# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/skysys/stitching/ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(1267, 755)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/skysys/stitching/ui/skysysIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.topLayout = QtWidgets.QWidget(self.centralwidget)
        self.topLayout.setObjectName("topLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.topLayout)
        self.horizontalLayout_8.setContentsMargins(5, 5, 5, 1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.ci = QtWidgets.QLabel(self.topLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ci.sizePolicy().hasHeightForWidth())
        self.ci.setSizePolicy(sizePolicy)
        self.ci.setMaximumSize(QtCore.QSize(250, 40))
        self.ci.setText("")
        self.ci.setPixmap(QtGui.QPixmap("/home/skysys/stitching/ui/skysys.png"))
        self.ci.setScaledContents(True)
        self.ci.setObjectName("ci")
        self.horizontalLayout_8.addWidget(self.ci)
        spacerItem = QtWidgets.QSpacerItem(40, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.previousButton = QtWidgets.QPushButton(self.topLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previousButton.sizePolicy().hasHeightForWidth())
        self.previousButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.previousButton.setFont(font)
        self.previousButton.setCheckable(False)
        self.previousButton.setChecked(False)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout_8.addWidget(self.previousButton)
        self.nextButton = QtWidgets.QPushButton(self.topLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout_8.addWidget(self.nextButton)
        self.verticalLayout_5.addWidget(self.topLayout)
        self.QStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.QStackedWidget.setObjectName("QStackedWidget")
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.page1Layout = QtWidgets.QHBoxLayout(self.page1)
        self.page1Layout.setContentsMargins(5, 5, 5, 5)
        self.page1Layout.setSpacing(5)
        self.page1Layout.setObjectName("page1Layout")
        self.pageWidget1 = QtWidgets.QWidget(self.page1)
        self.pageWidget1.setObjectName("pageWidget1")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.pageWidget1)
        self.horizontalLayout_12.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.liveLabel = QtWidgets.QLabel(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.liveLabel.sizePolicy().hasHeightForWidth())
        self.liveLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.liveLabel.setFont(font)
        self.liveLabel.setObjectName("liveLabel")
        self.verticalLayout_4.addWidget(self.liveLabel)
        self.chListLabel = QtWidgets.QLabel(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chListLabel.sizePolicy().hasHeightForWidth())
        self.chListLabel.setSizePolicy(sizePolicy)
        self.chListLabel.setObjectName("chListLabel")
        self.verticalLayout_4.addWidget(self.chListLabel)
        self.chTreeWidget = QtWidgets.QTreeWidget(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chTreeWidget.sizePolicy().hasHeightForWidth())
        self.chTreeWidget.setSizePolicy(sizePolicy)
        self.chTreeWidget.setObjectName("chTreeWidget")
        self.verticalLayout_4.addWidget(self.chTreeWidget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem1)
        self.streamingLabel = QtWidgets.QLabel(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.streamingLabel.sizePolicy().hasHeightForWidth())
        self.streamingLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.streamingLabel.setFont(font)
        self.streamingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.streamingLabel.setObjectName("streamingLabel")
        self.verticalLayout_4.addWidget(self.streamingLabel)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.chComboBox = QtWidgets.QComboBox(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chComboBox.sizePolicy().hasHeightForWidth())
        self.chComboBox.setSizePolicy(sizePolicy)
        self.chComboBox.setObjectName("chComboBox")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.chComboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.chComboBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.ptzControlLabel = QtWidgets.QLabel(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ptzControlLabel.sizePolicy().hasHeightForWidth())
        self.ptzControlLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ptzControlLabel.setFont(font)
        self.ptzControlLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ptzControlLabel.setObjectName("ptzControlLabel")
        self.verticalLayout_4.addWidget(self.ptzControlLabel)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.leftButton = QtWidgets.QPushButton(self.pageWidget1)
        self.leftButton.setObjectName("leftButton")
        self.horizontalLayout_5.addWidget(self.leftButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.upButton = QtWidgets.QPushButton(self.pageWidget1)
        self.upButton.setObjectName("upButton")
        self.verticalLayout.addWidget(self.upButton)
        self.homeButton = QtWidgets.QPushButton(self.pageWidget1)
        self.homeButton.setObjectName("homeButton")
        self.verticalLayout.addWidget(self.homeButton)
        self.downButton = QtWidgets.QPushButton(self.pageWidget1)
        self.downButton.setObjectName("downButton")
        self.verticalLayout.addWidget(self.downButton)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.rightButton = QtWidgets.QPushButton(self.pageWidget1)
        self.rightButton.setObjectName("rightButton")
        self.horizontalLayout_5.addWidget(self.rightButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.zoomOutButton = QtWidgets.QPushButton(self.pageWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.zoomOutButton.setFont(font)
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.horizontalLayout_7.addWidget(self.zoomOutButton)
        self.zoomLabel = QtWidgets.QLabel(self.pageWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomLabel.sizePolicy().hasHeightForWidth())
        self.zoomLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.zoomLabel.setFont(font)
        self.zoomLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.zoomLabel.setObjectName("zoomLabel")
        self.horizontalLayout_7.addWidget(self.zoomLabel)
        self.zoomInButton = QtWidgets.QPushButton(self.pageWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.zoomInButton.setFont(font)
        self.zoomInButton.setObjectName("zoomInButton")
        self.horizontalLayout_7.addWidget(self.zoomInButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_12.addLayout(self.verticalLayout_4)
        self.viewLabel = QtWidgets.QLabel(self.pageWidget1)
        self.viewLabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewLabel.sizePolicy().hasHeightForWidth())
        self.viewLabel.setSizePolicy(sizePolicy)
        self.viewLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.viewLabel.setFont(font)
        self.viewLabel.setStyleSheet("background-color: rgb(91, 91, 91);color: rgb(255, 255, 255);")
        self.viewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.viewLabel.setObjectName("viewLabel")
        self.horizontalLayout_12.addWidget(self.viewLabel)
        self.page1Layout.addWidget(self.pageWidget1)
        self.QStackedWidget.addWidget(self.page1)
        self.page2 = QtWidgets.QWidget()
        self.page2.setObjectName("page2")
        self.page2Layout = QtWidgets.QHBoxLayout(self.page2)
        self.page2Layout.setContentsMargins(5, 5, 5, 5)
        self.page2Layout.setSpacing(5)
        self.page2Layout.setObjectName("page2Layout")
        self.pageWidget2 = QtWidgets.QWidget(self.page2)
        self.pageWidget2.setObjectName("pageWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.pageWidget2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalWidget = QtWidgets.QWidget(self.pageWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ptzButton = QtWidgets.QPushButton(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ptzButton.sizePolicy().hasHeightForWidth())
        self.ptzButton.setSizePolicy(sizePolicy)
        self.ptzButton.setObjectName("ptzButton")
        self.verticalLayout_2.addWidget(self.ptzButton)
        self.chComboBox_2 = QtWidgets.QComboBox(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chComboBox_2.sizePolicy().hasHeightForWidth())
        self.chComboBox_2.setSizePolicy(sizePolicy)
        self.chComboBox_2.setObjectName("chComboBox_2")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.chComboBox_2.addItem("")
        self.verticalLayout_2.addWidget(self.chComboBox_2)
        self.restartButton = QtWidgets.QPushButton(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restartButton.sizePolicy().hasHeightForWidth())
        self.restartButton.setSizePolicy(sizePolicy)
        self.restartButton.setObjectName("restartButton")
        self.verticalLayout_2.addWidget(self.restartButton)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_3.addWidget(self.verticalWidget)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_1 = QtWidgets.QLabel(self.pageWidget2)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.gridLayout_5.addWidget(self.label_1, 0, 1, 1, 1)
        self.cctvLabel_1 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_1.setFont(font)
        self.cctvLabel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_1.setObjectName("cctvLabel_1")
        self.gridLayout_5.addWidget(self.cctvLabel_1, 0, 0, 1, 1)
        self.cctvLabel_9 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_9.setFont(font)
        self.cctvLabel_9.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_9.setObjectName("cctvLabel_9")
        self.gridLayout_5.addWidget(self.cctvLabel_9, 3, 2, 1, 1)
        self.cctvLabel_4 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_4.setFont(font)
        self.cctvLabel_4.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_4.setObjectName("cctvLabel_4")
        self.gridLayout_5.addWidget(self.cctvLabel_4, 3, 0, 1, 1)
        self.cctvLabel_7 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_7.setFont(font)
        self.cctvLabel_7.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_7.setObjectName("cctvLabel_7")
        self.gridLayout_5.addWidget(self.cctvLabel_7, 1, 2, 1, 1)
        self.cctvLabel_2 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_2.setFont(font)
        self.cctvLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_2.setObjectName("cctvLabel_2")
        self.gridLayout_5.addWidget(self.cctvLabel_2, 1, 0, 1, 1)
        self.cctvLabel_8 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_8.setFont(font)
        self.cctvLabel_8.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_8.setObjectName("cctvLabel_8")
        self.gridLayout_5.addWidget(self.cctvLabel_8, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.pageWidget2)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 4, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.pageWidget2)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 3, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.pageWidget2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.pageWidget2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.pageWidget2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 3, 1, 1, 1)
        self.cctvLabel_3 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_3.setFont(font)
        self.cctvLabel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_3.setObjectName("cctvLabel_3")
        self.gridLayout_5.addWidget(self.cctvLabel_3, 2, 0, 1, 1)
        self.cctvLabel_10 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_10.setFont(font)
        self.cctvLabel_10.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_10.setObjectName("cctvLabel_10")
        self.gridLayout_5.addWidget(self.cctvLabel_10, 4, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.pageWidget2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.pageWidget2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 2, 3, 1, 1)
        self.cctvLabel_5 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_5.setFont(font)
        self.cctvLabel_5.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_5.setObjectName("cctvLabel_5")
        self.gridLayout_5.addWidget(self.cctvLabel_5, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.pageWidget2)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 0, 3, 1, 1)
        self.cctvLabel_6 = QtWidgets.QLabel(self.pageWidget2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cctvLabel_6.setFont(font)
        self.cctvLabel_6.setAlignment(QtCore.Qt.AlignCenter)
        self.cctvLabel_6.setObjectName("cctvLabel_6")
        self.gridLayout_5.addWidget(self.cctvLabel_6, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.pageWidget2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 4, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_5)
        self.page2Layout.addWidget(self.pageWidget2)
        self.QStackedWidget.addWidget(self.page2)
        self.page3 = QtWidgets.QWidget()
        self.page3.setObjectName("page3")
        self.page3Layout = QtWidgets.QGridLayout(self.page3)
        self.page3Layout.setContentsMargins(5, 5, 5, 5)
        self.page3Layout.setObjectName("page3Layout")
        self.pageWidget3 = QtWidgets.QWidget(self.page3)
        self.pageWidget3.setObjectName("pageWidget3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.pageWidget3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.panoramaButton = QtWidgets.QPushButton(self.pageWidget3)
        self.panoramaButton.setObjectName("panoramaButton")
        self.verticalLayout_3.addWidget(self.panoramaButton)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.panoramaLabel = QtWidgets.QLabel(self.pageWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panoramaLabel.sizePolicy().hasHeightForWidth())
        self.panoramaLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.panoramaLabel.setFont(font)
        self.panoramaLabel.setStyleSheet("background-color: rgb(91, 91, 91);\n"
"color: rgb(255, 255, 255);")
        self.panoramaLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.panoramaLabel.setObjectName("panoramaLabel")
        self.horizontalLayout_2.addWidget(self.panoramaLabel)
        self.page3Layout.addWidget(self.pageWidget3, 0, 0, 1, 1)
        self.QStackedWidget.addWidget(self.page3)
        self.verticalLayout_5.addWidget(self.QStackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.QStackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "panorama"))
        self.previousButton.setText(_translate("MainWindow", "Previous Page"))
        self.nextButton.setText(_translate("MainWindow", "Next Page"))
        self.liveLabel.setText(_translate("MainWindow", "라이브"))
        self.chListLabel.setText(_translate("MainWindow", "채널 리스트"))
        self.chTreeWidget.headerItem().setText(0, _translate("MainWindow", "CCTV"))
        self.chTreeWidget.headerItem().setText(1, _translate("MainWindow", "URL"))
        self.streamingLabel.setText(_translate("MainWindow", "Streaming"))
        self.chComboBox.setItemText(0, _translate("MainWindow", "No Channel"))
        self.chComboBox.setItemText(1, _translate("MainWindow", "CCTV1"))
        self.chComboBox.setItemText(2, _translate("MainWindow", "CCTV2"))
        self.chComboBox.setItemText(3, _translate("MainWindow", "CCTV3"))
        self.chComboBox.setItemText(4, _translate("MainWindow", "CCTV4"))
        self.chComboBox.setItemText(5, _translate("MainWindow", "CCTV5"))
        self.chComboBox.setItemText(6, _translate("MainWindow", "CCTV6"))
        self.chComboBox.setItemText(7, _translate("MainWindow", "CCTV7"))
        self.chComboBox.setItemText(8, _translate("MainWindow", "CCTV8"))
        self.chComboBox.setItemText(9, _translate("MainWindow", "CCTV9"))
        self.chComboBox.setItemText(10, _translate("MainWindow", "CCTV10"))
        self.ptzControlLabel.setText(_translate("MainWindow", "PTZ Control"))
        self.leftButton.setText(_translate("MainWindow", "←"))
        self.upButton.setText(_translate("MainWindow", "↑"))
        self.homeButton.setText(_translate("MainWindow", "Home"))
        self.downButton.setText(_translate("MainWindow", "↓"))
        self.rightButton.setText(_translate("MainWindow", "→"))
        self.zoomOutButton.setText(_translate("MainWindow", "─"))
        self.zoomLabel.setText(_translate("MainWindow", "Zoom"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        self.viewLabel.setText(_translate("MainWindow", "No Channel"))
        self.ptzButton.setText(_translate("MainWindow", "PTZ Start"))
        self.chComboBox_2.setItemText(0, _translate("MainWindow", "CCTV1"))
        self.chComboBox_2.setItemText(1, _translate("MainWindow", "CCTV2"))
        self.chComboBox_2.setItemText(2, _translate("MainWindow", "CCTV3"))
        self.chComboBox_2.setItemText(3, _translate("MainWindow", "CCTV4"))
        self.chComboBox_2.setItemText(4, _translate("MainWindow", "CCTV5"))
        self.chComboBox_2.setItemText(5, _translate("MainWindow", "CCTV6"))
        self.chComboBox_2.setItemText(6, _translate("MainWindow", "CCTV7"))
        self.chComboBox_2.setItemText(7, _translate("MainWindow", "CCTV8"))
        self.chComboBox_2.setItemText(8, _translate("MainWindow", "CCTV9"))
        self.chComboBox_2.setItemText(9, _translate("MainWindow", "CCTV10"))
        self.restartButton.setText(_translate("MainWindow", "ReStart"))
        self.label_1.setText(_translate("MainWindow", "None"))
        self.cctvLabel_1.setText(_translate("MainWindow", "CCTV1"))
        self.cctvLabel_9.setText(_translate("MainWindow", "CCTV9"))
        self.cctvLabel_4.setText(_translate("MainWindow", "CCTV4"))
        self.cctvLabel_7.setText(_translate("MainWindow", "CCTV7"))
        self.cctvLabel_2.setText(_translate("MainWindow", "CCTV2"))
        self.cctvLabel_8.setText(_translate("MainWindow", "CCTV8"))
        self.label_10.setText(_translate("MainWindow", "None"))
        self.label_9.setText(_translate("MainWindow", "None"))
        self.label_7.setText(_translate("MainWindow", "None"))
        self.label_3.setText(_translate("MainWindow", "None"))
        self.label_4.setText(_translate("MainWindow", "None"))
        self.cctvLabel_3.setText(_translate("MainWindow", "CCTV3"))
        self.cctvLabel_10.setText(_translate("MainWindow", "CCTV10"))
        self.label_2.setText(_translate("MainWindow", "None"))
        self.label_8.setText(_translate("MainWindow", "None"))
        self.cctvLabel_5.setText(_translate("MainWindow", "CCTV5"))
        self.label_6.setText(_translate("MainWindow", "None"))
        self.cctvLabel_6.setText(_translate("MainWindow", "CCTV6"))
        self.label_5.setText(_translate("MainWindow", "None"))
        self.panoramaButton.setText(_translate("MainWindow", "Panorama Start"))
        self.panoramaLabel.setText(_translate("MainWindow", "panorama image"))
