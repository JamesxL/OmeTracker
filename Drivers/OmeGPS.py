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

USEBINARY = True


UBX_DISABLEGLL = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x01, 0x00, 0xFB, 0x11])

UBX_DISABLERMC = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x04, 0x00, 0xFE, 0x17])

UBX_ENABLEGGA = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x00, 0x01, 0xFB, 0x10])

UBX_DISABLEGGA = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x00, 0x00, 0xFA, 0x0F])

UBX_DISABLEVTG = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x05, 0x00, 0xFF, 0x19])

UBX_DISABLEGSA = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x02, 0x00, 0xFC, 0x13])

UBX_DISABLEGSV = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x03, 0x00, 0xFD, 0x15])

UBX_ENABLEPVT = bytearray(
    [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x07, 0x01, 0x13, 0x51])


UBX_SET10HZ = bytearray([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00,
                         0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x7A, 0x12])
UBX_SERIALBAUD = bytearray([0xB5, 0x62, 0x06, 0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0xD0, 0x08,
                            0x00, 0x00, 0x00, 0xC2, 0x01, 0x00, 0x07, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x7E])
UBX_SAVECONFIG = bytearray([0xB5, 0x62, 0x06, 0x09, 0x0D, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1D, 0xAB])

DEFAULT_LOG_PATH = os.path.expanduser(f'~/workspace/logs')
'''
some notes
GPS quality - 0: invalid, 1:standalone, 2:DGPS, 3:RTK. in the main app, it will be good to differentiate standalone vs DGPS for best results.
'''


def PRINTDEBUG(text, override=False):
    if debug | override:
        print(text)


