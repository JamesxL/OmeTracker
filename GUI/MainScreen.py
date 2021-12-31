# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainScreen_dark.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 480)
        MainWindow.setMinimumSize(QSize(720, 480))
        MainWindow.setMaximumSize(QSize(1280, 720))
        MainWindow.setStyleSheet(u"background-color: rgb(12,12,12);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget.setStyleSheet(u"background-color: rgb(12,12,12);")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.LapTimeLbl = QLabel(self.centralwidget)
        self.LapTimeLbl.setObjectName(u"LapTimeLbl")
        font = QFont()
        font.setFamily(u"FreeSans")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.LapTimeLbl.setFont(font)
        self.LapTimeLbl.setStyleSheet(u"color: rgb(187, 134, 252);")
        self.LapTimeLbl.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.LapTimeLbl, 2, 2, 1, 5)

        self.TrackReadyLbl = QLabel(self.centralwidget)
        self.TrackReadyLbl.setObjectName(u"TrackReadyLbl")
        font1 = QFont()
        font1.setPointSize(12)
        self.TrackReadyLbl.setFont(font1)
        self.TrackReadyLbl.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.TrackReadyLbl, 1, 6, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.StartTimerBtn = QPushButton(self.centralwidget)
        self.StartTimerBtn.setObjectName(u"StartTimerBtn")
        self.StartTimerBtn.setMinimumSize(QSize(125, 80))
        font2 = QFont()
        font2.setPointSize(25)
        font2.setBold(True)
        font2.setWeight(75)
        self.StartTimerBtn.setFont(font2)
        self.StartTimerBtn.setFocusPolicy(Qt.NoFocus)
        self.StartTimerBtn.setStyleSheet(u"color: rgb(78,154, 6);\n"
"background-color: rgb(31, 31, 31);")
        self.StartTimerBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.StartTimerBtn, 4, 2, 1, 1)

        self.StopTimerBtn = QPushButton(self.centralwidget)
        self.StopTimerBtn.setObjectName(u"StopTimerBtn")
        self.StopTimerBtn.setMinimumSize(QSize(125, 80))
        self.StopTimerBtn.setFont(font2)
        self.StopTimerBtn.setFocusPolicy(Qt.NoFocus)
        self.StopTimerBtn.setStyleSheet(u"color: rgb(176, 0, 32);\n"
"background-color: rgb(31, 31, 31);")
        self.StopTimerBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.StopTimerBtn, 4, 4, 1, 1)

        self.LoggerStatusBtn = QPushButton(self.centralwidget)
        self.LoggerStatusBtn.setObjectName(u"LoggerStatusBtn")
        self.LoggerStatusBtn.setEnabled(True)
        self.LoggerStatusBtn.setMinimumSize(QSize(125, 50))
        font3 = QFont()
        font3.setPointSize(16)
        self.LoggerStatusBtn.setFont(font3)
        self.LoggerStatusBtn.setFocusPolicy(Qt.NoFocus)
        self.LoggerStatusBtn.setStyleSheet(u"alternate-background-color: rgb(114, 159, 207);\n"
"color: rgb(3, 218, 198);")
        self.LoggerStatusBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.LoggerStatusBtn, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)

        self.GPSStatusBtn = QPushButton(self.centralwidget)
        self.GPSStatusBtn.setObjectName(u"GPSStatusBtn")
        self.GPSStatusBtn.setMinimumSize(QSize(125, 50))
        self.GPSStatusBtn.setFont(font3)
        self.GPSStatusBtn.setFocusPolicy(Qt.NoFocus)
        self.GPSStatusBtn.setStyleSheet(u"alternate-background-color: rgb(114, 159, 207);\n"
"color: rgb(3, 218, 198);")
        self.GPSStatusBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.GPSStatusBtn, 0, 4, 1, 1)

        self.GPSspeed = QLabel(self.centralwidget)
        self.GPSspeed.setObjectName(u"GPSspeed")
        font4 = QFont()
        font4.setPointSize(25)
        self.GPSspeed.setFont(font4)
        self.GPSspeed.setStyleSheet(u"color: rgb(211, 215, 207);")
        self.GPSspeed.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.GPSspeed, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 4, 1, 1)

        self.CANStatusBtn = QPushButton(self.centralwidget)
        self.CANStatusBtn.setObjectName(u"CANStatusBtn")
        self.CANStatusBtn.setMinimumSize(QSize(125, 50))
        self.CANStatusBtn.setFont(font3)
        self.CANStatusBtn.setFocusPolicy(Qt.NoFocus)
        self.CANStatusBtn.setStyleSheet(u"alternate-background-color: rgb(114, 159, 207);\n"
"color: rgb(3, 218, 198);")
        self.CANStatusBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.CANStatusBtn, 0, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 2, 1, 1)

        self.ConfigBtn = QPushButton(self.centralwidget)
        self.ConfigBtn.setObjectName(u"ConfigBtn")
        self.ConfigBtn.setMinimumSize(QSize(125, 80))
        self.ConfigBtn.setFont(font2)
        self.ConfigBtn.setFocusPolicy(Qt.NoFocus)
        self.ConfigBtn.setAutoFillBackground(False)
        self.ConfigBtn.setStyleSheet(u"background-color: rgb(31, 31, 31);")
        self.ConfigBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.ConfigBtn, 4, 6, 1, 1)

        self.LapRecordList = QListWidget(self.centralwidget)
        self.LapRecordList.setObjectName(u"LapRecordList")
        self.LapRecordList.setEnabled(True)
        self.LapRecordList.setMinimumSize(QSize(230, 0))
        self.LapRecordList.setMaximumSize(QSize(230, 16777215))
        font5 = QFont()
        font5.setPointSize(28)
        self.LapRecordList.setFont(font5)
        self.LapRecordList.setFocusPolicy(Qt.NoFocus)
        self.LapRecordList.setStyleSheet(u"background-color: rgba(255, 255, 255,20);\n"
"color: rgb(211, 215, 207);")
        self.LapRecordList.setSelectionMode(QAbstractItemView.NoSelection)
        self.LapRecordList.setTextElideMode(Qt.ElideMiddle)

        self.gridLayout.addWidget(self.LapRecordList, 0, 0, 3, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OmeTracker", None))
        self.LapTimeLbl.setText(QCoreApplication.translate("MainWindow", u"0:00:00.00", None))
        self.TrackReadyLbl.setText("")
        self.StartTimerBtn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.StopTimerBtn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.LoggerStatusBtn.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.GPSStatusBtn.setText(QCoreApplication.translate("MainWindow", u"GPS", None))
        self.GPSspeed.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.CANStatusBtn.setText(QCoreApplication.translate("MainWindow", u"CAN", None))
        self.ConfigBtn.setText(QCoreApplication.translate("MainWindow", u"Config", None))
    # retranslateUi

