#ifndef DFROBOT_HUSKEYLENS_V2_COMMON_H
#define DFROBOT_HUSKEYLENS_V2_COMMON_H
#include <Arduino.h>
#include <HardwareSerial.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <Stream.h>
#if 0
#define DBG(x)                                                                 \
  do {                                                                         \
    Serial.print(__FUNCTION__);                                                \
    Serial.print("():");                                                       \
    Serial.print(__LINE__);                                                    \
    Serial.print(":");                                                         \
    Serial.println(x);                                                         \
  } while (0)
#define DBG_KV(k, v)                                                           \
  do {                                                                         \
    Serial.print(__FUNCTION__);                                                \
    Serial.print("():");                                                       \
    Serial.print(__LINE__);                                                    \
    Serial.print(":");                                                         \
    Serial.print(k);                                                           \
    Serial.println(v);                                                         \
  } while (0)
#define DBG_HEX(x)                                                             \
  do {                                                                         \
    Serial.print(__FUNCTION__);                                                \
    Serial.print("():");                                                       \
    Serial.print(__LINE__);                                                    \
    Serial.print(":");                                                         \
    Serial.println(x, HEX);                                                    \
  } while (0)

#define DBG_HEX_ARRAY(x, len)                                                  \
  do {                                                                         \
    for (uint16_t i = 0; i < len; i++) {                                       \
      Serial.print(x[i], HEX);                                                 \
      Serial.print(" ");                                                       \
    }                                                                          \
  } while (0)
#define DBG_PRINT(x) Serial.print(x)
#define DBG_PRINTLN(x) Serial.println(x)
#else
#define DBG(x)
#define DBG_KV(k, v)
#define DBG_HEX(x)
#define DBG_HEX_ARRAY(x, len)
#define DBG_PRINT(x)
#define DBG_PRINTLN(x)
#endif

#include "Wire.h"

#if defined(ESP32) || defined(NRF5) || defined(ESP8266) || defined(NRF52833)
#define LARGE_MEMORY 1
#endif

//  小内存（AVR）只使用基类的内容，大内存MCU（esp32 microbit）可以使用派生类内容
#ifdef LARGE_MEMORY
#define FRAME_BUFFER_SIZE 512
#define MAX_RESULT_NUM 10
#define CMD_BUFFER_SIZE 512
#define MAX_PL_LEN 64
#else
#define FRAME_BUFFER_SIZE 128
#define MAX_RESULT_NUM 6
#define CMD_BUFFER_SIZE 64
#define MAX_PL_LEN 32
#endif

#define LCD_WIDTH 640
#define LCD_HEIGHT 480

#define HEADER_0_INDEX 0
#define HEADER_1_INDEX 1
#define COMMAND_INDEX 2
#define ALGO_INDEX 3
#define CONTENT_SIZE_INDEX 4
#define CONTENT_INDEX 5
#define PROTOCOL_SIZE 6

#define SQUARE(x) ((x) * (x))

typedef enum {
  RESOLUTION_DEFAULT = 0,
  RESOLUTION_640x480 = 1,
  RESOLUTION_1280x720 = 2,
  RESOLUTION_1920x1080 = 3,
} eResolution_t;

typedef enum {
  MEDIA_TYPE_AUDIO = 1,
  MEDIA_TYPE_VIDEO = 2,
} eMediaType_t;

typedef enum protocolCommand {
  COMMAND_KNOCK = 0x00,
  COMMAND_GET_RESULT = 0x01,
  COMMAND_GET_ALGO_PARAM = 0x02,
  COMMAND_GET_RESULT_BY_ID = 0x03,
  COMMAND_GET_BLOCKS_BY_ID = 0x04,
  COMMAND_GET_ARROWS_BY_ID = 0x05,
  // RFU 0x06 - 0x09

  COMMAND_SET_ALGORITHM = 0x0A,
  COMMAND_SET_NAME_BY_ID = 0x0B,
  COMMAND_SET_MULTI_ALGORITHM = 0x0C,
  COMMAND_SET_MULTI_ALGORITHM_RATIO = 0x0D,
  COMMAND_SET_ALGO_PARAMS = 0x0E,
  COMMAND_UPDATE_ALGORITHM_PARAMS = 0x0F,
  // RFU 0x0F - 0x19

  COMMAND_RETURN_ARGS = 0x1A,
  COMMAND_RETURN_INFO = 0x1B,
  COMMAND_RETURN_BLOCK = 0x1C,
  COMMAND_RETURN_ARROW = 0x1D,
  // RFU 0x1E - 0x1F

  COMMAND_ACTION_TAKE_PHOTO = 0x20,
  COMMAND_ACTION_TAKE_SCREENSHOT = 0x21,
  COMMAND_ACTION_LEARN = 0x22,
  COMMAND_ACTION_FORGET = 0x23,
  COMMAND_ACTION_SAVE_KNOWLEDGES = 0x24,
  COMMAND_ACTION_LOAD_KNOWLEDGES = 0x25,
  COMMAND_ACTION_DRAW_RECT = 0x26,
  COMMAND_ACTION_CLEAR_RECT = 0x27,
  COMMAND_ACTION_DRAW_TEXT = 0x28,
  COMMAND_ACTION_CLEAR_TEXT = 0x29,
  COMMAND_ACTION_PLAY_MUSIC = 0x2A,
  COMMAND_EXIT = 0x2B,
  COMMAND_ACTION_LEARN_BLOCK = 0x2C,
  COMMAND_ACTION_DRAW_UNIQUE_RECT = 0x2D,
  COMMAND_ACTION_START_RECORDING = 0x2E,
  COMMAND_ACTION_STOP_RECORDING = 0x2F,
  // RFU 0x30 - 0x3F

  COMMAND_ACTION_E2E_START_RECORDING  = 0x30, 
  COMMAND_ACTION_E2E_STOP_RECORDING   = 0x31,
  COMMAND_ACTION_E2E_SEND_ANNOTATION   = 0x32,

} eProtocolCommand_t;

