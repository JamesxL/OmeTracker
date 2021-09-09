from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore
import sys
import os
from OmeTimer.OmeTimer import OmeTimer
from sense_emu import SenseHat
from OmeGPS.OmeGPS import OmeGPS
from OmeCAN.OmeCAN import OmeCAN

import numpy as np
import datetime
import time
import csv


from GUI.MainScreen import Ui_MainWindow as MainGUI
from GUI.ConfigPop import Ui_ConfigPop as ConfigGUI


class MainWindow(QMainWindow, MainGUI):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.system = os.uname().nodename
        self.LapTimer = OmeTimer()

        

        # set up subwindows/popups
        self.ConfigWindow = ConfigWindow()
        # placeholder for GPS
        # placeholder for Logger
        # placeholder for CAN
        self.stffs = Lapper()


        # set up bottons
        self.StopTimerBtn.clicked.connect(self.StopTimerFx)
        self.StartTimerBtn.clicked.connect(self.StartTimerFx)
        self.ConfigBtn.clicked.connect(self.OpenConfig)


        self.LapTimeUpdatTimer = QTimer(self)
        self.LapTimeUpdatTimer.timeout.connect(self.getLaptime)
        self.LapTimeUpdatTimer.setInterval(10)


        if self.system == 'raspberrypi':
            self.showFullScreen()
        else:
            self.show()

        # self.showMaximized()
        # self.showFullScreen()

    def add_LapRecord(self, value):
        self.LapRecordList.sortItems(order=Qt.AscendingOrder)
        self.LapRecordList.insertItem(0, value)
        # time.sleep(1)

    def getLaptime(self):
        _current_elap_seg_time, _current_elap_lap_time = self.LapTimer.elapsed_seg_time()
        _formatted_time = str(datetime.timedelta(
            seconds=_current_elap_lap_time))[:-3]
        self.LapTimeLbl.setText(_formatted_time)

    def StartTimerFx(self):
        if not self.LapTimeUpdatTimer.isActive():
            self.LapTimeUpdatTimer.start()
            self.LapTimer.start_timer()

    def StopTimerFx(self):
        self.LapTimer.reset()
        self.LapTimeUpdatTimer.stop()

    def OpenConfig(self):
        self.ConfigWindow.show()

    def ExitProg(self):
        app.exit()


class ConfigWindow(QMainWindow, ConfigGUI):


    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ExitBtn.clicked.connect(self.ExitProg)
        self.ReturnBtn.clicked.connect(self.CloseDialog)

    def CloseDialog(self):
        self.close()

    def ExitProg(self):
        app.exit()

class Lapper:
    color_red = (0xff, 0x00, 0x00)
    color_amber = (0xff, 0xBF, 0x00)
    color_yellow = (0xff, 0xff, 0x00)
    color_orange = (0xff, 0xA5, 0x00)
    color_gold = (0xff, 0xd7, 0x00)
    color_blue = (0, 0, 0xff)
    color_green = (0x00, 0xff, 0x00)
    color_white = (0xff, 0xff, 0xff)

    glo_gps_interval = 0.5
    glo_gps_loc = [[0, 0], [1, 0], [2, 0], [0, 1],
                [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]]
    glo_gps_clr = [[0x88, 0x88, 0x88]]*len(glo_gps_loc)


    GPS_port = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'

    def __init__(self) -> None:
        # init peripherals
        self.LapTimer = OmeTimer()
        self.GPS = OmeGPS(self.GPS_port)
        self.CAN = OmeCAN()
        self.SenseHAT = SenseHat()





app = QApplication(sys.argv)
mainWin = MainWindow()

app.exit(app.exec_())
