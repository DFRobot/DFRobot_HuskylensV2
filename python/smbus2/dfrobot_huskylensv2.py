# -*- coding: utf-8 -*-

import time
import ctypes
import queue
import math
import struct
import logging
import smbus2
from smbus2 import i2c_msg
import serial

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LCD_WIDTH = 640
LCD_HEIGHT = 480

RESOLUTION_DEFAULT = 0
RESOLUTION_640x480 = 1
RESOLUTION_1280x720 = 2
RESOLUTION_1920x1080 = 3

MEDIA_TYPE_AUDIO = 1
MEDIA_TYPE_VIDEO = 2

COLOR_WHITE = 0xFFFFFF   # 白色
COLOR_RED = 0xFF0000     # 红色
COLOR_ORANGE = 0xFFA500  # 橙色
COLOR_YELLOW = 0xFFFF00  # 黄色
COLOR_GREEN = 0x00FF00   # 绿色
COLOR_CYAN = 0x00FFFF    # 青色
COLOR_BLUE = 0x0000FF    # 蓝色
COLOR_PURPLE = 0x800080  # 紫色
COLOR_PINK = 0xFFC0CB    # 粉色
COLOR_GRAY = 0x808080    # 灰色
COLOR_BLACK = 0x000000   # 黑色
COLOR_BROWN = 0xA52A2A   # 棕色
COLOR_OLIVE = 0x808000   # 橄榄绿
COLOR_TEAL = 0x008080    # 蓝绿色
COLOR_INDIGO = 0x4B0082  # 靛蓝色
COLOR_MAGENTA = 0xFF00FF # 洋红色

HEADER_0_INDEX = 0
HEADER_1_INDEX = 1
COMMAND_INDEX = 2
ALGO_INDEX = 3
CONTENT_SIZE_INDEX = 4
CONTENT_INDEX = 5
PROTOCOL_SIZE = 6

COMMAND_KNOCK = 0x00
COMMAND_GET_RESULT = 0x01
COMMAND_GET_ALGO_PARAM = 0x02
COMMAND_GET_RESULT_BY_ID = 0x03
COMMAND_GET_BLOCKS_BY_ID = 0x04
COMMAND_GET_ARROWS_BY_ID = 0x05

COMMAND_SET_ALGORITHM = 0x0A
COMMAND_SET_NAME_BY_ID = 0x0B
COMMAND_SET_MULTI_ALGORITHM = 0x0C
COMMAND_SET_MULTI_ALGORITHM_RATIO = 0x0D
COMMAND_SET_ALGO_PARAMS = 0x0E
COMMAND_UPDATE_ALGORITHM_PARAMS = 0x0F

COMMAND_RETURN_ARGS = 0x1A
COMMAND_RETURN_INFO = 0x1B
COMMAND_RETURN_BLOCK = 0x1C
COMMAND_RETURN_ARROW = 0x1D

COMMAND_ACTION_TAKE_PHOTO = 0x20
COMMAND_ACTION_TAKE_SCREENSHOT = 0x21
COMMAND_ACTION_LEARN = 0x22
COMMAND_ACTION_FORGET = 0x23
COMMAND_ACTION_SAVE_KNOWLEDGES = 0x24
COMMAND_ACTION_LOAD_KNOWLEDGES = 0x25
COMMAND_ACTION_DRAW_RECT = 0x26
COMMAND_ACTION_CLEAN_RECT = 0x27
COMMAND_ACTION_DRAW_TEXT = 0x28
COMMAND_ACTION_CLEAR_TEXT = 0x29
COMMAND_ACTION_PLAY_MUSIC = 0x2A
COMMAND_EXIT = 0x2B
COMMAND_ACTION_LEARN_BLOCK = 0x2C
COMMAND_ACTION_DRAW_UNIQUE_RECT = 0x2D
COMMAND_ACTION_START_RECORDING  = 0x2E
COMMAND_ACTION_STOP_RECORDING   = 0x2F

COMMAND_ACTION_E2E_START_RECORDING  = 0x30
COMMAND_ACTION_E2E_STOP_RECORDING   = 0x31
COMMAND_ACTION_E2E_SEND_ANNOTATION  = 0x32

ALGORITHM_ANY = 0
ALGORITHM_FACE_RECOGNITION = 1
ALGORITHM_OBJECT_RECOGNITION = 2
ALGORITHM_OBJECT_TRACKING = 3
ALGORITHM_COLOR_RECOGNITION = 4
ALGORITHM_OBJECT_CLASSIFICATION = 5
ALGORITHM_SELF_LEARNING_CLASSIFICATION = 6
ALGORITHM_SEGMENT = 7
ALGORITHM_HAND_RECOGNITION = 8
ALGORITHM_POSE_RECOGNITION = 9
ALGORITHM_LICENSE_RECOGNITION = 10
ALGORITHM_OCR_RECOGNITION = 11
ALGORITHM_LINE_TRACKING = 12
ALGORITHM_EMOTION_RECOGNITION = 13
ALGORITHM_GAZE_RECOGNITION = 14
ALGORITHM_FACE_ORIENTATION = 15
ALGORITHM_TAG_RECOGNITION = 16
ALGORITHM_BARCODE_RECOGNITION = 17
ALGORITHM_QRCODE_RECOGNITION = 18
ALGORITHM_FALLDOWN_RECOGNITION = 19
ALGORITHM_BUILTIN_RFU0 = 20
ALGORITHM_BUILTIN_RFU1 = 21
ALGORITHM_BUILTIN_RFU2 = 22
ALGORITHM_BUILTIN_RFU3 = 23
ALGORITHM_BUILTIN_RFU4 = 24
ALGORITHM_CUSTOM0 = 25
ALGORITHM_CUSTOM1 = 26
ALGORITHM_CUSTOM2 = 27

ALGORITHM_CUSTOM_BEGIN = 128

MULTI_ALGORITHM_MAX_COUNT = 3

class UnionInt8_0(ctypes.Union):
    _fields_ = [
        ("ID", ctypes.c_int8),
        ("maxID", ctypes.c_int8),
        ("rfu0", ctypes.c_int8),
        ("boardType", ctypes.c_int8),
        ("multiAlgoNum", ctypes.c_int8),
    ]

