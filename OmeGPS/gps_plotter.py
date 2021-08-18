import pynmea2
import os


overrideflag = 1

log_file = os.path.expanduser(f'~/workspace/logs/logs/2021-08-16_03-17-14-421.log')

log = open(log_file)
content = log.readlines()

if overrideflag:
    fixed = os.path.expanduser(f'~/workspace/logs/logs/2021-08-16_03-17-14-421_f.log')
    fx = open(fixed, 'w')


for a_line in content:
    _temp = a_line.split(', ')
    _time = _temp[0]
    try:
        _inc = _temp[1].lstrip('b').replace("'","").replace(r'\r\n', '').strip()
        if overrideflag:
            fx.write(f'{_inc}\r\n')
    except:
        print('somethingwrong')
        print(_temp[0])
    #print(type(_inc))
    try:
        _msg = pynmea2.parse(_inc)
        #print(_time)
        #print(repr(_msg))
        #if 'GGA' in _inc:
            #print(_msg.latitude)


    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
