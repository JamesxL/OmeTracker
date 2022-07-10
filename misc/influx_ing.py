from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import pandas as pd



# You can generate a Token from the "Tokens Tab" in the UI
token = "lVW_1FGpS31BowGBtmYtNxeWoGfugyDha2gJd1CbEbrSgpgiecr0xtbLlYFBbiMP2keyoxYCH2OhRwyX3sh0pg=="
org = "musa"
bucket = "smams"

client = InfluxDBClient(url="192.168.1.147:8086", token=token)
file =  os.path.expanduser(f'/home/james/workspace/logs/testlog/000004.CSV')

df = pd.read_csv(file, header=0)

print(df)