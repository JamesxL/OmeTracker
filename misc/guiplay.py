import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer, QTime, Qt
import time, datetime
from threading import Thread
from random import seed
from random import randint
  
class Window(QWidget):
  
    def __init__(self):
        super().__init__()
        seed(1)
  
        # setting geometry of main window
        self.setGeometry(100, 100, 800, 400)
  
        # creating a vertical layout
        layout = QVBoxLayout()
  
        # creating font object
        font = QFont('Arial', 120, QFont.Bold)
  
        # creating a label object
        self.label = QLabel()
  
        # setting centre alignment to the label
        self.label.setAlignment(Qt.AlignCenter)
  
        # setting font to the label
        self.label.setFont(font)
  
        # adding label to the layout
        layout.addWidget(self.label)
  
        # setting the layout to main window
        self.setLayout(layout)
  
        # creating a timer object
        timer = QTimer(self)
        timer2 = QTimer(self)
  
        # adding action to timer
        timer.timeout.connect(self.showTime)
        timer2.timeout.connect(self.setcolor)
  
        # update the timer every second
        timer.start(10)
        timer2.start(1000)
        self.startime = time.time()
        #self.xyz = timer2.time()

        
  
    # method called by timer
    def showTime(self):
  
        # getting current time
        current_time = time.time() - self.startime
  
        # converting QTime object to string
        label_time = str(datetime.timedelta(seconds = current_time))[:-3]#.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
    
  
        # showing it to the label
        self.label.setText(label_time)

    def setcolor(self):
        a = randint(50, 120)
        font = QFont('Arial', a, QFont.Bold)
        self.label.setFont(font)



  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# showing all the widgets
window.show()
  
# start the app
print('xx')

App.exit(App.exec_())