class UnionInt8_1(ctypes.Union):
    _fields_ = [
        ("rfu1", ctypes.c_int8),
        ("level", ctypes.c_int8),
        ("retValue", ctypes.c_int8),
        ("lineWidth", ctypes.c_int8),
        ("confidence", ctypes.c_int8),
    ]

class UnionInt16_0(ctypes.Union):
    _fields_ = [
        ("first", ctypes.c_int16),
        ("xCenter", ctypes.c_int16),
        ("xTarget", ctypes.c_int16),
        ("duration", ctypes.c_int16),
        ("algorithmType", ctypes.c_int16),
        ("classID", ctypes.c_int16),
        ("total_results", ctypes.c_int16),
        ("pitch", ctypes.c_int16),
    ]

class UnionInt16_1(ctypes.Union):
    _fields_ = [
        ("second", ctypes.c_int16),
        ("yCenter", ctypes.c_int16),
        ("yTarget", ctypes.c_int16),
        ("total_results_learned", ctypes.c_int16),
        ("yaw", ctypes.c_int16),
    ]

class UnionInt16_2(ctypes.Union):
    _fields_ = [
        ("third", ctypes.c_int16),
        ("width", ctypes.c_int16),
        ("angle", ctypes.c_int16),
        ("azimuth", ctypes.c_int16),
        ("total_blocks", ctypes.c_int16),
        ("roll", ctypes.c_int16),
    ]

class UnionInt16_3(ctypes.Union):
    _fields_ = [
        ("fourth", ctypes.c_int16),
        ("height", ctypes.c_int16),
        ("length", ctypes.c_int16),
        ("total_blocks_learned", ctypes.c_int16),
    ]

class PacketData_t(ctypes.Structure):
    _pack_ = 1
    _anonymous_ = ("u0", "u1", "u2", "u3", "u4", "u5")  # 关键点：匿名 union
    _fields_ = [
        ("u0", UnionInt8_0),
        ("u1", UnionInt8_1),
        ("u2", UnionInt16_0),
        ("u3", UnionInt16_1),
        ("u4", UnionInt16_2),
        ("u5", UnionInt16_3),
    ]
    def __init__(self, buf):
        super().__init__()

def read_u16(buf, idx):
    """读取小端 uint16。越界返回 None。"""
    if idx < 0 or idx + 1 >= len(buf):
        return None
    return buf[idx] | (buf[idx + 1] << 8)

def validate_result_payload(buf, keypoint_bytes=0):
    """校验 BLOCK/ARROW 内部布局是否装得进 LEN。通过返回 None，失败返回原因。"""
    if len(buf) < PROTOCOL_SIZE:
        return "buf<%d" % PROTOCOL_SIZE
    ln = buf[CONTENT_SIZE_INDEX]
    need = ln + PROTOCOL_SIZE
    if len(buf) < need:
        return "buf=%d < LEN+6=%d" % (len(buf), need)
    if ln < 10:
        return "LEN=%d < 10" % ln
    payload_end = CONTENT_INDEX + ln
    pos = CONTENT_INDEX + 10
    name_len = 0
    content_len = 0
    if ln > 10:
        name_len = buf[pos]
        pos += 1 + name_len
        if pos > payload_end:
            return "nameLength=%d exceeds LEN=%d" % (name_len, ln)
        if pos < payload_end:
            content_len = buf[pos]
            pos += 1 + content_len
            if pos > payload_end:
                return "contentLength=%d exceeds LEN=%d" % (content_len, ln)
    remain = payload_end - pos
    if keypoint_bytes and remain < keypoint_bytes:
        return (
            "keypoints need %d have %d nameLength=%d contentLength=%d LEN=%d"
            % (keypoint_bytes, remain, name_len, content_len, ln)
        )
    return None

class Result(PacketData_t):
    def __init__(self, buf):
        super().__init__(buf)
        self.nameLength = 0
        self.contentLength = 0
        self.data = buf
        self.name = ""
        self.content = ""
        self.algo = buf[ALGO_INDEX] if len(buf) > ALGO_INDEX else 0
        self.dataLength = buf[CONTENT_SIZE_INDEX] if len(buf) > CONTENT_SIZE_INDEX else 0
        base = CONTENT_INDEX
        if self.dataLength > 10:
            if len(buf) > base + 10:
                self.nameLength = buf[base + 10]
            if len(buf) > base + 10 + 1 + self.nameLength:
                self.contentLength = buf[base + 10 + 1 + self.nameLength]
        
        self.used = False
        self._truncated = False

        if len(buf) < CONTENT_INDEX + 10:
            self._truncated = True
            return

        self.ID = buf[base]
        self.level = buf[base + 1]
        v = read_u16(buf, base + 2)
        if v is None:
            self._truncated = True
            return
        self.first = v
        v = read_u16(buf, base + 4)
        self.second = 0 if v is None else v
        v = read_u16(buf, base + 6)
        self.third = 0 if v is None else v
        v = read_u16(buf, base + 8)
        self.fourth = 0 if v is None else v
        if v is None:
            self._truncated = True
            return

        str_idx = base + 10
        if self.nameLength > 0:
            name_end = str_idx + 1 + self.nameLength
            if name_end > len(buf):
                self._truncated = True
                self.nameLength = 0
            else:
                self.name = buf[str_idx + 1:name_end].decode("utf-8", "ignore")
                str_idx = name_end
        else:
            str_idx += 1
        if self.contentLength > 0:
            content_end = str_idx + 1 + self.contentLength
            if content_end > len(buf):
                self._truncated = True
                self.contentLength = 0
            else:
                self.content = buf[str_idx + 1:content_end].decode("utf-8", "ignore")

    def _fill_keypoints(self, buf, fields):
        base = CONTENT_INDEX + 12 + self.nameLength + self.contentLength
        last = fields[-1][1] + 2
        if self._truncated or base + last > len(buf):
            for name, _ in fields:
                setattr(self, name, 0)
            self._truncated = True
            return
        for name, offset in fields:
            v = read_u16(buf, base + offset)
            if v is None:
                self._truncated = True
                setattr(self, name, 0)
            else:
                setattr(self, name, v)

