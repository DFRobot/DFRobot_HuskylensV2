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
        self.husky = HuskylensV2_UART(tty_name="/dev/ttyAMA0", baudrate=115200)
    def run(self):
        while not self.husky.knock():
            time.sleep(0.5)
        while True:
            ret = self.husky.takeScreenshot()
            logging.info(f"takeScreenshotret={ret}")
            time.sleep(5)


ProtocolThread().start()
while True:
    time.sleep(1)