#include <Result.h>

Result::Result(const void *buf) {
  PacketHead_t *head = (PacketHead_t *)buf;
  PacketData_t *packet = (PacketData_t *)head->data;
  type = head->cmd;
  ID = packet->ID;
  level = packet->level;
  xCenter = packet->first;
  yCenter = packet->second;
  width = packet->third;
  height = packet->fourth;
  confidence = packet->confidence;
  used = 0;
  String_t *pname = (String_t *)packet->payload;
  uint16_t headerSize = (uint16_t)((uint32_t)pname - (uint32_t)packet);
  DBG_KV("sizeof(String_t)=", sizeof(String_t));
  DBG_KV("pname->length=", pname->length);

  if (head->data_length <= headerSize) {
    DBG("no string data");
  } else if (headerSize + sizeof(String_t) * 2 + pname->length >
             head->data_length) {
    DBG("string data truncated");
  } else {
    String_t *pcontent =
        (String_t *)(packet->payload + sizeof(String_t) + pname->length);
    DBG_KV("pcontent->length=", pcontent->length);
    if (pname->length) {
      name = pname->toString();
    }
    if (headerSize + sizeof(String_t) * 2 + pname->length + pcontent->length <=
        head->data_length) {
      if (pcontent->length) {
        content = pcontent->toString();
      }
    } else {
      DBG("content data truncated");
    }
  }
  DBG_KV("type=", type);
  DBG_KV("ID=", ID);
  DBG_KV("xCenter=", xCenter);
  DBG_KV("yCenter=", yCenter);
  DBG_KV("width=", width);

  DBG_KV("height=", height);
  DBG_KV("name=", name);
  DBG_KV("content=", content);
}
Result::~Result() {}

#ifdef LARGE_MEMORY
#define READ_INT16(p)                                                          \
  ({                                                                           \
    int16_t v;                                                                 \
    memcpy(&v, p, sizeof(v));                                                  \
    p++;                                                                       \
    v;                                                                         \
  })
FaceResult::FaceResult(const void *buf) : Result(buf) {
  DBG("\n");
  PacketHead_t *head = (PacketHead_t *)buf;
  PacketData_t *packet = (PacketData_t *)head->data;
  String_t *pname = (String_t *)packet->payload;
  uint16_t headerSize = (uint16_t)((uint32_t)pname - (uint32_t)packet);
  if (head->data_length <= headerSize) {
    DBG("no string data");
    return;
  }
  if (headerSize + sizeof(String_t) * 2 + pname->length > head->data_length) {
    DBG("string data truncated");
    return;
  }
  String_t *pcontent =
      (String_t *)(packet->payload + sizeof(String_t) + pname->length);
  uint16_t faceDataSize = headerSize + sizeof(String_t) * 2 + pname->length +
                          pcontent->length;
  if (head->data_length < faceDataSize + sizeof(int16_t) * 10) {
    DBG("no externed data");
    return;
  }
  int16_t *face_data = (int16_t *)(packet->payload + pname->length +
                                   pcontent->length + sizeof(String_t) * 2);

  leye_x = READ_INT16(face_data);
  leye_y = READ_INT16(face_data);
  reye_x = READ_INT16(face_data);
  reye_y = READ_INT16(face_data);
  nose_x = READ_INT16(face_data);
  nose_y = READ_INT16(face_data);
  lmouth_x = READ_INT16(face_data);
  lmouth_y = READ_INT16(face_data);
  rmouth_x = READ_INT16(face_data);
  rmouth_y = READ_INT16(face_data);
}