class FaceResult(Result):
    def __init__(self, buf):
        super().__init__(buf)
        FACE_FIELDS = [
            ("leye_x", 0), ("leye_y", 2),
            ("reye_x", 4), ("reye_y", 6),
            ("nose_x", 8), ("nose_y", 10),
            ("lmouth_x", 12), ("lmouth_y", 14),
            ("rmouth_x", 16), ("rmouth_y", 18)
        ]
        self._fill_keypoints(buf, FACE_FIELDS)

class HandResult(Result):
    def __init__(self, buf):
        super().__init__(buf)
        HAND_FIELDS = [
            ("wrist_x", 0), ("wrist_y", 2),
        
            ("thumb_cmc_x", 4), ("thumb_cmc_y", 6),
            ("thumb_mcp_x", 8), ("thumb_mcp_y", 10),
            ("thumb_ip_x", 12), ("thumb_ip_y", 14),
            ("thumb_tip_x", 16), ("thumb_tip_y", 18),
        
            ("index_finger_mcp_x", 20), ("index_finger_mcp_y", 22),
            ("index_finger_pip_x", 24), ("index_finger_pip_y", 26),
            ("index_finger_dip_x", 28), ("index_finger_dip_y", 30),
            ("index_finger_tip_x", 32), ("index_finger_tip_y", 34),
        
            ("middle_finger_mcp_x", 36), ("middle_finger_mcp_y", 38),
            ("middle_finger_pip_x", 40), ("middle_finger_pip_y", 42),
            ("middle_finger_dip_x", 44), ("middle_finger_dip_y", 46),
            ("middle_finger_tip_x", 48), ("middle_finger_tip_y", 50),
        
            ("ring_finger_mcp_x", 52), ("ring_finger_mcp_y", 54),
            ("ring_finger_pip_x", 56), ("ring_finger_pip_y", 58),
            ("ring_finger_dip_x", 60), ("ring_finger_dip_y", 62),
            ("ring_finger_tip_x", 64), ("ring_finger_tip_y", 66),
        
            ("pinky_finger_mcp_x", 68), ("pinky_finger_mcp_y", 70),
            ("pinky_finger_pip_x", 72), ("pinky_finger_pip_y", 74),
            ("pinky_finger_dip_x", 76), ("pinky_finger_dip_y", 78),
            ("pinky_finger_tip_x", 80), ("pinky_finger_tip_y", 82),
        ]
        self._fill_keypoints(buf, HAND_FIELDS)

class PoseResult(Result):
    def __init__(self, buf):
        super().__init__(buf)
        POSE_FIELDS = [
            ("nose_x", 0),   ("nose_y", 2),
            ("leye_x", 4),   ("leye_y", 6),
            ("reye_x", 8),   ("reye_y", 10),
            ("lear_x", 12),  ("lear_y", 14),
            ("rear_x", 16),  ("rear_y", 18),
        
            ("lshoulder_x", 20), ("lshoulder_y", 22),
            ("rshoulder_x", 24), ("rshoulder_y", 26),
            ("lelbow_x", 28),    ("lelbow_y", 30),
            ("relbow_x", 32),    ("relbow_y", 34),
            ("lwrist_x", 36),    ("lwrist_y", 38),
        
            ("rwrist_x", 40), ("rwrist_y", 42),
            ("lhip_x", 44),   ("lhip_y", 46),
            ("rhip_x", 48),   ("rhip_y", 50),
            ("lknee_x", 52),  ("lknee_y", 54),
            ("rknee_x", 56),  ("rknee_y", 58),
        
            ("lankle_x", 60), ("lankle_y", 62),
            ("rankle_x", 64), ("rankle_y", 66),
        ]
        self._fill_keypoints(buf, POSE_FIELDS)

