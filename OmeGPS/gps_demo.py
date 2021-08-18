from gps_drv import ome_gps 
import time


serial_port = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'
gps = ome_gps(serial_port)
gps.StartGpsLogging()
for i in range(100):
    pass
    print(gps.status)
    time.sleep(0.1)

gps.SetNewLog('test')

for i in range(100):
    pass
    print(gps.status)
    time.sleep(0.1)

gps.StopGpsLogging()