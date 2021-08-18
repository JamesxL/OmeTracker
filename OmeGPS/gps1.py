import serial
import time

disableGLL = bytearray([0xB5, 0x62 , 0x06 , 0x01 , 0x03 , 0x00 , 0xF0 , 0x01 , 0x00 , 0xFB , 0x11 ])
disableRMC = bytearray([0xB5 , 0x62 , 0x06 , 0x01 , 0x03 , 0x00 , 0xF0 , 0x04 , 0x00 , 0xFE , 0x17 ])
set10hz = bytearray([0xB5,0x62 ,0x06 ,0x08 ,0x06 ,0x00 ,0x64 ,0x00 ,0x01 ,0x00 ,0x01 ,0x00 ,0x7A ,0x12])
serialset = bytearray([0xB5 , 0x62 , 0x06 , 0x00 , 0x14 , 0x00 , 0x01 , 0x00 , 0x00 , 0x00 , 0xD0 , 0x08 , 0x00 , 0x00 , 0x00 , 0xC2 , 0x01 , 0x00 , 0x07 , 0x00 , 0x03 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0xC0 , 0x7E ])
saveconfig = bytearray([0xB5 , 0x62 , 0x06 , 0x09 , 0x0D , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0xFF , 0xFF , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x03 , 0x1D , 0xAB])

ser = serial.Serial('/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0', 9600,timeout=1)

for i in range (10):
    _inc = ser.readline()
    type(_inc)
    print(_inc)

    #time.sleep(0.01)
ser.write(serialset)
print('set baudrate')
for i in range (5):
    _inc = ser.readline()
    type(_inc)
    print(_inc)

ser.close()

ser = serial.Serial('/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0', 115200)


for i in range (50):
    _inc = ser.readline()
    type(_inc)
    print(_inc)

    #time.sleep(0.01)

ser.write(disableGLL)
print('disabled GPGLL here')

for i in range (50):
    _inc = ser.readline()
    type(_inc)
    print(_inc)

    #time.sleep(0.1)

ser.write(disableRMC)
print('disabled GPRMC here')


for i in range (50):
    _inc = ser.readline()
    type(_inc)
    print(_inc)

    #time.sleep(0.1)

ser.write(set10hz)
print('set 10hz')


for i in range (50):
    _inc = ser.readline()
    type(_inc)
    print(_inc)

    #time.sleep(0.1)