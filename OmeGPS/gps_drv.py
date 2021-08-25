import pynmea2
import serial
import os
from threading import Thread
import time
import io
import datetime

debug = False


'''
some notes
GPS quality - 0: invalid, 1:standalone, 2:DGPS, 3:RTK. in the main app, it will be good to differentiate standalone vs DGPS for best results.
'''


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
        self._status = {'timestamp': datetime.time(0, 0, 0), 'gps_ready': False, 'latitude': 0.0, 'longitude': 0.0,
                        'altitude': 0.0, 'gps_qual': 0.0, 'mode_fix_type': 0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0}
        self.runName = ''
        self.logFolder = os.path.expanduser(
            f'~/workspace/logs/')
        # logging related
        # create a default log file/path
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]

        self.logger = ''
        self.allowLogging = False
        self.newGGA = False
        self.SetNewLog()

        # configure GPS
        while True:

            try:
                self.ser = serial.Serial(serial_port, default_baud, timeout=1)
                break
            except Exception as e:
                self.PrintDebug(f'{e}', True)
            time.sleep(0.5)

        time.sleep(0.5)
        self.ser.write(self.serialset)
        time.sleep(0.05)
        self.PrintDebug('config serial port')
        time.sleep(0.5)
        # self.ser.close
        self.ser.baudrate = 115200
        time.sleep(0.1)
        self.PrintDebug('connected at 115200')
        self.PrintDebug('disableGLL')
        self.ser.write(self.disableGLL)
        time.sleep(0.05)
        self.PrintDebug('disableRMC')
        self.ser.write(self.disableRMC)
        time.sleep(0.05)
        self.PrintDebug('set10hz')
        self.ser.write(self.set10hz)
        time.sleep(0.05)
        self.PrintDebug('saveconfig')
        self.ser.write(self.saveconfig)
        time.sleep(0.05)
        # self.ser.reset_input_buffer()
        # threading
        self.gpsThread = Thread(target=self.ReadIncoming, daemon=True)
        self.gpsThread.start()
        self.PrintDebug('GPS initialized', True)
        

    @ property
    def gps_status(self):
        return self._status

    #use NewGGA flag to drive line trap and timer event such that when a new GPS is available, run the checks immediately for best timing
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
        self.PrintDebug('start a new log')
        try:
            self.logger.close()
        except Exception as e:
            self.PrintDebug(f"err{e}")
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
                        '%Y-%m-%d_%H-%M-%S-%f')[:-3]
                    self.logger.write(f'{_tmp_time}: {_decoded}\r\n')

            except Exception as e:
                self.PrintDebug(
                    f'read incoming err {e} with {_incoming}', True)

    def PrintDebug(self, text, override=False):
        if debug | override:
            print(text)

    def ClassifyMsgs(self, _incoming):
        _msg = pynmea2.parse(_incoming)
        if 'GNGGA' in _incoming:
            self._status.update({'timestamp': _msg.timestamp, 'latitude': _msg.latitude,
                                 'longitude': _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats': _msg.num_sats})
            self.PrintDebug(repr(_msg))
            self.newGGA = True
        elif 'VTG' in _incoming:
            self._status.update(
                {'true_track': _msg.true_track, 'groundspeed': _msg.spd_over_grnd_kmph})
            self.PrintDebug(repr(_msg))
        elif 'GSA' in _incoming:
            self._status.update({'mode_fix_type': _msg.mode_fix_type, })
            self.PrintDebug(repr(_msg))
        else:
            pass

    def GPSTimeSync(self):
        pass

    '''
    something to look at in the future. why calling this method resulted in bad runs
    def ClassifyMsgs(self, _incoming):
        print(_incoming)
        try:
            _msg = pynmea2.parse(_incoming)
        except Exception as e:
            self.PrintDebug('Parse error: {}'.format(e), True)
        if _msg.sentence_type == 'GGA':
            self._status.update({'timestamp': _msg.timestamp, 'latitude': _msg.latitude,
                               'longitude': _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats':_msg.num_sats})

        elif _msg.sentence_type == 'VTG':
            self._status.update({'true_track':_msg.true_track,'groundspeed':_msg.spd_over_grnd_kmph})
        else:
            pass
        self.PrintDebug([_msg.latitude,_msg.longitude])
        self.PrintDebug(self._status)
    '''
