'''
This file is used to play with ideas. It maybe random stuff that won't run

a few run modes(top level states)
1. timer
-- check_gps_ready(idle) -> 
2. learner
3. ? 



'''

import time
from sense_emu import SenseHat
from Drivers.OmeGPS import OmeGPS
from Drivers.OmeTimer import OmeTimer
import time
from threading import Thread
import numpy as np
import datetime
import os
import csv

# change this for your own port
serial_port = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'

gps = OmeGPS(serial_port)
sense = SenseHat()
sense.set_imu_config(True, True, True)
sense.set_rotation(90)
print(sense.get_accelerometer_raw())

timer = OmeTimer()


fix_state = 0
sat_num = 0

color_red = (0xff, 0x00, 0x00)
color_amber = (0xff, 0xBF, 0x00)
color_yellow = (0xff, 0xff, 0x00)
color_orange = (0xff, 0xA5, 0x00)
color_gold = (0xff, 0xd7, 0x00)
color_blue = (0, 0, 0xff)
color_green = (0x00, 0xff, 0x00)
color_white = (0xff, 0xff, 0xff)

glo_gps_interval = 0.5
glo_gps_loc = [[0, 0], [1, 0], [2, 0], [0, 1],
               [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]]
glo_gps_clr = [[0x88, 0x88, 0x88]]*len(glo_gps_loc)

'''
display planning
pixel 0,1,2,8,9,10,16,17,18 - GPS status - color = fix status - count*2 = sat count
pixel center 2 lights x and y - Acceleration 0,0.25,0.5,0.75,1G - red
pixel lower left - brake pedal - red
pixel lower right - gas pedal - green

display procss 1
an in-app frame buffer(iafb) array running at 10hz that sets all pixels to hat's fb
each thread/sub-app writes to the iafb. 

display process 2
just call set pixels ad-hoc. it may be in race condition vs other threads.need to see how the driver handles race conditions

'''


def TrapALine(coordFin1, coordFin2, coordCar):
    _fin_fin_vec = [coordFin1[0] - coordFin2[0],
                    coordFin1[1] - coordFin2[1]]
    _fin_len = np.linalg.norm(_fin_fin_vec)
    _fin_car_vec = [coordCar[0] - coordFin2[0],
                    coordCar[1] - coordFin2[1]]
    _fin_car_dist = np.linalg.norm(_fin_car_vec)
    _fin_car_od = np.cross(_fin_fin_vec, _fin_car_vec)/_fin_len
    trapped = False
    if abs(_fin_car_dist) < abs(_fin_len):
        TrapALine.new_state = _fin_car_od/abs(_fin_car_od)
        if TrapALine.last_state + TrapALine.new_state == 0:
            #('cross the line')
            trapped = True
        TrapALine.last_state = TrapALine.new_state
    else:
        TrapALine.last_state = 0
    #print(_fin_len, _fin_car_dist, _fin_car_od, TrapALine.new_state, TrapALine.last_state)
    return trapped


TrapALine.new_state = 0
TrapALine.last_state = 0


def gps_status_check(hat_obj, gps_obj):
    global glo_gps_clr, glo_gps_loc, glo_gps_interval
    # display rules
    # all pixels flash red at 5hz - no GPS connected, comm error
    # valid comm in 2hz
    # pixels in red = no fix
    # pixels in orange = 2D fix
    # pixels in blue = 3D fix
    # pixels in green = DGPS
    # unknown fix quality in white
    while True:
        _gps_status = gps_obj.gps_status
        _sat_count_div2 = int(_gps_status.get('num_sats'))//2
        _gps_qual = _gps_status.get('gps_qual')
        _mode_fix_type = _gps_status.get('mode_fix_type')
        if not gps_obj.GPS_ready:
            # no GPS,entire block red
            glo_gps_clr = [color_red]*len(glo_gps_loc)
            glo_gps_interval = 0.2
        else:
            glo_gps_interval = 0.5
            if _gps_qual == 0:
                glo_gps_clr = [color_red]*len(glo_gps_loc)
            elif _gps_qual == 1:
                if _mode_fix_type == 1:
                    glo_gps_clr = [color_red] * _sat_count_div2 + \
                        [[0, 0, 0]] * (len(glo_gps_loc)-_sat_count_div2)
                elif _mode_fix_type == 2:
                    glo_gps_clr = [color_orange] * _sat_count_div2 + \
                        [[0, 0, 0]] * (len(glo_gps_loc)-_sat_count_div2)
                else:
                    glo_gps_clr = [color_blue] * _sat_count_div2 + \
                        [[0, 0, 0]] * (len(glo_gps_loc)-_sat_count_div2)
            elif _gps_qual == 2:
                glo_gps_clr = [color_green] * _sat_count_div2 + \
                    [[0, 0, 0]] * (len(glo_gps_loc)-_sat_count_div2)
            else:
                glo_gps_clr = [color_white] * len(glo_gps_loc)
        # GPS incoming at 10hz, check at 5x
        time.sleep(0.025)


def gps_pixel_plotter():
    global sense, glo_gps_interval, glo_gps_loc, glo_gps_clr
    # the function takes arguments
    # color_set in [[coord1,color1],[coord2, color2]...]
    while True:
        time.sleep(glo_gps_interval)
        for i in range(len(glo_gps_loc)):
            sense.set_pixel(glo_gps_loc[i][0],
                            glo_gps_loc[i][1], glo_gps_clr[i])
        time.sleep(glo_gps_interval)
        for i in range(len(glo_gps_loc)):
            sense.set_pixel(glo_gps_loc[i][0], glo_gps_loc[i][1], [0, 0, 0])


imu_ready = False


