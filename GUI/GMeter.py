# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GMeter.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Gmeter(object):
    def setupUi(self, Gmeter):
        if not Gmeter.objectName():
            Gmeter.setObjectName(u"Gmeter")
        Gmeter.resize(400, 240)
        Gmeter.setMinimumSize(QSize(400, 240))
        Gmeter.setMaximumSize(QSize(1280, 720))
        Gmeter.setStyleSheet(u"background-color: rgb(233,233,233);")
        self.centralwidget = QWidget(Gmeter)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.LatG = QLCDNumber(self.centralwidget)
        self.LatG.setObjectName(u"LatG")
        font = QFont()
        font.setPointSize(15)
        self.LatG.setFont(font)

        self.gridLayout_2.addWidget(self.LatG, 2, 1, 1, 1)

        self.ReturnBtn = QPushButton(self.centralwidget)
        self.ReturnBtn.setObjectName(u"ReturnBtn")
        self.ReturnBtn.setMinimumSize(QSize(0, 50))
        self.ReturnBtn.setStyleSheet(u"background-color: rgb(138, 226, 52);")

        self.gridLayout_2.addWidget(self.ReturnBtn, 3, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)

        self.LonG = QLCDNumber(self.centralwidget)
        self.LonG.setObjectName(u"LonG")
        self.LonG.setFont(font)

        self.gridLayout_2.addWidget(self.LonG, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        Gmeter.setCentralWidget(self.centralwidget)

        self.retranslateUi(Gmeter)

        QMetaObject.connectSlotsByName(Gmeter)
    # setupUi

    def retranslateUi(self, Gmeter):
        Gmeter.setWindowTitle(QCoreApplication.translate("Gmeter", u"OmeConfiguration", None))
        self.ReturnBtn.setText(QCoreApplication.translate("Gmeter", u"Return", None))
        self.label.setText(QCoreApplication.translate("Gmeter", u"Acceleration Meter", None))
        self.label_2.setText(QCoreApplication.translate("Gmeter", u"Log", None))
        self.label_3.setText(QCoreApplication.translate("Gmeter", u"Lat", None))
    # retranslateUi

