from gps_drv import ome_gps 
import time


serial_port = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'
gps = ome_gps(serial_port)
gps.StartGpsLogging()
while True:
    print(gps.status)
    time.sleep(1)
    