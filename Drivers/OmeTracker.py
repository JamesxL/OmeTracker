import os
import time
import datetime
from .OmeCAN import OmeCAN
from .OmeTimer import OmeTimer
from .OmeGPS import OmeGPS, GPSReplay

#from sense_emu import SenseHat
import csv
import numpy as np
import threading



__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

DEFAULT_LOG_PATH = os.path.expanduser(f'~/workspace/logs')

replay_file = '/home/james/workspace/logs/Ome1/2021-09-04_16-30-22-188_default_GPS.log'

debug = True


def PRINTDEBUG(text, override=False):
    if debug | override:
        print(text)


def GLOTIME():
    return (time.clock_gettime(time.CLOCK_MONOTONIC_RAW))


# hardcoding all the configs here for now
#GPS_SERIAL_PORT = '/dev/serial/by-id/usb-FTDI_TTL232R-3V3_FTBI9WHN-if00-port0'
#GPS_SERIAL_PORT = '/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_365C335E3539-if00'
GPS_SERIAL_PORT = '/dev/ttyS0'
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

        #self.O_SenseHat = SenseHat()
        self.O_GPS = OmeGPS(GPS_SERIAL_PORT)
        #self.O_GPS = GPSReplay(replay_file)
        self.O_Timer = OmeTimer()
        self.O_CAN = OmeCAN(canport=CANPORT)
        self.track_db = TRACKDB

        # setup sensor hat
        #self.O_SenseHat.set_imu_config(True, True, True)
        #self.O_SenseHat.get_accelerometer_raw()
        #self.O_SenseHat.set_rotation(90)

        # variables for finish line trap
        self.finish_line_coords = None  # both coords here
        self.car_coord = None
        self.finish_line_new_state = 0
        self.finish_line_last_state = 0

        self.tracker_status = dict(
            global_time=None, run_mode='circuit', lap=None, segment=None, lap_time=None, segment_time=None, GPStimestamp=None, latitude=None, longitude=None, altitude=None, gps_qual=None, mode_fix_type=None, num_sats=None, true_track=None, groundspeed=None, accel_x=None, accel_y=None, accel_z=None
        )  # need to init this for logging

        # lapping mode related
        self.is_wp_set = True
        #self.wp = [[[39.538479135735535, -122.33108483437748],[39.5384749987112, -122.33129136447995]]]
        self.wp = [[[37.386551, -121.976507], [37.385315, -121.977011]], [[37.391480, -121.996019], [37.390993, -121.996053]], [[37.395856281151175, -122.01278184373095], [37.39557472782622, -122.01284438417055]], [[37.399191243521486, -122.0277364354773], [37.398766491778865, -122.02783723303757]], [[37.40784592640769, -122.0662768452659], [37.40749509288447, -122.06643479362538]], [[37.421219133570546, -122.09238105202712], [37.42081028170965, -122.09258279891876]], [[37.44711013467561, -122.12067538620087], [37.446821132971266, -122.12120173984503]], [[37.469178298696264, -122.1551627962261], [37.46874101933634, -122.15532021040003]], [[37.483537350142505, -122.18055454055384], [37.48322820661036, -122.18088150965406]], [[37.49228548293154, -122.22053122641603], [37.49196543121171, -122.22080670122045]], [[37.496489006227065, -122.23302884687149], [37.49621380681995, -122.23317391434453]], [[37.51415285182584, -122.25601270180371], [37.513823668212154, -122.25627433514738]], [[37.526430908306715, -122.26995379736208], [37.52616713677875, -122.27034003544544]], [[37.544776640040304, -122.28772475047946], [37.54444487991503, -122.28825046342624]]]
        ##[[[0,1],[0,1]]]
        self.start_finish_line = self.wp[0] #[[0,1],[0,1]]
        self.next_wp = self.wp[0] #[[0,1],[0,1]]
        self.segment_index = 0
        self.lap_count = 0
        self.isclosedcircuit = True

        # imu related
        self.imu_ready = False
        #self.imu_updater = threading.Thread(target=self.imu_handling, daemon=True)
        #self.imu_updater.start()

        # logger related stuffs
        self.last_log_update_time = 0
        self.log_file = None
        self.logger = None
        self.allow_logging = False

        # sensor status
        self.status_5hz = dict(
            GPS_connected=False,
            GPS_ready=False,
            GPS_logging=False,
            GPS_mode=None,
            GPS_sat_count=None,
            GPS_fix_quality=None,
            CAN_connected=False,
            CAN_ready=False,
            Tracker_logging=False,
        )
        self.status_5hz_updater = threading.Thread(
            target=self.update_status_5hz, daemon=True)
        self.status_5hz_updater.start()
        self.auto_log_thread = threading.Thread(
            target=self.auto_log, daemon=True)
        self.auto_log_thread.start()
        # self.start_new_log()

    

    def start_sys_logging(self, runName='default'):
        self.O_GPS.set_new_log(runName)
        self.O_CAN.set_new_log(runName)
        self.set_new_log(runName)
        self.O_GPS.start_GPS_logging()
        self.O_CAN.start_CAN_log()
        self.allow_logging = True

    def stop_sys_logging(self):
        self.allow_logging = False
        self.O_GPS.stop_GPS_logging()
        self.O_CAN.stop_CAN_logging()
        self.stop_logging()

    def set_new_log(self, runName='default'):
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]
        _log_file_path = os.path.expanduser(
            f'~/workspace/logs/{_tmp_time}_{runName}_mainlog.csv')
        self.last_log_update_time = 0
        self.log_file = open(_log_file_path, 'w')
        self.logger = csv.DictWriter(
            self.log_file, fieldnames=list(self.tracker_status.keys()))
        self.logger.writeheader()

    def stop_logging(self):
        self.allow_logging = False
        if not self.log_file.closed:
            self.log_file.flush()
            self.log_file.close()

    def update_status_5hz(self):
        while True:
            _status = dict(
                GPS_connected=self.O_GPS.GPS_connected,
                GPS_ready=self.O_GPS.GPS_ready,
                GPS_logging=self.O_GPS.allow_logging,
                GPS_mode=self.O_GPS.GPS_status['mode_fix_type'],
                GPS_sat_count=self.O_GPS.GPS_status['num_sats'],
                GPS_fix_quality=self.O_GPS.GPS_status['gps_qual'],
                CAN_connected=self.O_CAN.CAN_connected,
                CAN_ready=self.O_CAN.CAN_ready,
                Tracker_logging=self.allow_logging, 
                groundspeed = self.O_GPS.GPS_status['groundspeed']
            )
            self.status_5hz.update(_status)
            time.sleep(0.2)

    def get_sensor_status(self):
        return self.status_5hz

    def imu_handling(self):
        pass
        # run this in thread
        #
        #_last_imu_update_time = 0
        #while True:
        #    if GLOTIME() - _last_imu_update_time > 0.03:
        #        while not self.O_SenseHat._imu.IMURead():
        #            time.sleep(0.005)
        #        _last_imu_update_time = GLOTIME()
        #        self.imu_ready = True
        #    time.sleep(0.005)

    def load_waypoints(self, waypoints, start_fin_point):
        self.start_finish_line = start_fin_point
        self.wp = waypoints

    def load_a_track(self, star_fin, waypoints):
        self.start_finish_line = star_fin
        self.wp = waypoints
        self.next_wp = star_fin
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

    def lapping_mode(self):
        # the lap mode checks if car crosses finish line by constantly monitoring GPS status. it needs to be called in a while loop at certain interval
        # when driving .lapping mode runs indefinitely so it will trip properly
        if self.is_wp_set:
            if self.O_GPS.has_new_GGA:
                self.O_GPS.has_new_GGA = False
                self.tracker_status.update(self.O_GPS.gps_status)
                _car_coord = [self.tracker_status['latitude'],self.tracker_status['longitude']]
                #PRINTDEBUG(f'next wp {self.next_wp}, car_coord {_car_coord}')
                if self.trap_a_line(self.next_wp, _car_coord):
                    PRINTDEBUG(f'trapped')
                    _glo_time = GLOTIME()
                    if self.segment_index in [0, len(self.wp)]:
                        self.O_Timer.new_segment(_new_lap=True)
                        _current_elap_lap_time, _current_elap_seg_time, _, _ = self.O_Timer.get_all_times()
                        self.tracker_status.update({'global_time': _glo_time, 'lap': self.lap_count, 'segment': self.segment_index,
                                                    'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time})
                        self.lap_count += 1
                        self.segment_index = 1
                    else:
                        self.O_Timer.new_segment()
                        _current_elap_lap_time, _current_elap_seg_time, _, _ = self.O_Timer.get_all_times()
                        self.tracker_status.update({'global_time': _glo_time, 'lap': self.lap_count, 'segment': self.segment_index,
                                                    'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time})
                        self.segment_index += 1

                    if self.segment_index >= len(self.wp):
                        if self.isclosedcircuit:
                            self.next_wp = self.wp[0]
                        else:
                            self.segment_index = 0
                            self.next_wp = self.wp[self.segment_index]
                #else:
                #    self.next_wp = self.wp[self.segment_index]

                #_xel = self.O_SenseHat._imu.getIMUData()['accel']
                self.tracker_status.update(
                    {'accel_x': 0, 'accel_y': 0, 'accel_z': 0})
                if self.allow_logging:
                    self.logger.writerow(self.tracker_status)
                    self.log_file.flush
                    self.last_log_update_time = GLOTIME()


    def drag_mode(self):
        pass

    def auto_log(self):
        # always run at 20hz as soon as logging starts. this helps to keep records
        while True:
            _glo_time = GLOTIME()
            _current_elap_lap_time, _current_elap_seg_time, _, _ = self.O_Timer.get_all_times()
            #_xel = self.O_SenseHat._imu.getIMUData()['accel']
            self.tracker_status.update(self.O_GPS.gps_status)
            self.tracker_status.update({'global_time': _glo_time, 'lap': self.lap_count, 'segment': self.segment_index,
                                        'lap_time': _current_elap_lap_time, 'segment_time': _current_elap_seg_time, 'accel_x': 0, 'accel_y': 0, 'accel_z': 0})

            if (_glo_time - self.last_log_update_time > 0.05) & self.allow_logging:
                self.last_log_update_time = _glo_time
                self.logger.writerow(self.tracker_status)
            time.sleep(0.01)
