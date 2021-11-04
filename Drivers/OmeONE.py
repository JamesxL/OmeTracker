import serial
from threading import Thread
import time
import datetime
import os
import yaml


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

debug = False

USEBINARY = True


def PRINTDEBUG(text, override=False):
    if debug | override:
        print(text)


DEFAULT_LOG_PATH = os.path.expanduser(f'~/workspace/logs')


class OmeOne:
    def __init__(self, serial_port, baudrate=9600, log_folder=DEFAULT_LOG_PATH):

        self.log_folder = log_folder
        self.serial_port = serial_port
        self.baudrate = baudrate

        self.ONE_status = {'GPStimestamp': datetime.time(0, 0, 0), 'latitude': 0.0, 'longitude': 0.0,
                           'altitude': 0.0, 'gps_qual': 0.0, 'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0}

        self.ONE_status = {'timestamp': 0, 'year': 0, 'month': 0, 'day': 0, 'hour': 0, 'min': 0, 'sec': 0, 'iToW': 0, 'longitude': 0, 'latitude': 0, 'altitude': 0, 'gps_qual': 0.0,
                           'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0, 'accel_lon': 0, 'accel_lat': 0, 'accel_gvt': 0, 'imu_temp': 0, 'baro_pressure': 0, 'baro_temp': 0}

        self.run_name = ''

        # logging related
        # create a default log file/path
        self.GPS_connected = False
        self.GPS_ready = False
        self.logger = ''
        self.allow_logging = False
        self.new_GGA = False

        # need a better way to handle GPS init failure. maybe always let it happen and finish, but only set a success flag to allow retry
        try:
            self.ser = serial.Serial(
                self.serial_port, self.baudrate, timeout=1)
            self.GPS_connected = True
        except Exception as e:
            PRINTDEBUG(f'{e}', True)
            self.GPS_connected = False
            return

        time.sleep(0.05)
        PRINTDEBUG('config serial port')
        time.sleep(0.5)
        # self.ser.close
        self.ser.baudrate = 115200
        time.sleep(0.1)
        PRINTDEBUG('connected at 115200')

        # threading
        self.gpsThread = Thread(target=self.read_incoming, daemon=True)
        self.gpsThread.start()
        PRINTDEBUG('GPS initialized', True)

    def read_incoming(self):
        while True:
            _incoming = ''
            try:
                if USEBINARY:
                    _decoded, _parsed = self.ubx_bin.read()
                    self.classify_ubx_messages(_parsed)
                else:
                    _incoming = self.ser.readline()
                    _decoded = _incoming.decode(
                        'ascii', errors='strict').strip()
                    self.classify_nmea_messages(_decoded)
                self.GPS_ready = (_decoded != '')
                if self.allow_logging:
                    _tmp_time = datetime.datetime.utcnow().strftime(
                        '%Y-%m-%d %H:%M:%S.%f')[:-3]
                    self.logger.write(f'{_tmp_time}: {_decoded}\r\n')

            except Exception as e:
                PRINTDEBUG(
                    f'read incoming err {e} with ', True)

    def classify_ONE_message(self, _incoming):
        msg = _incoming.split(',')
