import can
import cantools
import os
import datetime
import threading

class OmeCAN():
    
    dbc_path = ''
    logFolder = os.path.expanduser(f'~/workspace/logs')
    
    
    def __init__(self):
        
        self.canParse = False
        self.canLog = False
        if self.dbc_path != '':
            self.db = cantools.database.load_file(self.dbc_path)
            self.canParse = True
        self.canBus = can.ThreadSafeBus('can0')
        self.logger = ''
        
        self.vehicleStatus = dict()
        self.stopThread = threading.Event()
        
    def canParser(self,_msg):
        if self.canParse:
            self.vehicleStatus.update(self.db.decode_message(_msg.arbitration_id, _msg.data))
        
    
    def newLog(self, runName = 'default'):
        _tmp_time = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S-%f')[:-3]
        self.logFile = f'{self.logFolder}/{_tmp_time}_{runName}_CAN.asc'
        self.logger = can.Logger(self.logFile)
        self.canLog = True
    
    def stopLog(self):
        self.canLog = False
        
    def receiveCAN(self):
        while True:
            _msg = self.canBus.recv(1)
            if self.canParse:
                self.canParser(_msg)
            if self.canLog:
                self.logger(_msg)
    @ property
    def getVehicleStatus(self):
        return self.vehicleStatus
    
    


        