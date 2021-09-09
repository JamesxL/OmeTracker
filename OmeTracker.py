import os
import time
import datetime
from OmeTimer.OmeTimer import OmeTimer
from sense_emu import SenseHat
from OmeGPS.OmeGPS import OmeGPS
from OmeCAN.OmeCAN import OmeCAN
import yaml
import csv
import numpy as np
import threading


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

DEFAULT_LOG_PATH = os.path.expanduser(f'~/workspace/logs')


debug = False


def PRINTDEBUG(text, override=False):
    if debug | override:
        print(text)


def GLOTIME():
    return (time.clock_gettime(time.CLOCK_MONOTONIC_RAW))


# hardcoding all the configs here for now
GPS_SERIAL_PORT = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'
CANPORT = 'can0'
TRACKDB = f'{__location__}/config/TrackDB.csv'


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


class OmeTracker:

    def __init__(self) -> None:

        self.O_GPS = OmeGPS(GPS_SERIAL_PORT)
        self.O_Timer = OmeTimer()
        self.O_SenseHat = SenseHat()
        self.O_CAN = OmeCAN(canport=CANPORT)
        self.track_db = TRACKDB

        # variables for finish line trap
        self.finish_line_coords = None  # both coords here
        self.car_coord = None
        self.finish_line_new_state = 0
        self.finish_line_last_state = 0

        self.tracker_status = dict(
            global_time=None, lap=None, segment=None, lap_time=None, segment_time=None, GPStimestamp=None, gps_ready=None, latitude=None, longitude=None, altitude=None, gps_qual=None, mode_fix_type=None, num_sats=None, true_track=None, groundspeed=None, accel_x=None, accel_y=None, accel_z=None
        )  # need to init this for logging

        # lapping mode related
        self.wp = ''
        self.start_finish_line = ''
        self.next_wp = ''
        self.segment_index = 0
        self.lap_count = 0
        self.isclosedcircuit = False

        # imu related
        self.imu_ready = False
        self.imu_updater = threading.Thread(
            target=self.imu_handling, daemon=True)
        self.imu_updater.start()
        

        # logger related stuffs
        self.last_log_update_time = 0
        self.log_file = None
        self.logger = None
        self.start_new_log()

        

    def start_new_log(self):
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]
        _log_file_path = os.path.expanduser(
            f'~/workspace/logs/{_tmp_time}_mainlog.csv')
        self.last_log_update_time = 0
        self.log_file = open(_log_file_path, 'w')
        self.logger = csv.DictWriter(
            self.log_file, fieldnames=list(self.tracker_status.keys()))
        self.logger.writeheader()

    def imu_handling(self):
        # run this in thread
        _last_imu_update_time = 0
        while True:
            if GLOTIME() - _last_imu_update_time > 0.03:
                while not self.O_SenseHat._imu.IMURead():
                    time.sleep(0.005)
                _last_imu_update_time = GLOTIME()
                self.imu_ready = True
            time.sleep(0.005)


    def load_waypoints(self, waypoints, start_fin_point):
        self.start_finish_line = start_fin_point
        self.wp = waypoints

    def load_finish_line(self):
        pass

    def trap_a_line(self, a_line, car):
        _fin_fin_vec = [a_line[0][0] - a_line[1][0],
                        a_line[0][1] - a_line[1][1]]
        _fin_len = np.linalg.norm(_fin_fin_vec)
        _fin_car_vec = [car[0] - a_line[1][0],
                        car[1] - a_line[1][1]]
        _fin_car_dist = np.linalg.norm(_fin_car_vec)
        _fin_car_od = np.cross(_fin_fin_vec, _fin_car_vec)/_fin_len
        trapped = False
        if abs(_fin_car_dist) < abs(_fin_len):
            self.finish_line_new_state = _fin_car_od/abs(_fin_car_od)
            if self.finish_line_last_state + self.finish_line_new_state == 0:
                #('cross the line')
                trapped = True
            self.finish_line_last_state = self.finish_line_new_state
        else:
            self.finish_line_last_state = 0
        #print(_fin_len, _fin_car_dist, _fin_car_od, TrapALine.new_state, TrapALine.last_state)
        return trapped

    def start(self):
        self.O_Timer.start_timer()
        self.O_GPS.set_new_log()
        self.O_GPS.start_new_log()
        self.O_CAN.set_new_log()
        self.O_CAN.start_new_log()

    def stop(self):
        self.O_Timer.reset()
        self.O_GPS.stop_GPS_logging()
        self.O_CAN.stop_new_log()

    def lapping_mode(self):
        # the lap mode checks if car crosses finish line by constantly monitoring GPS status. it needs to be called in a while loop at certain interval
        # when driving .lapping mode runs indefinitely so it will trip properly
        if self.O_GPS.has_new_GGA:
            self.O_GPS.has_new_GGA = False
            self.tracker_status.update(self.O_GPS.gps_status)
            _car_coord = self.tracker_status[self.tracker_status['latitude'],
                                             self.tracker_status['longitude']]
            if self.trap_a_line(self.next_wp, _car_coord):
                _glo_time = GLOTIME()
                if self.segment_index in [0, len(self.wp)]:
                    self.O_Timer.new_segment(_new_lap=True)
                    _current_elap_lap_time, _current_elap_seg_time = self.O_Timer.get_all_times()
                    self.tracker_status.update({'global_time': _glo_time, 'lap': self.lap_count, 'segment': self.segment_index,
                                                'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time})
                    self.lap_count += 1
                    self.segment_index = 1
                else:
                    self.O_Timer.new_segment()
                    _current_elap_lap_time, _current_elap_seg_time = self.O_Timer.get_all_times()
                    self.tracker_status.update({'global_time': _glo_time, 'lap': self.lap_count, 'segment': self.segment_index,
                                                'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time})
                    self.segment_index += 1

                if self.segment_index >= len(self.wp):
                    if self.isclosedcircuit:
                        self.next_wp = self.wp[0]
                    else:
                        self.segment_index = 0
                        self.next_wp = self.wp[self.segment_index]
            else:
                self.next_wp = self.wp[self.segment_index]

            _xel = self.O_SenseHat._imu.getIMUData()['accel']
            self.tracker_status.update(
                {'accel_x': -_xel[0], 'accel_y': -_xel[1], 'accel_z': _xel[2]})
            self.logger.writerow(self.tracker_status)
            self.log_file.flush
            self.last_log_update_time = GLOTIME()

    def drag_mode(self):
        pass

    def auto_log(self):
        # always run at 20hz as soon as logging starts. this helps to keep records
        _glo_time = GLOTIME()
        if _glo_time - self.last_log_update_time > 0.05:
            _current_elap_seg_time, _current_elap_lap_time = self.O_Timer.elapsed_seg_time()
            _xel = self.O_SenseHat._imu.getIMUData()['accel']
            self.tracker_status.update(self.O_GPS.gps_status)
            self.tracker_status.update({'global_time': _glo_time, 'lap': self.lap_count, 'segment': self.segment_index,
                                        'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time, 'accel_x': -_xel[0], 'accel_y': -_xel[1], 'accel_z': _xel[2]})
            self.last_log_update_time = _glo_time
            self.logger.writerow(self.tracker_status)
