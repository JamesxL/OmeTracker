import serial
import time
from datetime import datetime 
import os
import io
import pynmea2

now = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]

filepath = os.path.expanduser(f'~/workspace/logs/{now}.log')

# GPS configuration parameters
disableGLL = bytearray([0xB5, 0x62 , 0x06 , 0x01 , 0x03 , 0x00 , 0xF0 , 0x01 , 0x00 , 0xFB , 0x11 ])
disableRMC = bytearray([0xB5 , 0x62 , 0x06 , 0x01 , 0x03 , 0x00 , 0xF0 , 0x04 , 0x00 , 0xFE , 0x17 ])
set10hz = bytearray([0xB5,0x62 ,0x06 ,0x08 ,0x06 ,0x00 ,0x64 ,0x00 ,0x01 ,0x00 ,0x01 ,0x00 ,0x7A ,0x12])
serialset = bytearray([0xB5 , 0x62 , 0x06 , 0x00 , 0x14 , 0x00 , 0x01 , 0x00 , 0x00 , 0x00 , 0xD0 , 0x08 , 0x00 , 0x00 , 0x00 , 0xC2 , 0x01 , 0x00 , 0x07 , 0x00 , 0x03 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0xC0 , 0x7E ])
saveconfig = bytearray([0xB5 , 0x62 , 0x06 , 0x09 , 0x0D , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0xFF , 0xFF , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x03 , 0x1D , 0xAB])

#configure GPS
ser = serial.Serial('/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0', 9600,timeout=1)
ser.write(serialset)
print('config serial port')
time.sleep(1)
ser.close
ser = serial.Serial('/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0', 115200,timeout=1)
print('connected at 115200')
ser.write(disableGLL)
print('disableGLL')
ser.write(disableRMC)
print('disableRMC')
ser.write(set10hz)
print('set10hz')
ser.write(saveconfig)
print('saveconfig')
#ser.reset_input_buffer()

logger = open(filepath, 'a')

counter = 0
while True:
    
    _time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    _read = ser.readline()
    _decoded = ''
    
    #use try to run decoding and throw unabled ones to screen
    try:
        _decoded = _read.decode('ascii',errors ='strict').strip()
        logger.write(f'{_time}: {_decoded}\r\n')
    except:
        print(f'error decoding:{_read}')
        pass
    

    if 'GNGGA' in _decoded:
        counter = counter + 1
        print(_decoded)
        print(repr(pynmea2.parse(_decoded)))
        counter = 0


    