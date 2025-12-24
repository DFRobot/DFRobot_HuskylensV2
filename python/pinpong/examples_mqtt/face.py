# -*- coding: utf-8 -*-

#实验效果：学习一次ID
#接线：使用windows或linux电脑连接一块树，树莓派主控板，哈士奇接到I2C口SCL SDA
import os
import time
import tkinter as tk
from pinpong.board import Board
from pinpong.libs.dfrobot_huskylensv2 import *
import threading
import sys
import logging
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,                # 日志级别：DEBUG/INFO/WARNING/ERROR
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
Board("UNIHIKER").begin()  #初始化

# 创建主窗口
root = tk.Tk()
root.title("面部特征绘制")
root.geometry("640x480")  # 设置窗口大小
# 创建画布
canvas = tk.Canvas(root, width=640, height=480, bg='white')
canvas.pack()


def draw_result(result):
    """在UI线程里绘制"""
    if result:
        # 绘制面部方框
        canvas.create_rectangle(
            result.xCenter - result.width / 2, result.yCenter - result.height / 2,
            result.xCenter + result.width / 2, result.yCenter + result.height / 2,
            outline='blue', width=2
        )

        # 左眼
        canvas.create_oval(
            result.leye_x - 5, result.leye_y - 5,
            result.leye_x + 5, result.leye_y + 5,
            fill='green', outline='green'
        )

        # 右眼
        canvas.create_oval(
            result.reye_x - 5, result.reye_y - 5,
            result.reye_x + 5, result.reye_y + 5,
            fill='green', outline='green'
        )

        # 鼻子
        canvas.create_oval(
            result.nose_x - 5, result.nose_y - 5,
            result.nose_x + 5, result.nose_y + 5,
            fill='red', outline='red'
        )

        # 嘴巴
        canvas.create_line(
            result.lmouth_x, result.lmouth_y,
            result.rmouth_x, result.rmouth_y,
            fill='red', width=2
        )

        # 标签
        canvas.create_text(result.leye_x, result.leye_y - 15, text="L-Eye", fill="black")
        canvas.create_text(result.reye_x, result.reye_y - 15, text="R-Eye", fill="black")
        canvas.create_text(result.nose_x, result.nose_y - 15, text="Nose", fill="black")
        canvas.create_text(
            (result.lmouth_x + result.rmouth_x) / 2,
            (result.lmouth_y + result.rmouth_y) / 2 - 15,
            text="Mouth", fill="black"
        )
    else:
        canvas.delete("all")
        #canvas.create_text(320, 240, text="No face detected", fill="gray")

class ProtocolThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        while True:
            husky = HuskylensV2_UART(tty_name="/dev/ttySP0",baudrate=115200, debug_level=logging.INFO)
            while not husky.knock():
                time.sleep(3)
            husky.switchAlgorithm(ALGORITHM_FACE_RECOGNITION)
            while True:
                husky.getResult(ALGORITHM_FACE_RECOGNITION)
                root.after(0, draw_result, None)
                while husky.available(ALGORITHM_FACE_RECOGNITION):
                    result = husky.popCachedResult(ALGORITHM_FACE_RECOGNITION)
                    if result:
                        print("result.name=",result.name)
                        print(f"result.Center={result.xCenter,result.yCenter}")
                        print(f"result.leye=({result.leye_x,result.leye_y})")
                    else:
                        print(None)
                    root.after(0, draw_result, result)

ProtocolThread().start()
root.mainloop()
