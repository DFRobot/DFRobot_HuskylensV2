'''!
  @file ObjectRecognitionNo_X.py
  @brief Sample code for obtaining information about objects ID.X(ID.0)
  @If multiple targets are detected simultaneously, 
  @you can modify the parameters of getCachedResultByID() to adjust which target is printed.
  

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
    if  ((huskylens.getCachedResultByID(ALGORITHM_OBJECT_RECOGNITION, 1) is not None)):
        print(str("Name: ") + str(huskylens.getCachedResultByID(ALGORITHM_OBJECT_RECOGNITION,1).name))
        print(str("xCenter: ") + str(huskylens.getCachedResultByID(ALGORITHM_OBJECT_RECOGNITION,1).xCenter))
        print(str("yCenter: ") + str(huskylens.getCachedResultByID(ALGORITHM_OBJECT_RECOGNITION,1).yCenter))
        print(str("Width: ") + str(huskylens.getCachedResultByID(ALGORITHM_OBJECT_RECOGNITION,1).width))
        print(str("Height: ") + str(huskylens.getCachedResultByID(ALGORITHM_OBJECT_RECOGNITION,1).height))
    time.sleep(0.1)