class ProtocolV2(object):
    def __init__(self):
        self.ERROR_COUNT = 0x05
        self.RETRY_COUNT = 10
        self.RETRY_DELAY_S = 1
        self.FRAME_BUFFER_SIZE = 1024
        self.receive_index = HEADER_0_INDEX
        self.receive_buffer = bytearray(1024)
        self.connect = False
        self.commandHeader = [0x55, 0xAA]
        self.customId = [None, None, None]
        self.result = {}
        self.send_buffer = bytearray(512)
        self._last_drop = ""
        self._wait_fail = ""
        for i in range(256):
            self.result[i] = {"algo": i, "info": None, "blocks": []}

    def toStoreAlgoIndex(self, algo: int):
        if algo >= ALGORITHM_CUSTOM_BEGIN:
            for i in range(len(self.customId)):
                if self.customId[i] == algo:
                    algo = ALGORITHM_CUSTOM0 + i
                    break
        return algo

    def print_hex(self, cmd):
        hex_cmd = [hex(x) for x in cmd]
        logging.debug(hex_cmd)

    def _frame_brief(self, frame):
        if not frame:
            return ""
        n = len(frame)
        ff = sum(1 for b in frame if b == 0xFF)
        head = [hex(x) for x in frame[:min(6, n)]]
        return "len=%d header=%s ff_bytes=%d/%d" % (n, head, ff, n)

    def _log_dropped_frame(self, reason, frame=None, extra=""):
        parts = [reason]
        if extra:
            parts.append(extra)
        if frame:
            parts.append(self._frame_brief(frame))
            if len(frame) > CONTENT_SIZE_INDEX:
                parts.append("cmd=%s" % hex(frame[COMMAND_INDEX]))
                parts.append("LEN=%s" % hex(frame[CONTENT_SIZE_INDEX]))
                if (frame[COMMAND_INDEX] == COMMAND_RETURN_INFO
                        and frame[CONTENT_SIZE_INDEX] != 10):
                    parts.append("hint=INFO_LEN_not_10_possible_bit_error")
        self._last_drop = " ".join(parts)
        logging.debug("dropped packet: %s", self._last_drop)

    def _describe_wait_fail(self, kind, expect_cmd):
        parts = [
            kind,
            "expect_cmd=%s" % hex(expect_cmd),
            "receive_index=%d" % self.receive_index,
        ]
        if kind == "unexpected command" and self.receive_index >= COMMAND_INDEX:
            parts.append("got_cmd=%s" % hex(self.receive_buffer[COMMAND_INDEX]))
            if self.receive_index >= CONTENT_SIZE_INDEX:
                parts.append("LEN=%s" % hex(self.receive_buffer[CONTENT_SIZE_INDEX]))
            parts.append(self._frame_brief(
                self.receive_buffer[0:self.receive_index + 1]))
        if self._last_drop:
            parts.append("prior_drop=(%s)" % self._last_drop)
        self._wait_fail = " ".join(parts)
        return self._wait_fail

    def checksum(self, cmd):
        cs = 0
        for x in cmd:
            cs += x
        return cs & 0xff

    def _flush_device_rx(self):
        self._clear_read_queue()
        self._reset_receive_state()

    def _retry_after_read_fail(self, attempt):
        """读失败后：未用尽次数则延时 1s、清缓存，准备重写命令。"""
        if attempt + 1 >= self.RETRY_COUNT:
            return
        time.sleep(self.RETRY_DELAY_S)
        self._flush_device_rx()

    def knock(self):
        # 初始化时清一次设备残留；后续写命令不再清
        self._flush_device_rx()
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_KNOCK)
        self.husky_lens_protocol_write_uint8(1)
        self.husky_lens_protocol_write_zero_bytes(9)
        self.husky_lens_protocol_write_end()
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def getResult(self, algo):
        self.husky_lens_protocol_write_begin(algo, COMMAND_GET_RESULT)
        self.husky_lens_protocol_write_end()
        last_reason = ""
        for attempt in range(self.RETRY_COUNT):
            n = self._getResultOnce(algo)
            if n is not None:
                return n
            last_reason = self._wait_fail or "getResult"
            self._retry_after_read_fail(attempt)
        logging.error(
            "getResult failed after %d retries algo=%d %s",
            self.RETRY_COUNT, algo, last_reason,
        )
        return None

    def _getResultOnce(self, algo):
        self._write_to_huskyLens()
        ret, _, _ = self.wait(COMMAND_RETURN_INFO)
        if not ret:
            return None
        if self.receive_index != CONTENT_INDEX + 10:
            info_len = -1
            if self.receive_index >= CONTENT_SIZE_INDEX:
                info_len = self.receive_buffer[CONTENT_SIZE_INDEX]
            self._wait_fail = (
                "invalid RETURN_INFO length receive_index=%d LEN=%s"
                % (self.receive_index, hex(info_len & 0xff) if info_len >= 0 else "n/a")
            )
            return None

        self.result[algo]["info"] = Result(self.receive_buffer[0:self.receive_index+1])
        self.result[algo]["info"].total_arrows = (
            self.result[algo]["info"].total_results - self.result[algo]["info"].total_blocks
        )
        self.result[algo]["info"].total_arrows_learned = (
            self.result[algo]["info"].total_results_learned
            - self.result[algo]["info"].total_blocks_learned
        )
        self.result[algo]["blocks"] = []

        for i in range(self.result[algo]["info"].total_blocks):
            ret, _, _ = self.wait(COMMAND_RETURN_BLOCK)
            if not ret:
                return None
            L = self.receive_buffer[CONTENT_SIZE_INDEX] + PROTOCOL_SIZE
            frame = self.receive_buffer[0:L]
            keypoint_bytes = 0
            if algo == ALGORITHM_FACE_RECOGNITION:
                keypoint_bytes = 20
            elif algo == ALGORITHM_POSE_RECOGNITION:
                keypoint_bytes = 68
            elif algo == ALGORITHM_HAND_RECOGNITION:
                keypoint_bytes = 84
            layout_err = validate_result_payload(frame, keypoint_bytes)
            if layout_err:
                self._wait_fail = "invalid BLOCK layout block=%d/%d %s" % (
                    i, self.result[algo]["info"].total_blocks, layout_err)
                return None
            if algo == ALGORITHM_FACE_RECOGNITION:
                parsed = FaceResult(frame)
            elif algo == ALGORITHM_POSE_RECOGNITION:
                parsed = PoseResult(frame)
            elif algo == ALGORITHM_HAND_RECOGNITION:
                parsed = HandResult(frame)
            else:
                parsed = Result(frame)
            self.result[algo]["blocks"].append(parsed)

        for i in range(self.result[algo]["info"].total_arrows):
            ret, _, _ = self.wait(COMMAND_RETURN_ARROW)
            if not ret:
                return None
            L = self.receive_buffer[CONTENT_SIZE_INDEX] + PROTOCOL_SIZE
            if algo == ALGORITHM_LINE_TRACKING:
                parsed = Result(self.receive_buffer[0:L])
            else:
                parsed = Result(self.receive_buffer[0:L])
            self.result[algo]["blocks"].append(parsed)
        return self.result[algo]["info"].total_results

    def _clear_read_queue(self):
        if hasattr(self, "q"):
            while not self.q.empty():
                self.q.get()

    def wait(self, command):
        self._last_drop = ""
        self._wait_fail = ""
        self._abort_wait = False
        receiving = True
        self.receive_buffer = bytearray(1024)
        self.receive_index = HEADER_0_INDEX
        start_ms = time.time_ns() // 1_000_000
        while receiving:
            now_ms = time.time_ns() // 1_000_000
            if now_ms - start_ms > 8000:
                break
            c = self._read_from_huskyLens()
            if c is None:
                time.sleep(0.01)
                continue
            if self.husky_lens_protocol_receive(c):
                if self.receive_buffer[COMMAND_INDEX] == command:
                    receiving = False
                else:
                    # 旧帧（如等 0x1A 却先碰到 INFO/BLOCK），丢掉继续读，不重写
                    self.receive_buffer = bytearray(1024)
                    self.receive_index = HEADER_0_INDEX
            elif self._abort_wait:
                break
        if self._abort_wait:
            self._describe_wait_fail("bad frame", command)
            self._flush_device_rx()
            return False, [], []
        if receiving:
            self._describe_wait_fail("timeout 8s", command)
            self._flush_device_rx()
            return False, [], []
        retInt = []
        retStr = []
        if command != COMMAND_RETURN_ARGS:
            return True, [], []

        totalIntArgs = self.receive_buffer[CONTENT_INDEX]
        contentSize = self.receive_buffer[CONTENT_SIZE_INDEX]
        contentEnd = CONTENT_INDEX + contentSize
        retValue = self.receive_buffer[CONTENT_INDEX + 1]
        offset = CONTENT_INDEX + 2
        for _ in range(totalIntArgs):
            v = self.receive_buffer[offset] | (self.receive_buffer[offset + 1] << 8)
            retInt.append(v)
            offset += 2

        offset = CONTENT_INDEX + 10
        logging.debug(f"contentEnd={contentEnd},offset={offset}")
        while offset < contentEnd:
            length = self.receive_buffer[offset]
            logging.debug(f"length={length}")
            if length == 0:
                break
            offset += 1
        
            # 越界保护
            if offset + length > contentEnd:
                break
        
            s = bytes(self.receive_buffer[offset:offset + length]).decode("utf-8")
            logging.debug(f"s={s}")
            retStr.append(s)
            offset += length
        return retValue == 0, retInt, retStr

    def _reset_receive_state(self, data=None):
        self.receive_index = HEADER_0_INDEX
        if data == 0x55:
            self.receive_buffer[HEADER_0_INDEX] = 0x55
            self.receive_index = HEADER_1_INDEX

    def husky_lens_protocol_receive(self, data):
        data &= 0xFF
        max_content = min(255, self.FRAME_BUFFER_SIZE - PROTOCOL_SIZE)

        if self.receive_index == HEADER_0_INDEX:
            if data != 0x55:
                return False
            self.receive_buffer[HEADER_0_INDEX] = 0x55
            self.receive_index = HEADER_1_INDEX
            return False

        if self.receive_index == HEADER_1_INDEX:
            if data != 0xAA:
                # 0x55 0x55 AA：把当前字节当作新的包头
                self._reset_receive_state(data)
                return False
            self.receive_buffer[HEADER_1_INDEX] = 0xAA
            self.receive_index = COMMAND_INDEX
            return False

        if self.receive_index == COMMAND_INDEX:
            self.receive_buffer[COMMAND_INDEX] = data
            self.receive_index = ALGO_INDEX
            return False

        if self.receive_index == ALGO_INDEX:
            self.receive_buffer[ALGO_INDEX] = data
            self.receive_index = CONTENT_SIZE_INDEX
            return False

        if self.receive_index == CONTENT_SIZE_INDEX:
            if data > max_content:
                self._log_dropped_frame("invalid content size", extra="size=%d" % data)
                self._reset_receive_state(data)
                self._abort_wait = True
                return False
            self.receive_buffer[CONTENT_SIZE_INDEX] = data
            self.receive_index = CONTENT_INDEX
            return False

        if self.receive_index >= self.FRAME_BUFFER_SIZE:
            self._log_dropped_frame("receive buffer overflow")
            self._reset_receive_state(data)
            self._abort_wait = True
            return False

        self.receive_buffer[self.receive_index] = data
        frame_end = self.receive_buffer[CONTENT_SIZE_INDEX] + CONTENT_INDEX
        if self.receive_index == frame_end:
            frame = self.receive_buffer[0:self.receive_index + 1]
            logging.debug(f"<--------self.receive_index={self.receive_index}")
            self.print_hex(frame)
            calc_cs = self.checksum(frame[:-1])
            recv_cs = frame[-1]
            valid = (
                len(frame) >= PROTOCOL_SIZE
                and frame[HEADER_0_INDEX] == 0x55
                and frame[HEADER_1_INDEX] == 0xAA
                and calc_cs == recv_cs
            )
            if not valid:
                self._log_dropped_frame(
                    "checksum/header mismatch",
                    frame,
                    extra="receive_index=%d calc_cs=%d recv_cs=%d" % (
                        self.receive_index, calc_cs, recv_cs),
                )
                self._reset_receive_state(data)
                self._abort_wait = True
                return False
            return True

        self.receive_index += 1
        return False

    def available(self, algo):
        for i in range(len(self.result[algo]["blocks"])):
            if not self.result[algo]["blocks"][i].used:
                return True
        return False

    def husky_lens_protocol_write_begin(self, algo, command):
        self.send_buffer = bytearray(512)
        self.send_buffer[HEADER_0_INDEX] = 0x55
        self.send_buffer[HEADER_1_INDEX] = 0xAA
        self.send_buffer[COMMAND_INDEX] = command
        self.send_buffer[ALGO_INDEX] = algo
        self.send_index = CONTENT_INDEX

    def husky_lens_protocol_write_uint8(self, content):
        self.send_buffer[self.send_index] = content
        self.send_index += 1

    def husky_lens_protocol_write_zero_bytes(self, count):
        end = self.send_index + count
        self.send_buffer[self.send_index:end] = b'\x00' * count
        self.send_index = end
    
    def husky_lens_protocol_write_string(self, string : str):
        data = string.encode("utf-8")
        length = len(data)
        end = self.send_index + 1 + length
        self.send_buffer[self.send_index:end] = bytes([length]) + data
        self.send_index = end
        
    def husky_lens_protocol_write_int16(self, content):
        self.send_buffer[self.send_index] = content & 0xFF
        self.send_buffer[self.send_index + 1] = (content >> 8) & 0xFF
        self.send_index += 2

    def husky_lens_protocol_write_int32(self, content):
        self.send_buffer[self.send_index] = content & 0xFF
        self.send_buffer[self.send_index + 1] = (content >> 8) & 0xFF
        self.send_buffer[self.send_index + 2] = (content >> 16) & 0xFF
        self.send_buffer[self.send_index + 3] = (content >> 24) & 0xFF
        self.send_index += 4

    def husky_lens_protocol_write_end(self):
        self.send_buffer[CONTENT_SIZE_INDEX] = self.send_index - CONTENT_INDEX
        cs = 0
        for i in range(self.send_index):
            cs += self.send_buffer[i]
        self.send_buffer[self.send_index] = cs & 0xFF
        self.send_index += 1
    def learnBlock(self, algo, x, y, width, height):
        self.husky_lens_protocol_write_begin(algo, COMMAND_ACTION_LEARN_BLOCK)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_int16(x)
        self.husky_lens_protocol_write_int16(y)
        self.husky_lens_protocol_write_int16(width)
        self.husky_lens_protocol_write_int16(height)
        self.husky_lens_protocol_write_end()
        ret, argInt, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        if not ret:
            return 0
        return argInt[0] if argInt else 0
        
    def switchAlgorithm(self, algo):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_SET_ALGORITHM)
        self.husky_lens_protocol_write_uint8(algo)
        self.husky_lens_protocol_write_zero_bytes(9)
        self.husky_lens_protocol_write_end()
      
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def takePhoto(self, resolution):
        resolutions = {"default": RESOLUTION_1280x720, "640x480": RESOLUTION_640x480, 
                       "1280x720": RESOLUTION_1280x720, "1920x1080": RESOLUTION_1920x1080}
        if resolution not in resolutions:
            return ""
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_TAKE_PHOTO)
        self.husky_lens_protocol_write_uint8(resolutions[resolution])
        self.husky_lens_protocol_write_zero_bytes(9)
        self.husky_lens_protocol_write_end()
        ret, _, argStr = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        if not ret:
            return ""
        return argStr[0] if argStr else ""

    def takeScreenshot(self):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_TAKE_SCREENSHOT)
        self.husky_lens_protocol_write_end()
        ret, _, argStr = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        if not ret:
            return ""
        return argStr[0] if argStr else ""

    def learn(self, algo):
        self.husky_lens_protocol_write_begin(algo, COMMAND_ACTION_LEARN)
        self.husky_lens_protocol_write_end()
        ret, argInt, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        if not ret:
            return 0
        return argInt[0] if argInt else 0

    def forget(self, algo):
        self.husky_lens_protocol_write_begin(algo, COMMAND_ACTION_FORGET)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def drawRect(self, color: int, lineWidth: int, x: int, y: int, width: int, height: int):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_DRAW_RECT)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_uint8(lineWidth)
        self.husky_lens_protocol_write_int16(x)
        self.husky_lens_protocol_write_int16(y)
        self.husky_lens_protocol_write_int16(width)
        self.husky_lens_protocol_write_int16(height)
        self.husky_lens_protocol_write_int16(0)
        self.husky_lens_protocol_write_int32(color)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def drawUniqueRect(self, color: int, lineWidth: int, x: int, y: int, width: int, height: int):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_DRAW_UNIQUE_RECT)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_uint8(lineWidth)
        self.husky_lens_protocol_write_int16(x)
        self.husky_lens_protocol_write_int16(y)
        self.husky_lens_protocol_write_int16(width)
        self.husky_lens_protocol_write_int16(height)
        self.husky_lens_protocol_write_int16(0)
        self.husky_lens_protocol_write_int32(color)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def clearRect(self):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_CLEAN_RECT)
        self.husky_lens_protocol_write_end()

        ret,_,_ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def drawText(self, color: int, fontSize: int, x: int, y: int, text: str):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_DRAW_TEXT)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_uint8(fontSize)
        
        self.husky_lens_protocol_write_int16(x)
        self.husky_lens_protocol_write_int16(y)
        self.husky_lens_protocol_write_int16(0)
        self.husky_lens_protocol_write_int16(0)
        self.husky_lens_protocol_write_string(text)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_int32(color)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret
        
    def clearText(self):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_CLEAR_TEXT)
        self.husky_lens_protocol_write_end()
        
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def saveKnowledges(self, algo: int, knowledgeID: int):
        self.husky_lens_protocol_write_begin(algo, COMMAND_ACTION_SAVE_KNOWLEDGES)
        self.husky_lens_protocol_write_uint8(knowledgeID)
        self.husky_lens_protocol_write_zero_bytes(9)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def loadKnowledges(self, algo: int, knowledgeID: int):
        self.husky_lens_protocol_write_begin(algo, COMMAND_ACTION_LOAD_KNOWLEDGES)
        self.husky_lens_protocol_write_uint8(knowledgeID)
        self.husky_lens_protocol_write_zero_bytes(9)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def playMusic(self, name: str, volume: int):
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_PLAY_MUSIC)
        self.husky_lens_protocol_write_zero_bytes(2)
     
        self.husky_lens_protocol_write_int16(volume)
        self.husky_lens_protocol_write_zero_bytes(6)
        self.husky_lens_protocol_write_string(name)
        self.husky_lens_protocol_write_end()
      
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def setNameByID(self, algo: int, ID: int, name: str):
        self.husky_lens_protocol_write_begin(algo, COMMAND_SET_NAME_BY_ID)
        self.husky_lens_protocol_write_uint8(ID)
        self.husky_lens_protocol_write_zero_bytes(9)
        self.husky_lens_protocol_write_string(name)
        self.husky_lens_protocol_write_end()
        
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def setMultiAlgorithm(self, algos: list):
        if len(algos) > 3 or len(algos) < 2:
            return False
        customAlgoNum = 0
        self.customId = [None, None, None]
        for algo in algos:
            if algo >= ALGORITHM_CUSTOM_BEGIN:
                self.customId[customAlgoNum] = algo
                customAlgoNum += 1

        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_SET_MULTI_ALGORITHM)
        self.husky_lens_protocol_write_uint8(len(algos))
        self.husky_lens_protocol_write_uint8(0)

        for algo in algos:
            self.husky_lens_protocol_write_int16(algo)
        for _ in range(4 - len(algos)):
            self.husky_lens_protocol_write_int16(0)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def setMultiAlgorithmRatio(self, ratios: list):
        if len(ratios) > 3 or len(ratios) < 2:
            return False
        self.husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_SET_MULTI_ALGORITHM_RATIO)
        self.husky_lens_protocol_write_uint8(len(ratios))
        self.husky_lens_protocol_write_uint8(0)

        for ratio in ratios:
            self.husky_lens_protocol_write_int16(ratio)
        for _ in range(4 - len(ratios)):
            self.husky_lens_protocol_write_int16(0xFFFF)

        self.husky_lens_protocol_write_end()
        
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def setAlgorithmParams(self, algo, params=None):
        if params is None:
            params = {"show_name": False}
        for k, v in params.items():
            self.husky_lens_protocol_write_begin(algo, COMMAND_SET_ALGO_PARAMS)
           
            if isinstance(v, bool):
                self.husky_lens_protocol_write_uint8(1)
                self.husky_lens_protocol_write_uint8(0)
                self.husky_lens_protocol_write_int16(v)
                self.husky_lens_protocol_write_zero_bytes(6)
                self.husky_lens_protocol_write_string(k)
            elif isinstance(v, float):
                float_bytes = struct.pack("<f", v)
                v0, v1 = struct.unpack("<hh", float_bytes)
                self.husky_lens_protocol_write_uint8(2)
                self.husky_lens_protocol_write_uint8(0)
                self.husky_lens_protocol_write_int16(v0)
                self.husky_lens_protocol_write_int16(v1)
                self.husky_lens_protocol_write_zero_bytes(4)
                self.husky_lens_protocol_write_string(k)
            elif isinstance(v, str):
                self.husky_lens_protocol_write_zero_bytes(10)
                self.husky_lens_protocol_write_string(k)
                self.husky_lens_protocol_write_string(v)
            else:
                logging.error(f"unknown type key={k} value={v}")
                return False
            self.husky_lens_protocol_write_end()
            ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
            if not ret:
                return False
        return True

    def updateAlgoParams(self, algo):
        self.husky_lens_protocol_write_begin(algo, COMMAND_UPDATE_ALGORITHM_PARAMS)
        self.husky_lens_protocol_write_end()
        ret,_,_ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def getAlgorithmParams(self, algo, param_keys):
        params = {}
        for k in param_keys:
            self.husky_lens_protocol_write_begin(algo, COMMAND_GET_ALGO_PARAM)
            self.husky_lens_protocol_write_zero_bytes(10)
            self.husky_lens_protocol_write_string(k)
            self.husky_lens_protocol_write_end()
            ret, argInt, argStr = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
            logging.debug(f"argInt={argInt},argStr={argStr}")
            if ret:
                if len(argInt) == 1:
                    params[k] = argInt[0] == 1
                elif len(argInt) == 2:
                    # 把两个 int16 拼成 4 字节
                    v0 = argInt[0] - 0x10000 if argInt[0] > 0x7FFF else argInt[0]
                    v1 = argInt[1] - 0x10000 if argInt[1] > 0x7FFF else argInt[1]
                    float_bytes = struct.pack("<hh", v0, v1)
                    # 再把 4 字节当作 float 解析
                    value = struct.unpack("<f", float_bytes)[0]
                    params[k] = round(value, 1)
                if argStr:
                    params[k] = argStr[0]
        return params

    def startRecording(self, mediaType: int, duration: int, filename: str = "", resolution: int = RESOLUTION_DEFAULT):
        self.husky_lens_protocol_write_begin(0, COMMAND_ACTION_START_RECORDING)
        self.husky_lens_protocol_write_uint8(resolution)
        self.husky_lens_protocol_write_uint8(mediaType)
        self.husky_lens_protocol_write_int16(duration)
        self.husky_lens_protocol_write_zero_bytes(6)
        self.husky_lens_protocol_write_string(filename)
        self.husky_lens_protocol_write_end()
        
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def stopRecording(self, mediaType: int):
        self.husky_lens_protocol_write_begin(0, COMMAND_ACTION_STOP_RECORDING)
        self.husky_lens_protocol_write_uint8(0)
        self.husky_lens_protocol_write_uint8(mediaType)
        self.husky_lens_protocol_write_zero_bytes(8)
        self.husky_lens_protocol_write_end()
        
        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def e2eStartRecording(self):
        self.husky_lens_protocol_write_begin(0, COMMAND_ACTION_E2E_START_RECORDING)
        self.husky_lens_protocol_write_zero_bytes(10)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def e2eStopRecording(self):
        self.husky_lens_protocol_write_begin(0, COMMAND_ACTION_E2E_STOP_RECORDING)
        self.husky_lens_protocol_write_zero_bytes(10)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def e2eSendAnnotation(self, annotation:str):
        self.husky_lens_protocol_write_begin(0, COMMAND_ACTION_E2E_SEND_ANNOTATION)
        self.husky_lens_protocol_write_zero_bytes(10)
        self.husky_lens_protocol_write_string(annotation)
        self.husky_lens_protocol_write_end()

        ret, _, _ = self.executeCommand(wait_cmd=COMMAND_RETURN_ARGS)
        return ret

    def executeCommand(self, wait_cmd):
        for attempt in range(self.RETRY_COUNT):
            self._write_to_huskyLens()
            ret, retInt, retStr = self.wait(wait_cmd)
            if ret:
                return ret, retInt, retStr
            self._retry_after_read_fail(attempt)
        logging.error(
            "command failed after %d retries expect_cmd=%s %s",
            self.RETRY_COUNT, hex(wait_cmd), self._wait_fail,
        )
        return False, [], []

