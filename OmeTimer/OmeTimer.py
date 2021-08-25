import time
import timeit

# use time time.clock_gettime(time.CLOCK_MONOTONIC_RAW) for oscillator based timing for best real time results

# run logic, treat everything as segment. and only trip if it is a new lap
# probably run at 100hz if the main runs at 50hz(given gps only updates at 10hz)

debug = False


class OmeTimer():
    def __init__(self):
        self.lap_start_time = 0  # start time of the lap
        self.seg_start_time = 0  # start time of the segment
        self.current_elap_lap_time = 0  # elapsed time for current lap
        self.current_elap_seg_time = 0  # elapsed time for current lap
        self.last_seg_time = 0  # previous segment time
        self.last_lap_time = 0  # previous lap time

    # to do. maybe combine the 2 timer to a thread for running continuously. Then only call to return value
    
    def StartTimer(self):
        pass

    def ElapsedSegTime(self, _time_now=time.clock_gettime(time.CLOCK_MONOTONIC_RAW)):
        if debug:
            print(_time_now)
        self.current_elap_seg_time = _time_now - self.seg_start_time
        self.current_elap_lap_time = _time_now - self.lap_start_time
        return [self.current_elap_seg_time, self.current_elap_lap_time]

    def NewSegment(self, _time_now=time.clock_gettime(time.CLOCK_MONOTONIC_RAW), _new_lap=False):
        if debug:
            print(_time_now)
        # run time recording right before cut out
        self.ElapsedSegTime(_time_now)
        # copy the time over and set up new seg/lap start time
        self.last_seg_time = self.current_elap_seg_time
        self.seg_start_time = _time_now
        if _new_lap:
            self.last_lap_time = self.current_elap_lap_time
            self.lap_start_time = _time_now
        # no return. the main will call seg time or lap time accordingly to grab them

    @property
    def GetAllTimes(self):
        # return all 4 run time items
        return [self.current_elap_lap_time, self.current_elap_seg_time, self.last_lap_time, self.last_seg_time]
    
    def reset(self):
        self.lap_start_time = 0  
        self.seg_start_time = 0  
        self.current_elap_lap_time = 0 
        self.current_elap_seg_time = 0  
        self.last_seg_time = 0 
        self.last_lap_time = 0  




a = OmeTimer()
run_amount = 1000000
print(timeit.timeit(setup=a.ElapsedSegTime, number=run_amount)/run_amount)
