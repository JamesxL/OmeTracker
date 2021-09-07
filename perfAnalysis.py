#from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%matplotlib inline


def analyze1(filename):
    df = pd.read_csv(filename)
    #print(df)

    
    #ax = plt.axes(projection='3d')

    plt.figure(figsize=(20,15))
    # Data for a three-dimensional line
    """zline = np.linspace(0, 15, 1000)
    xline = np.sin(zline)
    yline = np.cos(zline)
    ax.plot3D(xline, yline, zline, 'gray')"""

    # Data for three-dimensional scattered points

    #ax.scatter3D(df.longitude, df.latitude, df.groundspeed)
    xf = df[(df.lap==1)&(df.session==1)]
    #print(xf.lap_time.max())
    
    print(df.groupby(['session','lap']).lap_time.max())
    #print(xf)
    plt.scatter(df.longitude, df.latitude, c = df.groundspeed, cmap = 'jet',s=0.5,vmin=0,vmax=200)
    cbar = plt.colorbar()
    cbar.solids.set_edgecolor("face")


    plt.show()


def TrapALine(coordFin1, coordFin2, coordCar):
    _fin_fin_vec = [coordFin1[0] - coordFin2[0],
                    coordFin1[1] - coordFin2[1]]
    _fin_len = np.linalg.norm(_fin_fin_vec)
    _fin_car_vec = [coordCar[0] - coordFin2[0],
                    coordCar[1] - coordFin2[1]]
    _fin_car_dist = np.linalg.norm(_fin_car_vec)
    _fin_car_od = np.cross(_fin_fin_vec, _fin_car_vec)/_fin_len
    trapped = False
    if abs(_fin_car_dist) < abs(_fin_len):
        TrapALine.new_state = _fin_car_od/abs(_fin_car_od)
        if TrapALine.last_state + TrapALine.new_state == 0:
            #('cross the line')
            trapped = True
        TrapALine.last_state = TrapALine.new_state
    else:
        TrapALine.last_state = 0
    #print(_fin_len, _fin_car_dist, _fin_car_od, TrapALine.new_state, TrapALine.last_state)
    return trapped


TrapALine.new_state = 0
TrapALine.last_state = 0    

coor1=[39.53845951912364, -122.3313076822977]
coor2=[39.53846986168637, -122.33106896571067]


def count_time(file):
    lap = 0
    start_time = 0
    df = pd.read_csv(file)
    #print(df)
    for index, arow in df.iterrows():
        car= [ arow.latitude,arow.longitude]
        #print(car)
        if TrapALine(coor1,coor2,car):
            lap = lap+1
            start_time = arow.global_time
            print(f'pass a line at {arow.lap_time}')            
        df.at[index,'lap']=lap
        df.at[index,'lap_time'] = arow.global_time - start_time
    df.to_csv(f'timed_{file}')

def combine(alist):
    df = pd.read_csv(alist[0])
    session = 1
    df['session'] = session
    for i in range(len(alist)-1):
        xf = pd.read_csv(alist[i+1])
        session = session+1
        xf['session'] = session
        df = df.append(xf)
    df.to_csv('summary.txt',index=False)

#combine(['timed_session1.txt','timed_session2.txt','timed_session3.txt','timed_session4.txt'])

#count_time('session1.txt')


analyze1('summary.txt')