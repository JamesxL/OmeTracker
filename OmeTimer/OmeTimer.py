import time
import os

# use time time.clock_gettime(time.CLOCK_MONOTONIC_RAW) for oscillator based timing for best real time results

# run logic, treat everything as segment. and only trip if it is a new lap
# probably run at 100hz if the main runs at 50hz(given gps only updates at 10hz)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

debug = False

DEFAULT_LOG_PATH = os.path.expanduser(f'~/workspace/logs')

def PRINTDEBUG(text, override=False):
    if debug | override:
        print(text)

class OmeTimer:
    def __init__(self):
        self.lap_start_time = 0  # start time of the lap
        self.seg_start_time = 0  # start time of the segment
        self.current_elap_lap_time = 0  # elapsed time for current lap
        self.current_elap_seg_time = 0  # elapsed time for current lap
        self.last_seg_time = 0  # previous segment time
        self.last_lap_time = 0  # previous lap time
    # to do. maybe combine the 2 timer to a thread for running continuously. Then only call to return value
    
    def start_timer(self):
        _time_now = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        self.seg_start_time = _time_now
        self.lap_start_time = _time_now
        pass

    def elapsed_seg_time(self, _time_now=None):
        if _time_now is None:
            _time_now = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        if debug:
            PRINTDEBUG(_time_now)
        
        if (self.seg_start_time !=0) & (self.lap_start_time != 0):
            self.current_elap_seg_time = float("{:.3f}".format(_time_now - self.seg_start_time))
            self.current_elap_lap_time = float("{:.3f}".format(_time_now - self.lap_start_time))
        return [self.current_elap_seg_time, self.current_elap_lap_time]

    def new_segment(self, _time_now=None, _new_lap=False):
        if _time_now is None:
            _time_now = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        if debug:
            PRINTDEBUG(_time_now)
        # run time recording right before cut out
        self.elapsed_seg_time(_time_now)
        # copy the time over and set up new seg/lap start time
        self.last_seg_time = self.current_elap_seg_time
        self.seg_start_time = _time_now
        if _new_lap:
            self.last_lap_time = self.current_elap_lap_time
            self.lap_start_time = _time_now
        # no return. the main will call seg time or lap time accordingly to grab them

    #@property
    def get_all_times(self):
        # return all 4 run time items
        _tmp = [self.current_elap_lap_time, self.current_elap_seg_time]
        return _tmp
    
    def reset(self):
        self.lap_start_time = 0  
        self.seg_start_time = 0  
        self.current_elap_lap_time = 0 
        self.current_elap_seg_time = 0  
        self.last_seg_time = 0 
        self.last_lap_time = 0  



"""
a = OmeTimer()
run_amount = 1000000
print(timeit.timeit(setup=a.ElapsedSegTime, number=run_amount)/run_amount)
"""