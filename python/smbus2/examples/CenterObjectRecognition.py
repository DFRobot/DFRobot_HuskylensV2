'''!
  @file CenterObjectRecognition.py
  @brief Sample code for obtaining information about objects near the center

'''


import sys
import os
sys.path.append("../")
from dfrobot_huskylensv2 import *


huskylens = HuskylensV2_I2C() #Comment this line to disable I2C mode
#huskylens = HuskylensV2_UART(tty_name="/dev/ttyAMA0", baudrate=115200) #Uncomment this line to use UART mode
huskylens.knock()
huskylens.switchAlgorithm(ALGORITHM_OBJECT_RECOGNITION)

while True:
    huskylens.getResult(ALGORITHM_OBJECT_RECOGNITION)
    if  (huskylens.available(ALGORITHM_OBJECT_RECOGNITION)):
        print(str("ID: ") + str(huskylens.getCachedCenterResult(ALGORITHM_OBJECT_RECOGNITION).ID))
        print(str("Name: ") + str(huskylens.getCachedCenterResult(ALGORITHM_OBJECT_RECOGNITION).name))
        print(str("xCenter: ") + str(huskylens.getCachedCenterResult(ALGORITHM_OBJECT_RECOGNITION).xCenter))
        print(str("yCenter: ") + str(huskylens.getCachedCenterResult(ALGORITHM_OBJECT_RECOGNITION).yCenter))
        print(str("Width: ") + str(huskylens.getCachedCenterResult(ALGORITHM_OBJECT_RECOGNITION).width))
        print(str("Height: ") + str(huskylens.getCachedCenterResult(ALGORITHM_OBJECT_RECOGNITION).height))
    time.sleep(0.1)