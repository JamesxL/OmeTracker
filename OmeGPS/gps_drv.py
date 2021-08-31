import pynmea2
import serial
import requests
from threading import Thread
import time
import datetime
import os
import sys
import yaml

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
debug = False


'''
some notes
GPS quality - 0: invalid, 1:standalone, 2:DGPS, 3:RTK. in the main app, it will be good to differentiate standalone vs DGPS for best results.
'''


def PrintDebug(text, override=False):
    if debug | override:
        print(text)


class ome_gps:
    # init constants
    disableGLL = bytearray(
        [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x01, 0x00, 0xFB, 0x11])
    disableRMC = bytearray(
        [0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0xF0, 0x04, 0x00, 0xFE, 0x17])
    set10hz = bytearray([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00,
                        0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x7A, 0x12])
    serialset = bytearray([0xB5, 0x62, 0x06, 0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0xD0, 0x08,
                          0x00, 0x00, 0x00, 0xC2, 0x01, 0x00, 0x07, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x7E])
    saveconfig = bytearray([0xB5, 0x62, 0x06, 0x09, 0x0D, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x1D, 0xAB])

    def __init__(self, serial_port, default_baud=9600):
        self._status = {'GPStimestamp': datetime.time(0, 0, 0), 'gps_ready': False, 'latitude': 0.0, 'longitude': 0.0,
                        'altitude': 0.0, 'gps_qual': 0.0, 'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0}
        self.runName = ''
        self.logFolder = os.path.expanduser(
            f'~/workspace/logs/')
        # logging related
        # create a default log file/path

        self.logger = ''
        self.allowLogging = False
        self.newGGA = False
        self.SetNewLog()
        self.MGA = UBXMGA()

        # configure GPS
        while True:

            try:
                self.ser = serial.Serial(serial_port, default_baud, timeout=1)
                break
            except Exception as e:
                PrintDebug(f'{e}', True)
            time.sleep(0.5)

        time.sleep(0.5)
        self.ser.write(self.serialset)
        time.sleep(0.05)
        PrintDebug('config serial port')
        time.sleep(0.5)
        # self.ser.close
        self.ser.baudrate = 115200
        time.sleep(0.1)
        PrintDebug('connected at 115200')
        self.MGA.BulkRun(self.ser)
        PrintDebug('disableGLL')
        self.ser.write(self.disableGLL)
        time.sleep(0.05)
        PrintDebug('disableRMC')
        self.ser.write(self.disableRMC)
        time.sleep(0.05)
        PrintDebug('set10hz')
        self.ser.write(self.set10hz)
        time.sleep(0.05)
        PrintDebug('saveconfig')
        self.ser.write(self.saveconfig)
        time.sleep(0.05)
        # self.ser.reset_input_buffer()
        # threading
        self.gpsThread = Thread(target=self.ReadIncoming, daemon=True)
        self.gpsThread.start()
        PrintDebug('GPS initialized', True)

    @ property
    def gps_status(self):
        return self._status

    # use NewGGA flag to drive line trap and timer event such that when a new GPS is available, run the checks immediately for best timing
    @ property
    def GetNewGGA(self):
        return self.newGGA

    @GetNewGGA.setter
    def GetNewGGA(self, new_state):
        self.newGGA = new_state

    def StartGpsLogging(self):
        self.allowLogging = True
        pass

    def StopGpsLogging(self):
        self.allowLogging = False
        pass

    def SetNewLog(self, name='default'):
        PrintDebug('start a new log')
        try:
            self.logger.close()
        except Exception as e:
            PrintDebug(f"err{e}")
        self.runName = name
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]
        self.logPath = os.path.expanduser(
            f'~/workspace/logs/{_tmp_time}_{name}_GPS.log')
        self.logger = open(self.logPath, 'a')

    def ReadIncoming(self):
        while True:
            _incoming = ''
            _incoming = self.ser.readline()
            self._status.update({'gps_ready': _incoming != ''})
            try:
                _decoded = _incoming.decode('ascii', errors='strict').strip()
                self.ClassifyMsgs(_decoded)
                if self.allowLogging:
                    _tmp_time = datetime.datetime.utcnow().strftime(
                        '%Y-%m-%d %H:%M:%S.%f')[:-3]
                    self.logger.write(f'{_tmp_time}: {_decoded}\r\n')

            except Exception as e:
                PrintDebug(
                    f'read incoming err {e} with {_incoming}', True)

    def ClassifyMsgs(self, _incoming):
        _msg = pynmea2.parse(_incoming)
        if 'GNGGA' in _incoming:
            self._status.update({'GPStimestamp': _msg.timestamp, 'latitude': _msg.latitude,
                                 'longitude': _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats': _msg.num_sats})
            PrintDebug(repr(_msg))
            self.newGGA = True
        elif 'VTG' in _incoming:
            self._status.update(
                {'true_track': _msg.true_track, 'groundspeed': _msg.spd_over_grnd_kmph})
            PrintDebug(repr(_msg))
        elif 'GSA' in _incoming:
            self._status.update({'mode_fix_type': _msg.mode_fix_type, })
            PrintDebug(repr(_msg))
        else:
            pass

    def GPSTimeSync(self):
        pass


class UBXMGA():
    TokenOffline = 'dwbjfCfWTXSfMDvj3oZ9xA'
    TokenOnline = 'M7Wl0T-9TmyHpfUwScphug'
    ServersOnline = ['https://online-live1.services.u-blox.com/GetOnlineData.ashx?token=',
                     'https://online-live2.services.u-blox.com/GetOnlineData.ashx?token=']
    ServersOffline = ['https://offline-live1.services.u-blox.com/GetOfflineData.ashx?token=',
                      'https://offline-live2.services.u-blox.com/GetOfflineData.ashx?token=']
    TokenStr = 'token='
    ArgsOffline = ';gnss=gps,glo;alm=gps,glo;period=5;resolution=1'
    ArgsOnline = ';gnss=gps,glo,qzss,bds,gal;datatype=eph,alm,aux,pos'

    TokenFileName = 'ubxToken.yml'
    MGADataFileName = 'ubxMGAData.yml'

    OfflineDataExpiration = 14 * 24 * 3600
    OnlineDataExpiration = 4 * 3600

    def __init__(self):
        self.MGATokens = dict(
            OnlineToken=None,
            OfflineToken=None
        )
        self.MGAData = dict(
            OnlineMGADate=None,
            OnlineMGAData=None,
            OfflineMGADate=None,
            OfflineMGAData=None
        )

        self.TokenValid = False
        self.ValidOfflineData = False
        self.ValidOnlineData = False
        self.TokenPath = os.path.join(__location__, self.TokenFileName)
        self.MGAPath = os.path.join(__location__, self.MGADataFileName)
        try:
            with open(self.TokenPath, 'r') as f:
                self.MGATokens.update(yaml.safe_load(f))
                self.TokenValid = True
        except Exception as e:
            PrintDebug(f'no valid token or {e}')
        try:
            with open(self.MGAPath, 'r') as f:
                self.MGAData.update(yaml.safe_load(f))
        except Exception as e:
            PrintDebug(f'no valid MGA data or {e}')
        self.TestMGADataValidity()

    def TestMGADataValidity(self):
        self.ValidOfflineData = (self.MGAData['OfflineMGADate'] is not None) & (
            self.MGAData['OfflineMGAData'] is not None)
        self.ValidOnlineData = (self.MGAData['OnlineMGADate'] is not None) & (
            self.MGAData['OnlineMGAData'] is not None)

    def GetValidMGAData(self):
        _tmp_time = datetime.datetime.utcnow()
        if self.ValidOnlineData & (_tmp_time - self.MGAData['OnlineMGADate'] < datetime.timedelta(seconds=self.OnlineDataExpiration)):
            _time = self.MGAData['OnlineMGADate']
            PrintDebug(f'use online MGA data from {_time}', True)
            return self.MGAData['OnlineMGAData']
        if self.ValidOfflineData & (_tmp_time - self.MGAData['OfflineMGADate'] < datetime.timedelta(seconds=self.OfflineDataExpiration)):
            _time = self.MGAData['OfflineMGADate']
            PrintDebug(f'use online MGA data from {_time}', True)
            return self.MGAData['OfflineMGAData']
        return b''

    def UpdateGPS(self, ser):
        _drainer = True
        while _drainer:
            _drainer = ser.inWaiting()
            ser.read(_drainer)
            time.sleep(0.001)
        ser.write(self.GetValidMGAData())

    def GetNewMGA(self):
        _tmp_time = datetime.datetime.utcnow()
        for _alink in self.ServersOnline:
            try:
                _req = _alink + self.TokenOnline + self.ArgsOnline
                self.MGAData['OnlineMGAData'] = requests.get(
                    _req, stream=True).content
                self.MGAData['OnlineMGADate'] = _tmp_time
                PrintDebug('received new OnlineMGAData', True)
                break
            except Exception as e:
                PrintDebug(e, True)
        for _alink in self.ServersOffline:
            try:
                _req = _alink + self.TokenOffline + self.ArgsOffline
                self.MGAData['OfflineMGAData'] = requests.get(
                    _req, stream=True).content
                self.MGAData['OfflineMGADate'] = _tmp_time
                PrintDebug('received new OfflineMGAData',True)
                break
            except Exception as e:
                PrintDebug(e, True)
        try:
            with open(self.MGAPath, 'w+') as f:
                yaml.dump(self.MGAData, f, default_flow_style=False)
        except Exception as e:
            PrintDebug(f'no valid MGA data or {e}')

    def BulkRun(self, ser):
        if self.TokenValid:
            self.GetNewMGA()
        self.TestMGADataValidity()
        self.UpdateGPS(ser)

class GPSReplay():

    def __init__(self, file):
        self._status = {'GPStimestamp': datetime.time(0, 0, 0), 'gps_ready': False, 'latitude': 0.0, 'longitude': 0.0,
                        'altitude': 0.0, 'gps_qual': 0.0, 'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0}
        self.ser = open(file,'r')
        self.newGGA = False
        
        self.gpsThread = Thread(target=self.ReadIncoming, daemon=True)
        self.gpsThread.start()
        PrintDebug('GPS Replay initialized', True)

    @ property
    def gps_status(self):
        return self._status

    # use NewGGA flag to drive line trap and timer event such that when a new GPS is available, run the checks immediately for best timing
    @ property
    def GetNewGGA(self):
        return self.newGGA

    @GetNewGGA.setter
    def GetNewGGA(self, new_state):
        self.newGGA = new_state

    def StartGpsLogging(self):
        pass

    def StopGpsLogging(self):
        pass


    def ReadIncoming(self):
        _count = 0
        _baselogtimestamp = ''
        _basenowtime = datetime.datetime.utcnow()
        while True:
            _incoming = ''
            try:
                _anewline = self.ser.readline()
                _content = _anewline.split(': ')
                
                _timestamp = datetime.datetime.strptime(_content[0],'%Y-%m-%d_%H-%M-%S-%f')
                _incoming = _content[1]
                if _count == 0:
                    _basetimestamp = _timestamp
                    
                while True:
                    if datetime.datetime.utcnow() - _basenowtime >= (_timestamp - _basetimestamp):
                        break
                    time.sleep(0.001)
                
                self._status.update({'gps_ready': _incoming != ''})
                try:
                    _decoded = _incoming#.decode('ascii', errors='strict').strip()
                    self.ClassifyMsgs(_decoded)

                except Exception as e:
                    PrintDebug(
                        f'read incoming err {e} with {_incoming}', True)
                _count +=1
            except Exception as e:
                print(e)
                break

    def ClassifyMsgs(self, _incoming):
        try:
            _msg = pynmea2.parse(_incoming)
            if 'GNGGA' in _incoming:
                self._status.update({'GPStimestamp': _msg.timestamp, 'latitude': _msg.latitude,
                                    'longitude':  _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats': _msg.num_sats})
                PrintDebug(repr(_msg))
                self.newGGA = True
            elif 'VTG' in _incoming:
                self._status.update(
                    {'true_track': _msg.true_track, 'groundspeed': _msg.spd_over_grnd_kmph})
                PrintDebug(repr(_msg))
            elif 'GSA' in _incoming:
                self._status.update({'mode_fix_type': _msg.mode_fix_type, })
                PrintDebug(repr(_msg))
            else:
                pass
        except Exception as e:
            print(e)