typedef enum {
  ALGORITHM_ANY = 0,                      // 0
  ALGORITHM_FACE_RECOGNITION = 1,         // 1
  ALGORITHM_OBJECT_RECOGNITION,           // 2
  ALGORITHM_OBJECT_TRACKING,              // 3
  ALGORITHM_COLOR_RECOGNITION,            // 4
  ALGORITHM_OBJECT_CLASSIFICATION,        // 5
  ALGORITHM_SELF_LEARNING_CLASSIFICATION, // 6
  ALGORITHM_SEGMENT,                      // 7
  ALGORITHM_HAND_RECOGNITION,             // 8
  ALGORITHM_POSE_RECOGNITION,             // 9
  ALGORITHM_LICENSE_RECOGNITION,          // 10
  ALGORITHM_OCR_RECOGNITION,              // 11
  ALGORITHM_LINE_TRACKING,                // 12
  ALGORITHM_EMOTION_RECOGNITION,          // 13
  ALGORITHM_GAZE_RECOGNITION,             // 14
  ALGORITHM_FACE_ORIENTATION,             // 15
  ALGORITHM_TAG_RECOGNITION,              // 16
  ALGORITHM_BARCODE_RECOGNITION,          // 17
  ALGORITHM_QRCODE_RECOGNITION,           // 18
  ALGORITHM_FALLDOWN_RECOGNITION,         // 19
  ALGORITHM_DEPTH_CAMERA,                 // 20
  ALGORITHM_DONKEYCAR,                    // 21
  ALGORITHM_CAMERA,                       // 22
  ALGORITHM_RFU3,                         // 23
  ALGORITHM_RFU4,                         // 24
  ALGORITHM_CUSTOM0,                      // 25
  ALGORITHM_CUSTOM1,                      // 26
  ALGORITHM_CUSTOM2,                      // 27
  ALGORITHM_BUILTIN_COUNT,                // 28

  ALGORITHM_CUSTOM_BEGIN = 128, // 128

} eAlgorithm_t;

#ifdef LARGE_MEMORY
#define ALGORITHM_COUNT ALGORITHM_BUILTIN_COUNT
#define CUSTOM_ALGORITHM_COUNT 3
#else
#define ALGORITHM_COUNT 1
#define CUSTOM_ALGORITHM_COUNT 1
#endif

typedef enum BoardType {
  BOARD_SMALL_RAM = 0x0,
  BOARD_LARGE_RAM = 0x1
} eBoardType_t;

typedef enum ResultType {
  Result_Block = 0x0,
  Result_Arrow = 0x1,
  Result_Unknown
} eResultType_t;

typedef struct __attribute__((packed)) {
  uint8_t head55;
  uint8_t headaa;
  uint8_t cmd;
  uint8_t algo_id;
  uint8_t data_length;
  uint8_t data[0];
} PacketHead_t;

typedef struct __attribute__((packed)) {
  uint8_t length;
  int8_t data[0];
  // 成员函数方式
  String toString() const {
    if (length == 0) {
      return String("");
    }
    char *buf = (char *)malloc(length + 1);
    if (buf == NULL) {
      return String("");
    }
    memcpy(buf, data, length);
    buf[length] = 0;
    String str(buf);
    free(buf);
    return str;
  }
} String_t;

