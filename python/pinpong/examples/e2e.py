# -*- coding: utf-8 -*-

import logging
import os
import random
import sys
import time
from pinpong.board import Board

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dfrobot_huskylensv2 import *

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,                # 日志级别：DEBUG/INFO/WARNING/ERROR
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BOARD_TYPE = "UNIHIKER"
TTY_NAME = "/dev/ttySP0"
BAUDRATE = 115200
ANNOTATION_COUNT = 10
ANNOTATION_INTERVAL = 0.5


def build_annotation(start_time):
    timestamp_ms = int((time.monotonic() - start_time) * 1000)
    sensor_data = [random.randint(0, 999) for _ in range(3)]
    annotation = "{},{},{},{}".format(timestamp_ms, *sensor_data)
    return timestamp_ms, sensor_data, annotation


def main():
    Board(BOARD_TYPE).begin()  # 初始化

    husky = HuskylensV2_UART(
        tty_name=TTY_NAME,
        baudrate=BAUDRATE,
        debug_level=logging.INFO,
    )

    logging.info("[E2E] Waiting for HUSKYLENS V2...")
    while not husky.knock():
        logging.warning("[E2E] Device not ready, retrying...")
        time.sleep(3)

    logging.info("[E2E] Start recording...")
    ret = husky.e2eStartRecording()
    if not ret:
        logging.error("[E2E] Start recording failed")
        return

    logging.info("[E2E] Recording started")
    start_time = time.monotonic()

    try:
        for index in range(ANNOTATION_COUNT):
            timestamp_ms, sensor_data, annotation = build_annotation(start_time)
            ret = husky.e2eSendAnnotation(annotation)

            logging.info(
                '[E2E] Annotation %d/%d %s: time=%d, data=%s, payload="%s"',
                index + 1,
                ANNOTATION_COUNT,
                "sent" if ret else "failed",
                timestamp_ms,
                sensor_data,
                annotation,
            )
            time.sleep(ANNOTATION_INTERVAL)
    finally:
        ret = husky.e2eStopRecording()
        logging.info("[E2E] Stop recording %s", "success" if ret else "failed")


if __name__ == "__main__":
    main()