class HuskylensV2(ProtocolV2):
    def __init__(self):
        super().__init__()
    
    def begin(self):
        return self.knock()
        
    def popCachedResult(self, algo):
        for i in range(len(self.result[algo]["blocks"])):
            if self.result[algo]["blocks"][i].used:
                continue
            self.result[algo]["blocks"][i].used = True
            return self.result[algo]["blocks"][i]
        return None

    def getCachedCenterResult(self, algo):
        centerIndex = -1
        minLen = 0x0FFFFFFF
        for i in range(len(self.result[algo]["blocks"])):
            length = math.pow(self.result[algo]["blocks"][i].xCenter - LCD_WIDTH / 2, 2) + \
                     math.pow(self.result[algo]["blocks"][i].yCenter - LCD_HEIGHT / 2, 2)
            if length < minLen:
                minLen = length
                centerIndex = i
        if centerIndex != -1:
            return self.result[algo]["blocks"][centerIndex]
        return None

    def getCachedResultByIndex(self, algo, index):
        if index >= len(self.result[algo]["blocks"]):
          return None
        return self.result[algo]["blocks"][index]

    def getCachedResultByID(self, algo, ID):
        logging.debug(f"len(self.result[algo][blocks])={len(self.result[algo]['blocks'])}")
        for i in range(len(self.result[algo]["blocks"])):
            if self.result[algo]["blocks"][i].ID == ID:
                return self.result[algo]["blocks"][i]
        return None

    def getCachedResultNum(self, algo):
        return len(self.result[algo]["blocks"])

    def getCachedResultLearnedNum(self, algo):
        count = 0
        for i in range(len(self.result[algo]["blocks"])):
            if self.result[algo]["blocks"][i].ID != 0:
                count += 1
        return count
    
    def getCachedResultNumByID(self, algo, ID):
        count = 0
        for i in range(len(self.result[algo]["blocks"])):
            if ID == self.result[algo]["blocks"][i].ID:
                count += 1
        return count

    def getCachedIndexResultByID(self, algo: int, ID: int, index: int):
        logging.debug(f"len(self.result[algo][blocks]={len(self.result[algo]['blocks'])}")
        _index = 0
        for i in range(len(self.result[algo]["blocks"])):
            logging.debug(f"i={i} ID={self.result[algo]['blocks'][i].ID}")
            if ID == self.result[algo]["blocks"][i].ID:
                if index == _index:
                    logging.debug(f"index={index}  i={i}")
                    return self.result[algo]["blocks"][i]
                _index += 1
        return None

    def getCachedResultMaxID(self, algo: int):
        return self.result[algo]["info"].maxID

    def getCurrentBranch(self, algo: int, attr: str):
        blocks = self.result[algo]["blocks"]
        logging.debug(f"len(blocks)={len(blocks)}")
        if len(blocks) == 0:
            return 0
        if blocks[0].level == 1:
            return getattr(blocks[0], attr, 0)
        return 0

    def getUpcomingBranchCount(self, algo: int):
        count = len(self.result[algo]["blocks"]) - 1
        if count < 0:
            count = 0
        return count

    def getBranch(self, algo: int, index: int, attr: str):
        blocks = self.result[algo]["blocks"]
        if len(blocks) - 1 - index > 0:
            return getattr(blocks[1 + index], attr, 0)
        return 0

    def createResult(self):
        return Result([0] * 16)  