HandResult::HandResult(const void *buf) : Result(buf) {
  DBG("\n");
  PacketHead_t *head = (PacketHead_t *)buf;
  PacketData_t *packet = (PacketData_t *)head->data;
  String_t *pname = (String_t *)packet->payload;
  uint16_t headerSize = (uint16_t)((uint32_t)pname - (uint32_t)packet);
  if (head->data_length <= headerSize) {
    DBG("no string data");
    return;
  }
  if (headerSize + sizeof(String_t) * 2 + pname->length > head->data_length) {
    DBG("string data truncated");
    return;
  }
  String_t *pcontent =
      (String_t *)(packet->payload + sizeof(String_t) + pname->length);
  uint16_t handDataSize = headerSize + sizeof(String_t) * 2 + pname->length +
                          pcontent->length;
  if (head->data_length < handDataSize + sizeof(int16_t) * 40) {
    DBG("no externed data");
    return;
  }
  int16_t *hand_data = (int16_t *)(packet->payload + pname->length +
                                   pcontent->length + sizeof(String_t) * 2);

  wrist_x = READ_INT16(hand_data); // 手腕
  wrist_y = READ_INT16(hand_data);
  DBG_HEX(wrist_x);
  DBG_HEX(wrist_y);
  thumb_cmc_x = READ_INT16(hand_data);
  thumb_cmc_y = READ_INT16(hand_data); // 拇指根部
  thumb_mcp_x = READ_INT16(hand_data);
  thumb_mcp_y = READ_INT16(hand_data); // 拇指中间关节
  thumb_ip_x = READ_INT16(hand_data);
  thumb_ip_y = READ_INT16(hand_data); // 拇指第二关节
  thumb_tip_x = READ_INT16(hand_data);
  thumb_tip_y = READ_INT16(hand_data); // 拇指指尖

  index_finger_mcp_x = READ_INT16(hand_data);
  index_finger_mcp_y = READ_INT16(hand_data); // 食指根部
  index_finger_pip_x = READ_INT16(hand_data);
  index_finger_pip_y = READ_INT16(hand_data); // 食指第一关节
  index_finger_dip_x = READ_INT16(hand_data);
  index_finger_dip_y = READ_INT16(hand_data); // 食指第二关节
  index_finger_tip_x = READ_INT16(hand_data);
  index_finger_tip_y = READ_INT16(hand_data); // 食指指尖
  middle_finger_mcp_x = READ_INT16(hand_data);
  middle_finger_mcp_y = READ_INT16(hand_data); // 中指根部

  middle_finger_pip_x = READ_INT16(hand_data);
  middle_finger_pip_y = READ_INT16(hand_data); // 中指第一关节
  middle_finger_dip_x = READ_INT16(hand_data);
  middle_finger_dip_y = READ_INT16(hand_data); // 中指第二关节
  middle_finger_tip_x = READ_INT16(hand_data);
  middle_finger_tip_y = READ_INT16(hand_data); // 中指指尖
  ring_finger_mcp_x = READ_INT16(hand_data);
  ring_finger_mcp_y = READ_INT16(hand_data); // 无名指根部
  ring_finger_pip_x = READ_INT16(hand_data);
  ring_finger_pip_y = READ_INT16(hand_data); // 无名指第一关节

  ring_finger_dip_x = READ_INT16(hand_data);
  ring_finger_dip_y = READ_INT16(hand_data); // 无名指第二关节
  ring_finger_tip_x = READ_INT16(hand_data);
  ring_finger_tip_y = READ_INT16(hand_data); // 无名指指尖
  pinky_finger_mcp_x = READ_INT16(hand_data);
  pinky_finger_mcp_y = READ_INT16(hand_data); // 小指根部
  pinky_finger_pip_x = READ_INT16(hand_data);
  pinky_finger_pip_y = READ_INT16(hand_data); // 小指第一关节
  pinky_finger_dip_x = READ_INT16(hand_data);
  pinky_finger_dip_y = READ_INT16(hand_data); // 小指第二关节
  DBG_HEX(pinky_finger_dip_x);
  DBG_HEX(pinky_finger_dip_y);
  pinky_finger_tip_x = READ_INT16(hand_data);
  pinky_finger_tip_y = READ_INT16(hand_data); // 小指指尖
  DBG_HEX(pinky_finger_tip_x);
  DBG_HEX(pinky_finger_tip_y);
}

PoseResult::PoseResult(const void *buf) : Result(buf) {
  DBG("begin parse\n");
  PacketHead_t *head = (PacketHead_t *)buf;
  PacketData_t *packet = (PacketData_t *)head->data;
  String_t *pname = (String_t *)packet->payload;
  uint16_t headerSize = (uint16_t)((uint32_t)pname - (uint32_t)packet);
  if (head->data_length <= headerSize) {
    DBG("no string data");
    return;
  }
  if (headerSize + sizeof(String_t) * 2 + pname->length > head->data_length) {
    DBG("string data truncated");
    return;
  }
  String_t *pcontent =
      (String_t *)(packet->payload + sizeof(String_t) + pname->length);
  uint16_t poseDataSize = headerSize + sizeof(String_t) * 2 + pname->length +
                          pcontent->length;
  if (head->data_length < poseDataSize + sizeof(int16_t) * 34) {
    DBG("no externed data");
    return;
  }
  DBG("hax externed data");
  DBG_PRINTLN(head->data_length - poseDataSize);
  int16_t *pose_data = (int16_t *)(packet->payload + pname->length +
                                   pcontent->length + sizeof(String_t) * 2);
  nose_x = READ_INT16(pose_data);
  nose_y = READ_INT16(pose_data);
  leye_x = READ_INT16(pose_data);
  leye_y = READ_INT16(pose_data);
  reye_x = READ_INT16(pose_data);
  reye_y = READ_INT16(pose_data);
  lear_x = READ_INT16(pose_data);
  lear_y = READ_INT16(pose_data);
  rear_x = READ_INT16(pose_data);
  rear_y = READ_INT16(pose_data);
  lshoulder_x = READ_INT16(pose_data);
  lshoulder_y = READ_INT16(pose_data);
  rshoulder_x = READ_INT16(pose_data);
  rshoulder_y = READ_INT16(pose_data);
  lelbow_x = READ_INT16(pose_data);
  lelbow_y = READ_INT16(pose_data);
  relbow_x = READ_INT16(pose_data);
  relbow_y = READ_INT16(pose_data);
  lwrist_x = READ_INT16(pose_data);
  lwrist_y = READ_INT16(pose_data);
  rwrist_x = READ_INT16(pose_data);
  rwrist_y = READ_INT16(pose_data);
  lhip_x = READ_INT16(pose_data);
  lhip_y = READ_INT16(pose_data);
  rhip_x = READ_INT16(pose_data);
  rhip_y = READ_INT16(pose_data);
  lknee_x = READ_INT16(pose_data);
  lknee_y = READ_INT16(pose_data);
  rknee_x = READ_INT16(pose_data);
  rknee_y = READ_INT16(pose_data);
  lankle_x = READ_INT16(pose_data);
  lankle_y = READ_INT16(pose_data);
  rankle_x = READ_INT16(pose_data);
  rankle_y = READ_INT16(pose_data);
  DBG("end parse\n");
}

#endif