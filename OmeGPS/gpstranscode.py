import os
import json
import ast
import csv
path = os.path.expanduser(
            f'~/workspace/logs/Ome1/2021-09-04_15-08-44-153_pglog.txt')
f = open(path,'r')
#p = os.path.expanduser(
#            f'~/workspace/logs/Ome1/2021-09-04_16-30-22-188_default_GPST.log')
#x = open(p,'w')
#while True:
dd = {'global_time': 75.766966012, 'lap': 0, 'segment': 0, 'lap_time': 0.001, 'segment_time': 0.001, 'GPStimestamp': [16, 58, 26, 400000], 'gps_ready': True, 'latitude': 39.5396225, 'longitude': -122.331949, 'altitude': 89.9, 'gps_qual': 1, 'mode_fix_type': '3', 'num_sats': '11', 'true_track': 357.42, 'groundspeed': 15.848, 'accel_x': 0.022547468543052673, 'accel_y': -0.03751062601804733, 'accel_z': 0.9834386706352234}
col = list(dd.keys())

m = open('session1.txt', 'w')
writer = csv.DictWriter(m,fieldnames=col)
writer.writeheader()

while True:

    line = f.readline().replace("'",'"').replace("datetime.time(","[").replace('), "gps_read','], "gps_read')
    try:
        pass
        writer.writerow(ast.literal_eval(line))
    except Exception as e:
        print(e)
        break
    #writer.writerow()


