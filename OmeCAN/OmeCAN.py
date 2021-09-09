import can
import cantools
import os
import datetime
import threading


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

debug = False
DEFAULT_LOG_PATH = os.path.expanduser(f'~/workspace/logs')

def PRINTDEBUG(text, override=False):
    if debug | override:
        print(text)



class OmeCAN:
        
    def __init__(self, canport = 'can0', dbc_path = '', log_folder = DEFAULT_LOG_PATH):
        self.log_folder = log_folder
        self.dbc_path = dbc_path
        self.canport = canport
        self.log_file = ''

        self.CAN_parse = False
        self.CAN_log = False
        self.CAN_connected = False
        if self.dbc_path != '':
            self.db = cantools.database.load_file(self.dbc_path)
            self.CAN_parse = True

        try:
            self.CAN_bus = can.ThreadSafeBus('can0')
            self.CAN_connected = True
        except Exception as e:
            self.CAN_connected = False
            PRINTDEBUG(e, True)


        self.logger = ''
        
        self.vehicle_status = dict()
        self.CAN_thread = threading.Thread(target=self.CAN_receiver, daemon=True)
        self.stop_thread = threading.Event()
        self.CAN_thread.start()
        
    def CAN_parser(self,_msg):
        if self.CAN_parse:
            self.vehicle_status.update(self.db.decode_message(_msg.arbitration_id, _msg.data))
        
    
    def set_new_log(self, runName = 'default'):
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]
        self.log_file = f'{self.log_folder}/{_tmp_time}_{runName}_CAN.asc'
        self.logger = can.Logger(self.log_file)

    def start_new_log(self):
        self.CAN_log = True

    def stop_new_log(self):
        self.CAN_log = False
    
        
    def CAN_receiver(self):
        #only allow to try receiving CAN when there is one connected
        while self.CAN_connected:
            try:
                _msg = self.CAN_bus.recv(1)
            except Exception as e:
                print(e)
            if self.CAN_parse:
                self.CAN_parser(_msg)
            if self.CAN_log:
                self.logger(_msg)
    @ property
    def get_vehicle_status(self):
        return self.vehicle_status
    
    


        