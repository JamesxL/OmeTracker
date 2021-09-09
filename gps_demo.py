'''
MIT License

Copyright (c) 2021 JamesxL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This is a demo for the GPS driver. 
1. It is written for Ublox SAM-M8Q, but should be compatable to any Ublox GPS
2. You will need to set serial_port



To-do 2021/8/18
- add optional initial baudrate input for gps not default to 9600


'''


from OmeGPS.gps_drv import ome_gps
import time
import serial

#change this for your own port
serial_port = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'

gps = ome_gps(serial_port)
#gps.start_GPS_logging()
while True:
    print(gps.gps_status)
    time.sleep(1)
