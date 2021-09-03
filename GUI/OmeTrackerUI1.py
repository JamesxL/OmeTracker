# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OmeTrackerV1.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet(u"background-color: rgb(191,191,191,1);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.LapTime = QLabel(self.centralwidget)
        self.LapTime.setObjectName(u"LapTime")
        self.LapTime.setGeometry(QRect(550, 130, 591, 211))
        font = QFont()
        font.setFamilies([u"FreeSans"])
        font.setPointSize(60)
        font.setBold(True)
        font.setKerning(True)
        self.LapTime.setFont(font)
        self.LapTime.setAlignment(Qt.AlignCenter)
        self.LapRecord = QListView(self.centralwidget)
        self.LapRecord.setObjectName(u"LapRecord")
        self.LapRecord.setEnabled(True)
        self.LapRecord.setGeometry(QRect(9, 8, 421, 681))
        font1 = QFont()
        font1.setPointSize(35)
        self.LapRecord.setFont(font1)
        self.LapRecord.setFocusPolicy(Qt.NoFocus)
        self.LapRecord.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.GPSStatus = QLabel(self.centralwidget)
        self.GPSStatus.setObjectName(u"GPSStatus")
        self.GPSStatus.setGeometry(QRect(650, 10, 91, 41))
        font2 = QFont()
        font2.setPointSize(15)
        self.GPSStatus.setFont(font2)
        self.GPSStatus.setStyleSheet(u"background-color: rgb(233, 185, 110,0);")
        self.Logger = QLabel(self.centralwidget)
        self.Logger.setObjectName(u"Logger")
        self.Logger.setGeometry(QRect(780, 10, 91, 41))
        self.Logger.setFont(font2)
        self.StartTimer = QPushButton(self.centralwidget)
        self.StartTimer.setObjectName(u"StartTimer")
        self.StartTimer.setGeometry(QRect(530, 490, 221, 121))
        font3 = QFont()
        font3.setPointSize(40)
        font3.setBold(True)
        self.StartTimer.setFont(font3)
        self.StartTimer.setStyleSheet(u"color: rgb(78, 154, 6);\n"
"background-color: rgb(171, 183, 183, 1);")
        self.StopTimer = QPushButton(self.centralwidget)
        self.StopTimer.setObjectName(u"StopTimer")
        self.StopTimer.setGeometry(QRect(900, 490, 221, 121))
        self.StopTimer.setFont(font3)
        self.StopTimer.setStyleSheet(u"color: rgb(164, 0, 0);")
        self.Logger_2 = QLabel(self.centralwidget)
        self.Logger_2.setObjectName(u"Logger_2")
        self.Logger_2.setGeometry(QRect(920, 10, 91, 41))
        self.Logger_2.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LapTime.setText(QCoreApplication.translate("MainWindow", u"02:00:12.234", None))
        self.GPSStatus.setText(QCoreApplication.translate("MainWindow", u"GPS:12", None))
        self.Logger.setText(QCoreApplication.translate("MainWindow", u"Logging", None))
        self.StartTimer.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.StopTimer.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.Logger_2.setText(QCoreApplication.translate("MainWindow", u"Logging", None))
    # retranslateUi

