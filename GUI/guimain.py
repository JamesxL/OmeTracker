from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
import sys
import time

from OmeTrackerUI1 import Ui_MainWindow

class MainWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

        self.StopTimer.clicked.connect(QCoreApplication.instance().quit)
        self.StartTimer.clicked.connect(self.additems)
        

        self.show()
        

    def add_LapRecord(self, value):
        self.LapRecord.sortItems(order=Qt.AscendingOrder)
        self.LapRecord.insertItem(0,value)
        #time.sleep(1)

    def additems(self):
        for i in range(28):
            self.add_LapRecord(str(i))






app = QApplication(sys.argv)
mainWin = MainWindow()

app.exit(app.exec_())