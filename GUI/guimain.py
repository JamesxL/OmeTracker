from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
import sys

from OmeTrackerUI1 import Ui_MainWindow

class MainWindow(QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

        self.StartTimer.clicked.connect(QCoreApplication.instance().quit)
        
        self.show()
        

        
        

app = QApplication(sys.argv)
mainWin = MainWindow()

app.exit(app.exec_())