'''!
  @file ObjectRecognitionNo_X.py
  @brief Sample code for obtaining information about objects No.X(No.0) of ID X(ID 1)
  @If multiple targets are detected simultaneously, 
  @you can modify the parameters of getCachedIndexResultByID() to adjust which target is printed.

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
        print(str("Name: ") + str(huskylens.getCachedIndexResultByID(ALGORITHM_OBJECT_RECOGNITION,1,0).name))
        print(str("xCenter: ") + str(huskylens.getCachedIndexResultByID(ALGORITHM_OBJECT_RECOGNITION,1,0).xCenter))
        print(str("yCenter: ") + str(huskylens.getCachedIndexResultByID(ALGORITHM_OBJECT_RECOGNITION,1,0).yCenter))
        print(str("Width: ") + str(huskylens.getCachedIndexResultByID(ALGORITHM_OBJECT_RECOGNITION,1,0).width))
        print(str("Height: ") + str(huskylens.getCachedIndexResultByID(ALGORITHM_OBJECT_RECOGNITION,1,0).height))
    time.sleep(0.1)