# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConfigPop.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigPop(object):
    def setupUi(self, ConfigPop):
        if not ConfigPop.objectName():
            ConfigPop.setObjectName(u"ConfigPop")
        ConfigPop.resize(400, 240)
        ConfigPop.setMinimumSize(QSize(400, 240))
        ConfigPop.setMaximumSize(QSize(1280, 720))
        ConfigPop.setStyleSheet(u"background-color: rgb(233,233,233);")
        self.centralwidget = QWidget(ConfigPop)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ReturnBtn = QPushButton(self.centralwidget)
        self.ReturnBtn.setObjectName(u"ReturnBtn")
        self.ReturnBtn.setMinimumSize(QSize(0, 50))
        self.ReturnBtn.setStyleSheet(u"background-color: rgb(138, 226, 52);")

        self.gridLayout.addWidget(self.ReturnBtn, 2, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.SelectTrack = QPushButton(self.centralwidget)
        self.SelectTrack.setObjectName(u"SelectTrack")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectTrack.sizePolicy().hasHeightForWidth())
        self.SelectTrack.setSizePolicy(sizePolicy)
        self.SelectTrack.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.SelectTrack, 1, 0, 1, 1)

        self.ExitBtn = QPushButton(self.centralwidget)
        self.ExitBtn.setObjectName(u"ExitBtn")
        self.ExitBtn.setMinimumSize(QSize(0, 50))
        self.ExitBtn.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.ExitBtn.setAutoDefault(True)

        self.gridLayout.addWidget(self.ExitBtn, 3, 0, 1, 1)

        ConfigPop.setCentralWidget(self.centralwidget)

        self.retranslateUi(ConfigPop)

        QMetaObject.connectSlotsByName(ConfigPop)
    # setupUi

    def retranslateUi(self, ConfigPop):
        ConfigPop.setWindowTitle(QCoreApplication.translate("ConfigPop", u"OmeConfiguration", None))
        self.ReturnBtn.setText(QCoreApplication.translate("ConfigPop", u"Return", None))
        self.label.setText(QCoreApplication.translate("ConfigPop", u"Select Track and Config", None))
        self.SelectTrack.setText(QCoreApplication.translate("ConfigPop", u"Select Track", None))
        self.ExitBtn.setText(QCoreApplication.translate("ConfigPop", u"Exit", None))
    # retranslateUi

