# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainScreen.ui'
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
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QSize(800, 480))
        MainWindow.setMaximumSize(QSize(1280, 720))
        MainWindow.setStyleSheet(u"background-color: rgb(233,233,233);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)

        self.GPSStatusBtn = QPushButton(self.centralwidget)
        self.GPSStatusBtn.setObjectName(u"GPSStatusBtn")
        self.GPSStatusBtn.setMinimumSize(QSize(125, 50))
        font = QFont()
        font.setPointSize(16)
        self.GPSStatusBtn.setFont(font)
        self.GPSStatusBtn.setFocusPolicy(Qt.NoFocus)
        self.GPSStatusBtn.setStyleSheet(u"alternate-background-color: rgb(114, 159, 207);")
        self.GPSStatusBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.GPSStatusBtn, 0, 4, 1, 1)

        self.ConfigBtn = QPushButton(self.centralwidget)
        self.ConfigBtn.setObjectName(u"ConfigBtn")
        self.ConfigBtn.setMinimumSize(QSize(125, 80))
        font1 = QFont()
        font1.setPointSize(25)
        font1.setBold(True)
        font1.setWeight(75)
        self.ConfigBtn.setFont(font1)
        self.ConfigBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.ConfigBtn, 8, 6, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 7, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 7, 2, 1, 1)

        self.StartTimerBtn = QPushButton(self.centralwidget)
        self.StartTimerBtn.setObjectName(u"StartTimerBtn")
        self.StartTimerBtn.setMinimumSize(QSize(125, 80))
        self.StartTimerBtn.setFont(font1)
        self.StartTimerBtn.setStyleSheet(u"color: rgb(78, 154, 6);\n"
"background-color: rgb(171, 183, 183);")
        self.StartTimerBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.StartTimerBtn, 8, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.LapRecordList = QListWidget(self.centralwidget)
        self.LapRecordList.setObjectName(u"LapRecordList")
        self.LapRecordList.setEnabled(True)
        self.LapRecordList.setMinimumSize(QSize(300, 0))
        self.LapRecordList.setMaximumSize(QSize(250, 16777215))
        font2 = QFont()
        font2.setPointSize(28)
        self.LapRecordList.setFont(font2)
        self.LapRecordList.setFocusPolicy(Qt.NoFocus)
        self.LapRecordList.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.LapRecordList.setSelectionMode(QAbstractItemView.NoSelection)
        self.LapRecordList.setTextElideMode(Qt.ElideMiddle)

        self.gridLayout.addWidget(self.LapRecordList, 0, 0, 9, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.LoggerStatusBtn = QPushButton(self.centralwidget)
        self.LoggerStatusBtn.setObjectName(u"LoggerStatusBtn")
        self.LoggerStatusBtn.setEnabled(True)
        self.LoggerStatusBtn.setMinimumSize(QSize(125, 50))
        self.LoggerStatusBtn.setFont(font)
        self.LoggerStatusBtn.setFocusPolicy(Qt.NoFocus)
        self.LoggerStatusBtn.setStyleSheet(u"alternate-background-color: rgb(114, 159, 207);")
        self.LoggerStatusBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.LoggerStatusBtn, 0, 2, 1, 1)

        self.StopTimerBtn = QPushButton(self.centralwidget)
        self.StopTimerBtn.setObjectName(u"StopTimerBtn")
        self.StopTimerBtn.setMinimumSize(QSize(125, 80))
        self.StopTimerBtn.setFont(font1)
        self.StopTimerBtn.setStyleSheet(u"color: rgb(164, 0, 0);")
        self.StopTimerBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.StopTimerBtn, 8, 4, 1, 1)

        self.CANStatusBtn = QPushButton(self.centralwidget)
        self.CANStatusBtn.setObjectName(u"CANStatusBtn")
        self.CANStatusBtn.setMinimumSize(QSize(125, 50))
        self.CANStatusBtn.setFont(font)
        self.CANStatusBtn.setFocusPolicy(Qt.NoFocus)
        self.CANStatusBtn.setStyleSheet(u"alternate-background-color: rgb(114, 159, 207);")
        self.CANStatusBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.CANStatusBtn, 0, 6, 1, 1)

        self.LapTimeLbl = QLabel(self.centralwidget)
        self.LapTimeLbl.setObjectName(u"LapTimeLbl")
        font3 = QFont()
        font3.setFamily(u"FreeSans")
        font3.setPointSize(60)
        font3.setBold(True)
        font3.setWeight(75)
        font3.setKerning(True)
        self.LapTimeLbl.setFont(font3)
        self.LapTimeLbl.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.LapTimeLbl, 5, 2, 1, 5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 6, 2, 1, 1)

        self.TrackReadyLbl = QLabel(self.centralwidget)
        self.TrackReadyLbl.setObjectName(u"TrackReadyLbl")
        font4 = QFont()
        font4.setPointSize(12)
        self.TrackReadyLbl.setFont(font4)
        self.TrackReadyLbl.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.TrackReadyLbl, 2, 6, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 4, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OmeTracker", None))
        self.GPSStatusBtn.setText(QCoreApplication.translate("MainWindow", u"GPS", None))
        self.ConfigBtn.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.StartTimerBtn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.LoggerStatusBtn.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.StopTimerBtn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.CANStatusBtn.setText(QCoreApplication.translate("MainWindow", u"CAN", None))
        self.LapTimeLbl.setText(QCoreApplication.translate("MainWindow", u"0:00:00.000", None))
        self.TrackReadyLbl.setText("")
    # retranslateUi

