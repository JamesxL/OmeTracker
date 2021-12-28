import pynmea2
import serial
import requests
from threading import Thread
import time
import datetime
import os
import yaml

from pyubx2 import UBXReader


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

debug = False

'''
some notes
SuperSensor concept is an all-in-one remote module that has GPS-IMU and logging capacities
'''


def PRINTDEBUG(text, override=False):
    if debug | override:
        print(f'OmeSS: {text}')


class OmeSS(object):
    # init constants

    def __init__(self, serial_port, baudrate=230400):

        self.serial_port = serial_port
        self.baudrate = baudrate

        self.SS_status = {'timestamp': 0.0, 'year': 0.0, 'month': 0.0, 'day': 0.0, 'hour': 0.0, 'min': 0.0, 'sec': 0.0, 'iToW': 0.0, 'lon': 0.0, 'lat': 0.0, 'hMSL': 0.0, 'gSpeed': 0.0,
                          'headMot': 0.0, 'satcnt': 0.0, 'fixType': 0.0, 'fixstatus': 0.0, 'accel_lon': 0.0, 'accel_lat': 0.0, 'accel_gvt': 0.0, 'imu_temp': 0.0, 'baro_pres': 0.0, 'baro_temp': 0.0}
        """
        "timestamp(ms),year,month,day,hour,min,sec,iToW(ms),lon,lat,hMSL(mm),gSpeed(mm/s),headMot,satcnt,fixType,fixstatus,accel_lon,accel_lat,accel_gvt,imu_temp,baro_pres,baro_temp"
        """

        self.run_name = ''

        # logging related
        # create a default log file/path
        self.GPS_connected = False
        self.GPS_ready = False
        self.logger = ''
        self.allow_logging = False
        self.new_GGA = False

        # configure GPS

        # need a better way to handle GPS init failure. maybe always let it happen and finish, but only set a success flag to allow retry
        try:
            self.ser = serial.Serial(
                self.serial_port, self.baudrate, timeout=0.06)
            self.GPS_connected = True
        except Exception as e:
            PRINTDEBUG(f'{e}', True)
            self.GPS_connected = False
            return

        # threading
        self.gpsThread = Thread(target=self.read_incoming, daemon=True)
        self.gpsThread.start()
        time.sleep(1)
        PRINTDEBUG('OmeSS initialized', True)

    @property
    def ss_status(self):
        return self.SS_status

    # use NewGGA flag to drive line trap and timer event such that when a new GPS is available, run the checks immediately for best timing

    @property
    def has_new_GGA(self):
        return self.new_GGA

    @has_new_GGA.setter
    def has_new_GGA(self, new_state):
        self.new_GGA = new_state

    def read_incoming(self):
        while True:
            _incoming = ''
            _incoming = self.ser.readline().strip().decode('ascii')
            # PRINTDEBUG(repr(_incoming))
            if _incoming != '':
                self.new_GGA = True
                self.classify_OSS_msg(_incoming)
            else:
                self.new_GGA = False

    def classify_OSS_msg(self, _incoming):
        try:
            _msg = _incoming.split(",")
            self.SS_status = {'timestamp': int(_msg[0]), 'year': int(_msg[1]), 'month': int(_msg[2]), 'day': int(_msg[3]), 'hour': int(_msg[4]), 'min': int(_msg[5]), 'sec': int(_msg[6]),
                              'iToW': int(_msg[7]), 'lon': int(_msg[8])/1e7, 'lat': int(_msg[9])/1e7, 'hMSL': int(_msg[10])/1000, 'gSpeed': int(_msg[11])/1000, 'headMot': int(_msg[12]), 'satcnt': int(_msg[13]), 'fixType': int(_msg[14]), 'fixstatus': int(_msg[15]), 'accel_lon': float(_msg[16]), 'accel_lat': float(_msg[17]), 'accel_gvt': float(_msg[18]), 'imu_temp': float(_msg[19]), 'baro_pres': float(_msg[20]), 'baro_temp': float(_msg[21])}

        except Exception as e:
            PRINTDEBUG(f'{e}', True)
            self.new_GGA = False

        PRINTDEBUG(self.SS_status)
