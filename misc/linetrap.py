import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

from matplotlib import style
import numpy as np
import time

'''
prototyping the line trap algo
example the finish line is (0.9,0),(1.1,0)
the track is circle centered at (0,0) with radius of 1
the trap should successfully trap when the dot moves across between finish line

best way is probably using dot product to project moving point to finish line, changing sign = crossing the line, magnitude of the vector is if the vehicle is between or beyond the line 
'''


"""class traps:
    def __init__(self):
        self.last_state = 0
        self.new_state = 0

    def TrapALine(self, coordFin1, coordFin2, coordCar):
        _fin_fin_vec = [coordFin1[0] - coordFin2[0],
                        coordFin1[1] - coordFin2[1]]
        _fin_len = np.linalg.norm(_fin_fin_vec)
        _fin_car_vec = [coordCar[0] - coordFin2[0],
                        coordCar[1] - coordFin2[1]]
        _fin_car_dist = np.linalg.norm(_fin_car_vec)
        _fin_car_od = np.cross(_fin_fin_vec, _fin_car_vec)/_fin_len
        
        if abs(_fin_car_dist) < abs(_fin_len):
            self.new_state = _fin_car_od/abs(_fin_car_od)
            if self.last_state + self.new_state == 0:
                print('cross the line')
            self.last_state = self.new_state
        else:
            self.last_state = 0
        print(_fin_len, _fin_car_dist, _fin_car_od,
              self.new_state, self.last_state)
"""

def TrapALine(coordFin1, coordFin2, coordCar):
        _fin_fin_vec = [coordFin1[0] - coordFin2[0],
                        coordFin1[1] - coordFin2[1]]
        _fin_len = np.linalg.norm(_fin_fin_vec)
        _fin_car_vec = [coordCar[0] - coordFin2[0],
                        coordCar[1] - coordFin2[1]]
        _fin_car_dist = np.linalg.norm(_fin_car_vec)
        _fin_car_od = np.cross(_fin_fin_vec, _fin_car_vec)/_fin_len
        
        if abs(_fin_car_dist) < abs(_fin_len):
            TrapALine.new_state = _fin_car_od/abs(_fin_car_od)
            if TrapALine.last_state  + TrapALine.new_state == 0:
                print('cross the line')
                return True
            TrapALine.last_state  = TrapALine.new_state
        else:
            TrapALine.last_state  = 0
        print(_fin_len, _fin_car_dist, _fin_car_od,
              TrapALine.new_state, last_state)
        return False
TrapALine.new_state = 0
TrapALine.last_state = 0

# style.use('fivethirtyeight')
fig, ax = plt.subplots(figsize=(15, 15))
plt.axis([-1.5, 1.5, -1.5, 1.5])


t = 0
w = -5  # omega
alpha = 3.14/6  # initial location at -90 deg loc

x1 = 0.9
y1 = 0
x2 = 1.1
y2 = 0

vec_fin_line = [x2-x1, y2-y1]

ax.plot([x1, x2], [y1, y2], marker='o')
ax2 = ax.twinx()
plt.axis([-1.5, 1.5, -1.5, 1.5])


last_state = 0
new_state = 0




#trap = traps()

while True:
    _vehicle_coord = [np.cos(w*t+alpha), np.sin(w*t+alpha)]
    t = t+0.01
    TrapALine([x1, y1], [x2, y2], _vehicle_coord)
    """
    dist_car, dist_fin, car_len = distcalc([x1, y1], [x2, y2], _vehicle_coord)
    if abs(car_len) < abs(dist_fin):
        new_state = dist_car/abs(dist_car)
        if last_state + new_state == 0:
            print('cross the line')
        last_state = new_state
    else:
        last_state = 0"""

    # print(_vehicle_coord)
    points = plt.scatter(_vehicle_coord[0], _vehicle_coord[1])
    # time.sleep(0.01)
    # plt.draw()
    plt.pause(0.001)
    # plt.cla()
    points.remove()

"""
plt.show()"""
"""
plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

print('here')
plt.show()"""

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')



def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True,interval=10)
plt.show()
"""
