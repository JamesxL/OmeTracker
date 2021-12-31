from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore
import sys
import os
from Drivers.OmeTracker import OmeTracker


import numpy as np
import datetime
import time
import csv
import random


from GUI.MainScreen import Ui_MainWindow as MainGUI
from GUI.ConfigPop import Ui_ConfigPop as ConfigGUI
from GUI.GMeter import Ui_Gmeter as GMeterGUI


class AccelMeter(QWidget):
    dotsize = 20
    xcenter = 115
    ycenter = 100
    deadband = 0.05
    pixel_g_ratio = 60

    def __init__(self):
        super().__init__()
        self.rect = QRect()
        self.newpos = QPoint()
        self.rect = QRect(
            QPoint(self.xcenter-self.dotsize/2, self.ycenter-self.dotsize/2), QSize(self.dotsize, self.dotsize)
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.yellow, 2, Qt.SolidLine))
        painter.drawEllipse(55, 40, 120, 120)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawEllipse(25, 10, 180, 180)
        painter.setPen(QPen(Qt.gray, 2, Qt.DashLine))
        painter.drawLine(115, 0, 115, 200)
        painter.drawLine(15, 100, 215, 100)
        painter.setPen(QPen(Qt.red, 0, Qt.DashLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(self.rect)

        # self.paintMap(qp)

    def updateDotLoc(self, x, y):
        # tbd take input in coord or in G. maybe better to take in g and filter from here
        self.rect.moveTo(x*self.pixel_g_ratio+self.xcenter-self.dotsize/2, self.ycenter-y*self.pixel_g_ratio-self.dotsize/2)
        self.update()

    def paintMap(self, qp):
        qp.setBrush(QColor(200, 162, 200))  # lilac
        qp.setPen(QColor(200, 162, 200))
        qp.drawRect(self.rect())


class MainWindow(QMainWindow, MainGUI):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.accel = AccelMeter()
        self.gridLayout.addWidget(self.accel, 3, 0, 2, 1)

        self.xx = 0
        self.yy = 0

        self.system = os.uname().nodename
        self.Tracker = OmeTracker()

        # set up subwindows/popups
        self.ConfigWindow = ConfigWindow()
        self.GMeterWindow = GMeterWindow()

        # set up bottons
        self.StartTimerBtn.clicked.connect(self.StartTiming)
        self.StopTimerBtn.clicked.connect(self.StopTiming)
        self.ConfigBtn.clicked.connect(self.OpenConfig)
        # self.ConfigBtn.clicked.connect(self.OpenGMeter)

        self.ClockUpdater = QTimer(self)
        self.ClockUpdater.timeout.connect(self.UpdateClock)
        self.ClockUpdater.setInterval(20)
        self.ClockUpdater.start()

        self.SensorUpdater = QTimer(self)
        self.SensorUpdater.timeout.connect(self.UpdateSensor)
        self.SensorUpdater.start(100)

        self.RunMode = 'circuit'
        self.ModeRunner = QTimer(self)
        self.ModeRunner.setInterval(5)
        self.ConfigureRunMode()

        self.Tracker.start_sys_logging()

        self.StartTiming()

        if self.system == 'raspberrypi':
            self.showFullScreen()
        else:
            self.show()

        # self.StartTiming()

        # self.showMaximized()
        # self.showFullScreen()

    def StartTiming(self):
        self.Tracker.O_Timer.start_timer()
        self.ModeRunner.start()
        self.StartTimerBtn.setEnabled(False)
        self.StopTimerBtn.setEnabled(True)

    def StopTiming(self):
        self.Tracker.O_Timer.stop_timer()
        self.ModeRunner.stop()
        self.StartTimerBtn.setEnabled(True)
        self.StopTimerBtn.setEnabled(False)

    def ConfigureRunMode(self, mode='circuit'):
        if mode == 'circuit':
            self.ModeRunner.timeout.connect(self.Tracker.lapping_mode)
            pass

    def UpdateClock(self):
        self.accel.updateDotLoc(self.Tracker.get_accel_lat(),self.Tracker.get_accel_lon())
        _lap_time, _, _, _last_lap_time = self.Tracker.O_Timer.get_all_times()
        if _lap_time != 0:
            _formatted_time1 = str(datetime.timedelta(
                seconds=_lap_time))[:-4]
        else:
            _formatted_time1 = '0:00:00.000'
        self.LapTimeLbl.setText(_formatted_time1)
        if self.Tracker.O_Timer.is_new_lap:
            _formatted_time2 = str(datetime.timedelta(
                seconds=_last_lap_time))[:-4]
            self.LapRecordList.insertItem(0, _formatted_time2)
            self.Tracker.O_Timer.is_new_lap_data = False


    def UpdateGPSBtn(self, style=(255, 255, 255), text='GPS'):
        self.GPSStatusBtn.setStyleSheet(style)
        self.GPSStatusBtn.setText(text)

    def UpdateCANBtn(self, style=(255, 255, 255), text='CAN'):
        self.CANStatusBtn.setStyleSheet(style)
        self.CANStatusBtn.setText(text)

    def UpdateLogBtn(self, style=u"background-color: rgb(255, 255, 255);", text='Log'):
        self.LoggerStatusBtn.setStyleSheet(style)
        self.LoggerStatusBtn.setText(text)

    def UpdateSensor(self):
        _status = self.Tracker.get_sensor_status()
        self.GMeterWindow.LonG.display(self.Tracker.get_accel_lon())
        self.GMeterWindow.LatG.display(self.Tracker.get_accel_lat())
        if not _status['GPS_connected']:
            self.UpdateGPSBtn(u"background-color: rgb(176, 0, 32);", "NO GPS")
        else:
            _txt = 'GPS'
            if not _status['GPS_ready']:
                _txt = 'GGA'
                self.UpdateGPSBtn(
                    u"background-color: rgb(176, 0, 32);", _txt)
            else:
                if (_status['GPS_mode'] == 0) | (_status['GPS_fix_quality'] & 1 == 0):
                    _txt = 'NO FIX'
                    self.UpdateGPSBtn(
                        u"background-color: rgb(255, 255, 0);", _txt)
                else:
                    GPS_fix_modes = {'2': '2D', '3': '3D'}
                    GPS_fix_quals = {'1': '', '2': 'D'}
                    _fix_qual = max(
                        [(_status['GPS_fix_quality'] & 1), (_status['GPS_fix_quality'] & 2)])
                    _txt = GPS_fix_modes.get(str(
                        _status['GPS_mode'])) + GPS_fix_quals.get(str(_fix_qual))+f":{_status['GPS_sat_count']}"
                    self.UpdateGPSBtn(
                        u"background-color: rgb(176,246,81);", _txt)
            _spd = _status['groundspeed']
            if _spd is not None:
                _spd = "{:.1f}".format(_spd*2.23693629)
                self.GPSspeed.setText(_spd)
            else:
                self.GPSspeed.setText('0.0')

        if not _status['CAN_connected']:
            self.UpdateCANBtn(u"background-color: rgb(176, 0, 32);", "NO CAN")
        else:
            if not _status['CAN_ready']:
                self.UpdateGPSBtn(
                    u"background-color: rgb(176, 0, 32);", "NO COMM")
            else:
                self.UpdateGPSBtn(
                    u"background-color: rgb(176,246,81);", "CAN OK")
        if (_status['Tracker_logging']):
            self.UpdateLogBtn(u"background-color: rgb(176,246,81);", "Logging")
        else:
            self.UpdateLogBtn(text="NLOG")

    def OpenConfig(self):
        self.ConfigWindow.show()

    def OpenGMeter(self):
        self.GMeterWindow.show()

    def ExitProg(self):
        self.Tracker.stop_sys_logging()
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


class GMeterWindow(QMainWindow, GMeterGUI):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ReturnBtn.clicked.connect(self.CloseDialog)

    def CloseDialog(self):
        self.close()


app = QApplication(sys.argv)
mainWin = MainWindow()

app.exit(app.exec_())
