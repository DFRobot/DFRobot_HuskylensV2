'''!
  @file ObjectRecognitionNo_X.py
  @brief Sample code for obtaining information about objects ID.X(ID.0)
  @If multiple targets are detected simultaneously, 
  @you can modify the parameters of getCachedResultByID() to adjust which target is printed.
  
'''
import sys


sys.path.append("../")
from dfrobot_huskylensv2 import *



huskylens = HuskylensV2_I2C() #Comment this line to disable I2C mode
#huskylens = HuskylensV2_UART(tty_name="/dev/ttyAMA0", baudrate=115200) #Uncomment this line to use UART mode
huskylens.knock()
huskylens.switchAlgorithm(ALGORITHM_OBJECT_RECOGNITION)

while True:
    huskylens.getResult(ALGORITHM_OBJECT_RECOGNITION)
    if  (huskylens.available(ALGORITHM_FACE_RECOGNITION)):
        print(str("ID: ") + str(huskylens.getCachedResultByIndex(ALGORITHM_OBJECT_RECOGNITION,0).ID))
        print(str("Name: ") + str(huskylens.getCachedResultByIndex(ALGORITHM_OBJECT_RECOGNITION,0).name))
        print(str("xCenter: ") + str(huskylens.getCachedResultByIndex(ALGORITHM_OBJECT_RECOGNITION,0).xCenter))
        print(str("yCenter: ") + str(huskylens.getCachedResultByIndex(ALGORITHM_OBJECT_RECOGNITION,0).yCenter))
        print(str("Width: ") + str(huskylens.getCachedResultByIndex(ALGORITHM_OBJECT_RECOGNITION,0).width))
        print(str("Height: ") + str(huskylens.getCachedResultByIndex(ALGORITHM_OBJECT_RECOGNITION,0).height))
    time.sleep(0.1)