class HuskylensV2_I2C(HuskylensV2):
    def __init__(self, bus_num=1):  
        self.bus = smbus2.SMBus(bus_num)       
        self._connect = 0
        self.i2c_addr = 0x50
        self.q = queue.Queue()
        super().__init__()

    def _error_handling(self):
        self._connect += 1

    def _flush_device_rx(self, timeout_ms=150, max_bytes=2048):
        """knock/begin 初始化时丢掉设备 TX FIFO / 主机队列里的旧帧。

        I2C 没有 data-ready：FIFO 空时读到的是 0xFF 填充。
        连续两轮 16 字节全 0xFF 视为已空；超时或读满则停。
        """
        self._clear_read_queue()
        idle_reads = 0
        flushed = 0
        saw_header = False
        reason = "max_bytes"
        start_ms = time.time_ns() // 1_000_000
        while flushed < max_bytes:
            now_ms = time.time_ns() // 1_000_000
            if now_ms - start_ms > timeout_ms:
                reason = "timeout"
                break
            try:
                data = self._i2c_read_bytes(16)
            except Exception as e:
                reason = "i2c_error"
                logging.error("flush rx I2C error: %s", e)
                break
            if not data:
                reason = "empty"
                break
            flushed += len(data)
            if 0x55 in data:
                saw_header = True
            if all(b == 0xFF for b in data):
                idle_reads += 1
                if idle_reads >= 2:
                    reason = "idle"
                    break
            else:
                idle_reads = 0
        self._clear_read_queue()
        self._reset_receive_state()

    def _write_to_huskyLens(self):
        self._connect = 0
        command = bytes(self.send_buffer[0:self.send_index])
        while True:
            try:
                self.bus.i2c_rdwr(i2c_msg.write(self.i2c_addr, command))
                logging.debug("_write_to_huskyLens ----->")
                self.print_hex(command)
                time.sleep(0.05)
                return
            except Exception as e:
                logging.error("I2C write failed (%d/%d): %s", self._connect + 1, self.ERROR_COUNT, e)
                self._clear_read_queue()
                self._reset_receive_state()
                self._error_handling()
            if self._connect > self.ERROR_COUNT:
                raise ValueError("Please check the huskylens connection or Reconnection sensor!!!")

    def _i2c_read_bytes(self, n):
        if n < 1:
            n = 1
        msg = i2c_msg.read(self.i2c_addr, n)
        self.bus.i2c_rdwr(msg)
        return bytes(msg)

    def _read_need(self):
        # 包头未齐：只补齐 55 AA CMD ALGO LEN，不再固定读 32
        if self.receive_index <= CONTENT_SIZE_INDEX:
            return CONTENT_SIZE_INDEX - self.receive_index + 1
        frame_end = self.receive_buffer[CONTENT_SIZE_INDEX] + CONTENT_INDEX
        return max(1, frame_end - self.receive_index + 1)

    def _read_from_huskyLens(self):
        self._connect = 0
        if self.q.empty():
            try:
                for c in self._i2c_read_bytes(self._read_need()):
                    self.q.put(c)
            except Exception:
                time.sleep(0.01)
        if self.q.empty():
            return None
        return self.q.get()
    


