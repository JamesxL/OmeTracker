# TrackLogger
DIY Track Logger

#Critical Coding Rules:
1. Class names should normally use the CapWords convention.
2. Function names should be lowercase, with words separated by underscores as necessary to improve readability.
3. Variable names follow the same convention as function names.
4. Use one leading underscore only for non-public methods and instance variables.
5. Constants are usually defined on a module level and written in all capital letters with underscores separating words. Examples include MAX_OVERFLOW and TOTAL.



# List of Dependencies
## apt install ones
. python3-can, python3-serial

apt-get install python3-pyside2.qt3dcore python3-pyside2.qt3dinput python3-pyside2.qt3dlogic python3-pyside2.qt3drender python3-pyside2.qtcharts python3-pyside2.qtconcurrent python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qthelp python3-pyside2.qtlocation python3-pyside2.qtmultimedia python3-pyside2.qtmultimediawidgets python3-pyside2.qtnetwork python3-pyside2.qtopengl python3-pyside2.qtpositioning python3-pyside2.qtprintsupport python3-pyside2.qtqml python3-pyside2.qtquick python3-pyside2.qtquickwidgets python3-pyside2.qtscript python3-pyside2.qtscripttools python3-pyside2.qtsensors python3-pyside2.qtsql python3-pyside2.qtsvg python3-pyside2.qttest python3-pyside2.qttexttospeech python3-pyside2.qtuitools python3-pyside2.qtwebchannel python3-pyside2.qtwebsockets python3-pyside2.qtwidgets python3-pyside2.qtx11extras python3-pyside2.qtxml python3-pyside2.qtxmlpatterns python3-pyside2uic

## pip install ones
pip3 install cantools, pynmea2, sense_emu, sense_hat, pyyaml, pyubx2



pyside2 adjustment in raspberry pi
sudo vim /usr/bin/pyside2-uic
change python2 to python3



# Raspberry Pi Setups
1. Setup CAN interface sudo /sbin/ip link set can0 up type can bitrate 500000 (change 500000 to busrate of your vehicle if different)
2. qt5ct has some conflict wit pyside. do apt purge qt5ct to get rid of it for proper color scheming. 

something about setting up autostart
mkdir /home/pi/.config/lxsession
mkdir /home/pi/.config/lxsession/LXDE-pi
cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/
nano /home/pi/.config/lxsession/LXDE-pi/autostart
@lxterminal -e python3 /path/my_script.py



# Thought dump
1. try 18hz GPS instead of 10hz GPS+GLO if it achieves same accuracy
2. move to UBX_binary mode, it will be fixed byte and 1 single UBX-NAV-PVT message will have all needed info