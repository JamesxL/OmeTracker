import yaml


filename = 'SysConfig.yml'

SysConfig = dict(
    SuperSensor_enable=False,
    SuperSensor_path='/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0',
    GPS_enable=True,
    GPS_path='/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0',
    IMU_enable=False,
    IMU_addr=''
)

try:
    with open(filename, 'r') as f:
        SysConfig.update(yaml.safe_load(f))
except Exception as e:
    print(f'no valid file or {e}')

print(SysConfig)

try:
    with open(filename, 'w+') as f:
        yaml.dump(SysConfig, f, default_flow_style=False)
except Exception as e:
    print(f'write to new file {e}')