class HuskylensV2_UART(HuskylensV2):
    def __init__(self, tty_name="/dev/ttyS0", baudrate=115200, debug_level=logging.INFO):
        logging.getLogger().setLevel(debug_level)

        self.q = queue.Queue()
        self._connect = 0
        
        self.uart = serial.Serial(tty_name, baudrate=baudrate, timeout=0.01)
        super().__init__()

    def _error_handling(self):
        self._connect += 1

    def _flush_device_rx(self):
        self._clear_read_queue()
        try:
            n = self.uart.in_waiting
            if n:
                self.uart.read(n)
        except Exception:
            pass
        self._clear_read_queue()
        self._reset_receive_state()

    def _write_to_huskyLens(self):
        self._connect = 0
        command = self.send_buffer[0:self.send_index]
        while True:
            try:
              
                self.uart.write(command)
                logging.debug("_write_to_huskyLens ----->")
                self.print_hex(command)
                time.sleep(0.1)
                return
            except Exception as e:
                logging.error("UART write failed (%d/%d): %s", self._connect + 1, self.ERROR_COUNT, e)
                self._error_handling()
            if self._connect > self.ERROR_COUNT:
                raise ValueError("Please check the huskylens connection or Reconnection sensor!!!")

    def _read_from_huskyLens(self):
        self._connect = 0
        if self.q.empty():
            try:
    
                d = self.uart.read(32)
                for c in d:
                    self.q.put(c)
            except Exception:
                time.sleep(0.01)
        if self.q.empty():
            return None
        return self.q.get()