def prim_imu():
    # the sensor read time is ~20ms per run, to run it at 33ms cycle
    global imu_ready
    _lasttime = 0
    while True:

        if time.clock_gettime(time.CLOCK_MONOTONIC_RAW) - _lasttime > 0.03:
            while not sense._imu.IMURead():
                time.sleep(0.005)
            _lasttime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
            imu_ready = True
        time.sleep(0.005)


# start the actual stuffs
sense.show_message('Ome Tracker', scroll_speed=0.05)
# start the actual stuffs

sense.clear(0, 0, 0)
time.sleep(1)

GpsPlotThread = Thread(target=gps_pixel_plotter, daemon=True)
GpsStateThread = Thread(target=gps_status_check,
                        args=(sense, gps), daemon=True)
IMUThread = Thread(target=prim_imu, daemon=True)
GpsPlotThread.start()
GpsStateThread.start()
IMUThread.start()
gps.set_new_log()
gps.start_GPS_logging()


# 2 main run modes: accel and lap
# accel is 0-x type
# lap mode is close circuit vs non close circuit
wp = [[[37.386551, -121.976507], [37.385315, -121.977011]], [[37.391480, -121.996019], [37.390993, -121.996053]], [[37.395856281151175, -122.01278184373095], [37.39557472782622, -122.01284438417055]], [[37.399191243521486, -122.0277364354773], [37.398766491778865, -122.02783723303757]], [[37.40784592640769, -122.0662768452659], [37.40749509288447, -122.06643479362538]], [[37.421219133570546, -122.09238105202712], [37.42081028170965, -122.09258279891876]], [[37.44711013467561, -122.12067538620087], [37.446821132971266, -122.12120173984503]], [[37.469178298696264, -
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     122.1551627962261], [37.46874101933634, -122.15532021040003]], [[37.483537350142505, -122.18055454055384], [37.48322820661036, -122.18088150965406]], [[37.49228548293154, -122.22053122641603], [37.49196543121171, -122.22080670122045]], [[37.496489006227065, -122.23302884687149], [37.49621380681995, -122.23317391434453]], [[37.51415285182584, -122.25601270180371], [37.513823668212154, -122.25627433514738]], [[37.526430908306715, -122.26995379736208], [37.52616713677875, -122.27034003544544]], [[37.544776640040304, -122.28772475047946], [37.54444487991503, -122.28825046342624]]]
#print(f'wp count {len(wp)}')
start = wp[0]
fin = wp[len(wp)-1]
car_loc = []
track_state = dict(
    global_time=None, lap=None, segment=None, lap_time=None, segment_time=None, GPStimestamp=None, gps_ready=None, latitude=None, longitude=None, altitude=None, gps_qual=None, mode_fix_type=None, num_sats=None, true_track=None, groundspeed=None, accel_x=None, accel_y=None, accel_z=None
)

track_state.update(gps.gps_status)
indicator_timer = 0
log_timer = 0
_tmp_time = datetime.datetime.utcnow().strftime(
    '%Y-%m-%d_%H-%M-%S-%f')[:-3]
logfile = os.path.expanduser(f'~/workspace/logs/{_tmp_time}_pglog.csv')
# print(logfile)
m = open(logfile, 'w')
f = csv.DictWriter(m, fieldnames=list(track_state.keys()))
f.writeheader()


seg_index = 0
next_wp = wp[seg_index]
lap = 0

record_keeper = []
isclosedcircuit = False
timer.start_timer()
while True:
    if gps.has_new_GGA:
        gps.has_new_GGA = False
        track_state.update(gps.gps_status)
        _car_loc = [track_state.get('latitude'), track_state.get('longitude')]
        if TrapALine(next_wp[0], next_wp[1], _car_loc):
            # print(seg_index)
            _glo_time = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
            if seg_index in [0, len(wp)]:
                # next wp is start point
                timer.new_segment(_new_lap=True)
                _current_elap_lap_time, _current_elap_seg_time = timer.get_all_times()
                track_state.update({'global_time': _glo_time, 'lap': lap, 'segment': seg_index,
                                    'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time})
                lap += 1
                seg_index = 1
                #print(f'cross start{track_state}')

            else:
                timer.new_segment()
                _current_elap_lap_time, _current_elap_seg_time = timer.get_all_times()
                track_state.update({'global_time': _glo_time, 'lap': lap, 'segment': seg_index,
                                    'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time})
                seg_index += 1

            if seg_index >= len(wp):
                if isclosedcircuit:
                    # keep the index but change wp to 0
                    next_wp = wp[0]
                else:
                    # wrap to start line
                    seg_index = 0
                    next_wp = wp[seg_index]
            else:
                next_wp = wp[seg_index]
            _xel = sense._imu.getIMUData()['accel']
            track_state.update(
                {'accel_x': -_xel[0], 'accel_y': -_xel[1], 'accel_z': _xel[2]})
            #next_wp = wp[seg_index]
            f.writerow(track_state)
            m.flush()
            log_timer = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
            sense.set_pixel(7, 7, [125, 233, 12])
            indicator_timer = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)

    if time.clock_gettime(time.CLOCK_MONOTONIC_RAW) - indicator_timer > 10:
        sense.set_pixel(7, 7, [5, 5, 5])
        indicator_timer = 0

    if time.clock_gettime(time.CLOCK_MONOTONIC_RAW) - log_timer >= 0.05:
        _current_elap_lap_time, _current_elap_seg_time = timer.elapsed_seg_time()
        _glo_time = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        _xel = sense._imu.getIMUData()['accel']
        track_state.update({'global_time': _glo_time, 'lap': lap, 'segment': seg_index,
                            'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time, 'accel_x': -_xel[0], 'accel_y': -_xel[1], 'accel_z': _xel[2]})
        log_timer = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        f.writerow(track_state)

    time.sleep(0.01)