class OmeGPS:
    # init constants

    def __init__(self, serial_port, baudrate=9600, log_folder=DEFAULT_LOG_PATH):

        self.log_folder = log_folder
        self.serial_port = serial_port
        self.baudrate = baudrate

        self.GPS_status = {'GPStimestamp': datetime.time(0, 0, 0), 'latitude': 0.0, 'longitude': 0.0,
                           'altitude': 0.0, 'gps_qual': 0.0, 'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0}
        self.run_name = ''

        # logging related
        # create a default log file/path
        self.GPS_connected = False
        self.GPS_ready = False
        self.logger = ''
        self.allow_logging = False
        self.new_GGA = False
        # self.set_new_log()
        self.MGA = UBXMGA()
        

        # configure GPS

        # need a better way to handle GPS init failure. maybe always let it happen and finish, but only set a success flag to allow retry
        try:
            self.ser = serial.Serial(
                self.serial_port, self.baudrate, timeout=1)
            self.GPS_connected = True
        except Exception as e:
            PRINTDEBUG(f'{e}', True)
            self.GPS_connected = False
            return

        time.sleep(0.5)
        self.ser.write(UBX_SERIALBAUD)
        time.sleep(0.05)
        PRINTDEBUG('config serial port')
        time.sleep(0.5)
        # self.ser.close
        self.ser.baudrate = 115200
        time.sleep(0.1)
        PRINTDEBUG('connected at 115200')
        _config_list = []
        if USEBINARY:
            _config_list = [UBX_DISABLEGGA, UBX_DISABLEGLL, UBX_DISABLERMC, UBX_DISABLEVTG, UBX_DISABLEGSV, UBX_DISABLEGSA, UBX_ENABLEPVT]
            self.ubx_bin =  UBXReader(self.ser)

        else:
            _config_list= [UBX_ENABLEGGA, UBX_DISABLEGLL, UBX_DISABLERMC]
        _config_list.extend([UBX_SET10HZ, UBX_SAVECONFIG])
        for _msgs in _config_list:
            self.ser.write(_msgs)
            time.sleep(0.05)

        self.MGA.update_all(self.ser)

        # threading
        self.gpsThread = Thread(target=self.read_incoming, daemon=True)
        self.gpsThread.start()
        PRINTDEBUG('GPS initialized', True)

    @ property
    def gps_status(self):
        return self.GPS_status

    # use NewGGA flag to drive line trap and timer event such that when a new GPS is available, run the checks immediately for best timing

    @ property
    def has_new_GGA(self):
        return self.new_GGA

    @has_new_GGA.setter
    def has_new_GGA(self, new_state):
        self.new_GGA = new_state

    def start_GPS_logging(self):
        self.allow_logging = True
        pass

    def stop_GPS_logging(self):
        self.allow_logging = False
        pass

    def set_new_log(self, name='default'):
        PRINTDEBUG('start a new log')
        try:
            self.logger.close()
        except Exception as e:
            PRINTDEBUG(f"err{e}")
        self.run_name = name
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]
        self.logPath = os.path.expanduser(
            f'~/workspace/logs/{_tmp_time}_{name}_GPS.log')
        self.logger = open(self.logPath, 'a')

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
            
    def classify_ubx_messages(self, _incoming):
        _msg = _incoming #this is to keep format clean
        if _incoming.identity == 'NAV-PVT':
            #_timestamp = datetime.datetime(year=_msg.year, month= _msg.month, day = _msg.day, hour = _msg.hour, minute= _msg.min, second = _msg.second, microsecond = _msg.nano/100, tzinfo = UTC)
            _fix_qual_flags = int.from_bytes(_msg.flags, "little",signed=False)
            _fix_qual = max([(_fix_qual_flags & 1), (_fix_qual_flags &2)])
            self.GPS_status.update({'GPStimestamp': _msg.iTOW, 'latitude': _msg.lat/1e7,
                                    'longitude': _msg.lon/1e7, 'altitude': _msg.hMSL/1000, 'gps_qual': _fix_qual, 'num_sats': _msg.numSV, 'true_track': _msg.headVeh, 'groundspeed': _msg.gSpeed/1000, 'mode_fix_type': _msg.fixType} )
            PRINTDEBUG(repr(_incoming))
            self.new_GGA = True
        

    def classify_nmea_messages(self, _incoming):
        _msg = pynmea2.parse(_incoming)
        if 'GNGGA' in _incoming:
            self.GPS_status.update({'GPStimestamp': _msg.timestamp, 'latitude': _msg.latitude,
                                    'longitude': _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats': _msg.num_sats})
            PRINTDEBUG(repr(_msg))
            self.new_GGA = True
        elif 'VTG' in _incoming:
            self.GPS_status.update(
                {'true_track': _msg.true_track, 'groundspeed': _msg.spd_over_grnd_kmph*0.277778})
            PRINTDEBUG(repr(_msg))
        elif 'GSA' in _incoming:
            self.GPS_status.update({'mode_fix_type': _msg.mode_fix_type, })
            PRINTDEBUG(repr(_msg))
        else:
            pass


class UBXMGA:
    #TokenOffline = 'dwbjfCfWTXSfMDvj3oZ9xA'
    #TokenOnline = 'M7Wl0T-9TmyHpfUwScphug'
    URL_ONLINE_SERVER = ['https://online-live1.services.u-blox.com/GetOnlineData.ashx?token=',
                         'https://online-live2.services.u-blox.com/GetOnlineData.ashx?token=']
    URL_OFFLINE_SERVER = ['https://offline-live1.services.u-blox.com/GetOfflineData.ashx?token=',
                          'https://offline-live2.services.u-blox.com/GetOfflineData.ashx?token=']
    ARGS_OFLINE = ';gnss=gps,glo;alm=gps,glo;period=5;resolution=1'
    ARGS_ONLINE = ';gnss=gps,glo,qzss,bds,gal;datatype=eph,alm,aux,pos'

    TOKEN_FILE_NAME = 'ubxToken.yml'
    MGA_DATA_FILE_NAME = 'ubxMGAData.yml'

    OFFLINE_DATA_EXPIRATION = 14 * 24 * 3600
    ONLINE_DATA_EXPIRATION = 4 * 3600

    def __init__(self):
        self.MGA_tokens = dict(
            OnlineToken=None,
            OfflineToken=None
        )
        self.MGA_data = dict(
            OnlineMGADate=None,
            OnlineMGAData=None,
            OfflineMGADate=None,
            OfflineMGAData=None
        )

        self.token_valid = False
        self.valid_offline_data = False
        self.valid_online_data = False
        self.token_path = os.path.join(__location__, self.TOKEN_FILE_NAME)
        self.MGA_path = os.path.join(__location__, self.MGA_DATA_FILE_NAME)
        try:
            with open(self.token_path, 'r') as f:
                self.MGA_tokens.update(yaml.safe_load(f))
                self.token_valid = True
        except Exception as e:
            PRINTDEBUG(f'no valid token or {e}')
        try:
            with open(self.MGA_path, 'r') as f:
                self.MGA_data.update(yaml.safe_load(f))
        except Exception as e:
            PRINTDEBUG(f'no valid MGA data or {e}')
        self.test_MGA_data_validity()

    def test_MGA_data_validity(self):
        self.valid_offline_data = (self.MGA_data['OfflineMGADate'] is not None) & (
            self.MGA_data['OfflineMGAData'] is not None)
        self.valid_online_data = (self.MGA_data['OnlineMGADate'] is not None) & (
            self.MGA_data['OnlineMGAData'] is not None)

    def get_valid_MGA_data(self):
        _tmp_time = datetime.datetime.utcnow()
        if self.valid_online_data & (_tmp_time - self.MGA_data['OnlineMGADate'] < datetime.timedelta(seconds=self.ONLINE_DATA_EXPIRATION)):
            _time = self.MGA_data['OnlineMGADate']
            PRINTDEBUG(f'use online MGA data from {_time}', True)
            return self.MGA_data['OnlineMGAData']
        if self.valid_offline_data & (_tmp_time - self.MGA_data['OfflineMGADate'] < datetime.timedelta(seconds=self.OFFLINE_DATA_EXPIRATION)):
            _time = self.MGA_data['OfflineMGADate']
            PRINTDEBUG(f'use online MGA data from {_time}', True)
            return self.MGA_data['OfflineMGAData']
        return b''

    def update_GPS(self, ser):
        _drainer = True
        while _drainer:
            _drainer = ser.inWaiting()
            ser.read(_drainer)
        ser.write(self.get_valid_MGA_data())

    def get_new_MGA(self):
        _tmp_time = datetime.datetime.utcnow()
        for _alink in self.URL_ONLINE_SERVER:
            try:
                _req = _alink + \
                    self.MGA_tokens['TokenOnline'] + self.ARGS_ONLINE
                self.MGA_data['OnlineMGAData'] = requests.get(
                    _req, stream=True).content
                self.MGA_data['OnlineMGADate'] = _tmp_time
                PRINTDEBUG('received new OnlineMGAData', True)
                break
            except Exception as e:
                PRINTDEBUG(e, True)
        for _alink in self.URL_OFFLINE_SERVER:
            try:
                _req = _alink + \
                    self.MGA_tokens['TokenOffline'] + self.ARGS_OFLINE
                self.MGA_data['OfflineMGAData'] = requests.get(
                    _req, stream=True).content
                self.MGA_data['OfflineMGADate'] = _tmp_time
                PRINTDEBUG('received new OfflineMGAData', True)
                break
            except Exception as e:
                PRINTDEBUG(e, True)
        try:
            with open(self.MGA_path, 'w+') as f:
                yaml.dump(self.MGA_data, f, default_flow_style=False)
        except Exception as e:
            PRINTDEBUG(f'no valid MGA data or {e}')

    def update_all(self, ser):
        if self.token_valid:
            self.get_new_MGA()
        self.test_MGA_data_validity()
        self.update_GPS(ser)


class GPSReplay():

    def __init__(self, file):
        self.GPS_status = {'GPStimestamp': datetime.time(0, 0, 0), 'latitude': 0.0, 'longitude': 0.0,
                           'altitude': 0.0, 'gps_qual': 0.0, 'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0}

        self.GPS_connected = True
        self.ser = open(file, 'r')
        self.newGGA = False
        self.GPS_ready = False
        self.allow_logging =True
        self.gpsThread = Thread(target=self.read_incoming, daemon=True)
        self.gpsThread.start()
        PRINTDEBUG('GPS Replay initialized', True)

    @ property
    def gps_status(self):
        return self.GPS_status

    # use NewGGA flag to drive line trap and timer event such that when a new GPS is available, run the checks immediately for best timing
    @ property
    def has_new_GGA(self):
        return self.newGGA

    @has_new_GGA.setter
    def has_new_GGA(self, new_state):
        self.newGGA = new_state

    def start_GPS_logging(self):
        pass

    def stop_GPS_logging(self):
        pass
    
    def set_new_log(self,a):
        pass

    def read_incoming(self):
        # this is to replay log file
        _count = 0
        _baselogtimestamp = ''
        _basenowtime = datetime.datetime.utcnow()
        print('here')
        while True:
            _incoming = ''
            try:
                _anewline = self.ser.readline()
                _content = _anewline.split(': ')

                #_timestamp = datetime.datetime.strptime(
                #    _content[0], '%Y-%m-%d %H-%M-%S.%f')
                _incoming = _content[1]
                #if _count == 0:
                #    _basetimestamp = _timestamp

                #while True:
                #    if datetime.datetime.utcnow() - _basenowtime >= (_timestamp - _basetimestamp):
                #        break
                #    time.sleep(0.001)
                self.GPS_ready = _incoming != ''
                try:
                    # .decode('ascii', errors='strict').strip()
                    _decoded = _incoming
                    self.classify_messages(_decoded)

                except Exception as e:
                    PRINTDEBUG(
                        f'read incoming err {e} with {_incoming}', True)
                _count += 1
            except Exception as e:
                print(e)
                break
            time.sleep(0.001)
            

    def classify_messages(self, _incoming):
        try:
            _msg = pynmea2.parse(_incoming)
            if 'GNGGA' in _incoming:
                self.GPS_status.update({'GPStimestamp': _msg.timestamp, 'latitude': _msg.latitude,
                                        'longitude':  _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats': _msg.num_sats})
                PRINTDEBUG(repr(_msg))
                self.newGGA = True
            elif 'VTG' in _incoming:
                self.GPS_status.update(
                    {'true_track': _msg.true_track, 'groundspeed': _msg.spd_over_grnd_kmph*0.277778})
                PRINTDEBUG(repr(_msg))
            elif 'GSA' in _incoming:
                self.GPS_status.update({'mode_fix_type': _msg.mode_fix_type, })
                PRINTDEBUG(repr(_msg))
            else:
                pass
        except Exception as e:
            print(e)
