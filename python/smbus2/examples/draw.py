# -*- coding: utf-8 -*-


import sys
import time
import tkinter as tk
import threading
import logging

sys.path.append("..")
from dfrobot_huskylensv2 import *

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,                # logging level：DEBUG/INFO/WARNING/ERROR
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class ProtocolThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.husky = HuskylensV2_UART(tty_name="/dev/ttyAMA0", baudrate=115200,debug_level=logging.INFO)
    def run(self):
        self.husky.knock()
        ret = self.husky.switchAlgorithm(ALGORITHM_FACE_RECOGNITION)
        logging.info(f"husky.switchAlgorithm(ALGORITHM_FACE_RECOGNITION)={ret}")
        time.sleep(5)
        ret = self.husky.drawText(0x0000FF, 24, 10, 10, "Hello Huskylens!")
        logging.info(f"husky.drawText(0x0000FF, 24, 10, 10, 'Hello Huskylens!')={ret}")
        time.sleep(5)
        ret = self.husky.clearText()
        logging.info(f"husky.clearText()={ret}")
        time.sleep(5)
        
        while True:
            ret = self.husky.drawText(COLOR_RED, 20, 10, 10, "DFRobot Test")
            logging.info(f"husky.drawText(COLOR_RED, 20, 10, 10, 'DFRobot Test')={ret}")
            time.sleep(2)
            
            ret = self.husky.clearText()
            logging.info(f"husky.clearText()={ret}")
            time.sleep(2)
        
            ret = self.husky.drawRect(COLOR_GREEN, 4, 10, 10, 200, 30)
            logging.info(f"husky.drawRect(COLOR_GREEN, 4, 10, 10, 200, 30)={ret}")
            time.sleep(2)
            
            ret = self.husky.clearRect()
            logging.info(f"husky.clearRect()={ret}")
            time.sleep(2)
        
            for i in range(150):
                ret = self.husky.drawUniqueRect(COLOR_GREEN, 4, 50, 50, 102 + i * 2, 102 + i * 2)
                time.sleep(0.005)
            time.sleep(5)

ProtocolThread().start()
while True:
    time.sleep(1)