typedef struct __attribute__((packed)) {
  union {
    uint8_t ID;
    uint8_t maxID;
    uint8_t rfu0;
    uint8_t resolution;
    uint8_t boardType;
    uint8_t multiAlgoNum;
  };
  union {
    int8_t rfu1;
    int8_t level;
    int8_t mediaType;
    int8_t retValue;
    int8_t lineWidth;
    int8_t confidence;
  };
  union {
    int16_t first;
    int16_t xCenter;
    int16_t xTarget;
    int16_t duration;
    int16_t algorithmType;
    int16_t classID;
    int16_t total_results;
    int16_t pitch; // eular[0],沿Y轴移动，俯仰角,上下移动
  };
  union {
    int16_t second;
    int16_t yCenter;
    int16_t yTarget;
    int16_t total_results_learned;
    int16_t yaw; // eular[1], 沿Z轴移动， 偏航角,左右移动
  };
  union {
    int16_t third;
    int16_t width;
    int16_t angle;
    int16_t azimuth;
    int16_t total_blocks;
    int16_t roll;     // eular[2], 沿X轴移动， 横滚角,前后移动
    int16_t steering; // 转向角度
  };
  union {
    int16_t fourth;
    int16_t height;
    int16_t length;
    int16_t total_blocks_learned;
    int16_t throttle; // 油门
  };
  int8_t payload[0];
} PacketData_t;

class Result : public PacketData_t {
public:
  Result(const void *buf);
  ~Result();

public:
  int8_t type = -1;
  int8_t used = 0;
  String name;
  String content;
};

#ifdef LARGE_MEMORY
class FaceResult : public Result {
public:
  FaceResult(const void *buf);

public:
  int16_t leye_x;
  int16_t leye_y;
  int16_t reye_x;
  int16_t reye_y;
  int16_t nose_x;
  int16_t nose_y;
  int16_t lmouth_x;
  int16_t lmouth_y;
  int16_t rmouth_x;
  int16_t rmouth_y;
};

class HandResult : public Result {
public:
  HandResult(const void *buf);

public:
  int16_t wrist_x, wrist_y;         // 手腕
  int16_t thumb_cmc_x, thumb_cmc_y; // 拇指根部
  int16_t thumb_mcp_x, thumb_mcp_y; // 拇指中间关节
  int16_t thumb_ip_x, thumb_ip_y;   // 拇指第二关节
  int16_t thumb_tip_x, thumb_tip_y; // 拇指指尖

  int16_t index_finger_mcp_x, index_finger_mcp_y;   // 食指根部
  int16_t index_finger_pip_x, index_finger_pip_y;   // 食指第一关节
  int16_t index_finger_dip_x, index_finger_dip_y;   // 食指第二关节
  int16_t index_finger_tip_x, index_finger_tip_y;   // 食指指尖
  int16_t middle_finger_mcp_x, middle_finger_mcp_y; // 中指根部

  int16_t middle_finger_pip_x, middle_finger_pip_y; // 中指第一关节
  int16_t middle_finger_dip_x, middle_finger_dip_y; // 中指第二关节
  int16_t middle_finger_tip_x, middle_finger_tip_y; // 中指指尖
  int16_t ring_finger_mcp_x, ring_finger_mcp_y;     // 无名指根部
  int16_t ring_finger_pip_x, ring_finger_pip_y;     // 无名指第一关节

  int16_t ring_finger_dip_x, ring_finger_dip_y;   // 无名指第二关节
  int16_t ring_finger_tip_x, ring_finger_tip_y;   // 无名指指尖
  int16_t pinky_finger_mcp_x, pinky_finger_mcp_y; // 小指根部
  int16_t pinky_finger_pip_x, pinky_finger_pip_y; // 小指第一关节
  int16_t pinky_finger_dip_x, pinky_finger_dip_y; // 小指第二关节

  int16_t pinky_finger_tip_x, pinky_finger_tip_y; // 小指指尖
};

class PoseResult : public Result {
public:
  PoseResult(const void *buf);

public:
  int16_t nose_x, nose_y;
  int16_t leye_x, leye_y;
  int16_t reye_x, reye_y;
  int16_t lear_x, lear_y;
  int16_t rear_x, rear_y;

  int16_t lshoulder_x, lshoulder_y;
  int16_t rshoulder_x, rshoulder_y;
  int16_t lelbow_x, lelbow_y;
  int16_t relbow_x, relbow_y;
  int16_t lwrist_x, lwrist_y;

  int16_t rwrist_x, rwrist_y;
  int16_t lhip_x, lhip_y;
  int16_t rhip_x, rhip_y;
  int16_t lknee_x, lknee_y;
  int16_t rknee_x, rknee_y;

  int16_t lankle_x, lankle_y;
  int16_t rankle_x, rankle_y;
};
#endif // LARGE_MEMORY
#endif // DFROBOT_HUSKEYLENS_V2_RESULT_H
