import pynmea2
import serial
import os
from threading import Thread
import time
import io
import datetime 

debug = True


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

    def __init__(self, serial_port):

        self.port = serial_port
        self.status = {'timestamp': datetime.time(0, 0, 0), 'latitude': 0.0, 'longitude': 0.0,
                       'altitude': 0.0, 'gps_qual': 0.0, 'num_sats': 0, 'true_track': 0.0, 'groundspeed': 0.0, }
        self.runName = ''

        # logging related
        # create a default log file/path
        _tmp_time = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        self.logPath = os.path.expanduser(f'~/workspace/logs/{_tmp_time}_default_GPS.log')
        self.allowLogging = False
        self.logger = open(self.logPath, 'a')

        # configure GPS
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.ser.write(self.serialset)
        self.PrintDebug('config serial port')
        time.sleep(1)
        self.ser.close
        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        self.PrintDebug('connected at 115200')
        self.PrintDebug('disableGLL')
        self.ser.write(self.disableGLL)
        self.PrintDebug('disableRMC')
        self.ser.write(self.disableRMC)
        self.PrintDebug('set10hz')
        self.ser.write(self.set10hz)
        self.PrintDebug('saveconfig')
        self.ser.write(self.saveconfig)
        #threading
        self.gpsThread = Thread(target=self.ReadIncoming, daemon=True)
        self.gpsThread.start()


    def StartGpsLogging(self):
        self.allowLogging = True
        pass

    def StopGpsLogging(self):
        self.allowLogging = False
        pass

    def SetNewLog(self, name):
        self.PrintDebug('start a new log')
        try:
            self.logger.close()
        except Exception as e:
            self.PrintDebug(f"err{e}")
        self.runName = name
        _tmp_time = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        self.logPath = os.path.expanduser(f'~/workspace/logs/{_tmp_time}_{name}_GPS.log')
        self.logger = open(self.logPath, 'a')

    def ReadIncoming(self):
        while True:
            _incoming = ''
            try:
                _incoming = self.ser.readline().decode('ascii',errors ='strict').strip()
                self.ClassifyMsgs(_incoming)
                if self.allowLogging:
                    _tmp_time = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
                    self.logger.write(f'{_tmp_time}: {_incoming}\r\n')

            except Exception as e:
                self.PrintDebug(f'read incoming err {e} with {_incoming}', True)

    def PrintDebug(self, text, override=False):
        if debug | override:
            print(text)

    def ClassifyMsgs(self, _incoming):
        _msg = pynmea2.parse(_incoming)
        if 'GNGGA' in _incoming:
            self.status.update({'timestamp': _msg.timestamp, 'latitude': _msg.latitude,
                               'longitude': _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats':_msg.num_sats})
            self.PrintDebug(_incoming)
        elif 'VTG' in _incoming:
            self.status.update({'true_track':_msg.true_track,'groundspeed':_msg.spd_over_grnd_kmph})
        else:
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
            self.status.update({'timestamp': _msg.timestamp, 'latitude': _msg.latitude,
                               'longitude': _msg.longitude, 'altitude': _msg.altitude, 'gps_qual': _msg.gps_qual, 'num_sats':_msg.num_sats})
            
        elif _msg.sentence_type == 'VTG':
            self.status.update({'true_track':_msg.true_track,'groundspeed':_msg.spd_over_grnd_kmph})
        else:
            pass
        self.PrintDebug([_msg.latitude,_msg.longitude])
        self.PrintDebug(self.status)
    '''