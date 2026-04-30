# -*- coding: utf-8 -*-

import os
import sys
import time
import tkinter as tk
import threading
import sys
import logging

sys.path.append("..")
from dfrobot_huskylensv2 import *

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,                # logging level：DEBUG/INFO/WARNING/ERROR
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)



def main():
    husky = HuskylensV2_UART(tty_name="/dev/ttyAMA0",baudrate=115200, debug_level=logging.INFO)
    while not husky.knock():
        time.sleep(3)
    husky.switchAlgorithm(ALGORITHM_GAZE_RECOGNITION)
    time.sleep(5)
    
    while True:
        ret = husky.getResult(ALGORITHM_GAZE_RECOGNITION)
        logging.info(f"husky.getResult(ALGORITHM_GAZE_RECOGNITION)={ret}");

        while husky.available(ALGORITHM_GAZE_RECOGNITION):
            result = husky.popCachedResult(ALGORITHM_GAZE_RECOGNITION)
            if result:
                print("result.name=",result.name)
                print(f"result.pitch={result.pitch}")
                print(f"result.yaw={result.yaw}")
                print(f"result.azimuth={result.azimuth}")
            else:
                print(None)
            time.sleep(1)

if __name__ == "__main__":
    main()
