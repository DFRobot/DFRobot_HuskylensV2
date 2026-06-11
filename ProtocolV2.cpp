#include <ProtocolV2.h>

static uint8_t send_buffer[CMD_BUFFER_SIZE];
static uint8_t receive_buffer[FRAME_BUFFER_SIZE];

static short send_index = 0;
static short receive_index = 0;

static bool send_fail = false;
static bool receive_fail = false;

static short content_current = 0;
static short content_end = 0;
static bool content_read_end = false;

uint8_t *husky_lens_protocol_write_begin(eAlgorithm_t algo, uint8_t command) {
  send_fail = false;
  send_buffer[HEADER_0_INDEX] = 0x55;
  send_buffer[HEADER_1_INDEX] = 0xAA;
  send_buffer[COMMAND_INDEX] = command;
  send_buffer[ALGO_INDEX] = algo;
  send_index = CONTENT_INDEX;
  return (uint8_t *)send_buffer;
}

void husky_lens_protocol_write_uint8(uint8_t content) {
  if (send_index + sizeof(content) >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  memcpy(send_buffer + send_index, &content, sizeof(content));
  send_index += sizeof(content);
}

void husky_lens_protocol_write_int16(int16_t content) {
  if (send_index + sizeof(content) >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  memcpy(send_buffer + send_index, &content, sizeof(content));
  send_index += sizeof(content);
}

void husky_lens_protocol_write_zero_bytes(int16_t num) {
  if (send_index + num >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  memset(send_buffer + send_index, 0, num);
  send_index += num;
}

void husky_lens_protocol_write_string(String str) {
  if (send_index + str.length() >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  send_buffer[send_index++] = str.length();
  memcpy(send_buffer + send_index, str.c_str(), str.length());
  send_index += str.length();
}

void husky_lens_protocol_write_int32(int32_t content) {
  if (send_index + sizeof(content) >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  memcpy(send_buffer + send_index, &content, sizeof(content));
  send_index += sizeof(content);
}

void husky_lens_protocol_write_float(float content) {
  if (send_index + sizeof(content) >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  memcpy(send_buffer + send_index, &content, sizeof(content));
  send_index += sizeof(content);
}

void husky_lens_protocol_write_buffer_uint8(uint8_t *content, uint32_t length) {
  if (send_index + length >= CMD_BUFFER_SIZE) {
    send_fail = true;
    return;
  }
  memcpy(send_buffer + send_index, content, length);
  send_index += length;
}

int husky_lens_protocol_write_end() {
  if (send_fail) {
    return 0;
  }
  if (send_index + 1 >= CMD_BUFFER_SIZE) {
    return 0;
  }
  send_buffer[CONTENT_SIZE_INDEX] = send_index - CONTENT_INDEX;
  uint8_t sum = 0;
  for (int i = 0; i < send_index; i++) {
    sum += send_buffer[i];
  }
  send_buffer[send_index] = sum;
  send_index++;
  return send_index;
}
bool validateCheckSum() {
  uint8_t stackSumIndex = receive_buffer[CONTENT_SIZE_INDEX] + CONTENT_INDEX;
  uint8_t sum = 0;
  uint8_t i;
  // calculate the checksum
  for (i = 0; i < stackSumIndex; i++) {
    sum += receive_buffer[i];
  }
  if (sum != receive_buffer[stackSumIndex]) {
    DBG("checksum error [expected] [received]\n");
    DBG_HEX(sum);
    DBG_HEX(receive_buffer[stackSumIndex]);
  }
  return (sum == receive_buffer[stackSumIndex]);
}
bool husky_lens_protocol_receive(uint8_t data) {
  // DBG_HEX(receive_index);
  switch (receive_index) {
  case HEADER_0_INDEX:
    if (data != 0x55) {
      receive_index = 0;
      return false;
    }
    receive_buffer[HEADER_0_INDEX] = 0x55;
    break;
  case HEADER_1_INDEX:
    if (data != 0xaa) {
      receive_index = 0;
      return false;
    }
    receive_buffer[HEADER_1_INDEX] = 0xaa;
    break;
  case COMMAND_INDEX:
    receive_buffer[COMMAND_INDEX] = data;
    break;
  case ALGO_INDEX:
    receive_buffer[ALGO_INDEX] = data;
    break;
  case CONTENT_SIZE_INDEX:
    if ((int)receive_index >= FRAME_BUFFER_SIZE - PROTOCOL_SIZE) {
      receive_index = 0;
      return false;
    }
    receive_buffer[CONTENT_SIZE_INDEX] = data;
    break;
  default:
    receive_buffer[receive_index] = data;
    if (receive_index == receive_buffer[CONTENT_SIZE_INDEX] + CONTENT_INDEX) {
      content_end = receive_index;
      receive_index = 0;
      DBG_PRINTLN("<--");
      DBG_HEX_ARRAY(receive_buffer,
                    receive_buffer[CONTENT_SIZE_INDEX] + PROTOCOL_SIZE);
      DBG_PRINT("\n");
      return validateCheckSum();
    }
    break;
  }
  receive_index++;
  return false;
}

bool ProtocolV2::wait(uint8_t command) {
  timerBegin();
  while (!timerAvailable()) {
    if (protocolAvailable()) {
      if (command == receive_buffer[COMMAND_INDEX]) {
        DBG("return true\n");
        return true;
      } else {
        DBG("return false\n");
        DBG_HEX(command);
        DBG_HEX(receive_buffer[COMMAND_INDEX]);
        return false;
      }
    }
  }
  DBG("\n");
  return false;
}

void ProtocolV2::protocolWrite(uint8_t *buffer, int length) {
  if (wire) {
    DBG_PRINTLN("-->");
    DBG_HEX_ARRAY(buffer, length);
    DBG_PRINT("\n");
    timeOutDuration = 5000;
    wire->setClock(100000);
    uint16_t packets = length / MAX_PL_LEN;
    uint16_t remain = length % MAX_PL_LEN;
    for(uint16_t i = 0; i < packets; i++){
        wire->beginTransmission(addr);
        wire->write(buffer + i * MAX_PL_LEN, MAX_PL_LEN);
        wire->endTransmission();
    }
    if(remain){
        wire->beginTransmission(addr);
        wire->write(buffer + packets * MAX_PL_LEN, remain);
        wire->endTransmission();
    }

  } else if (stream) {
    DBG_PRINTLN("-->");
    DBG_HEX_ARRAY(buffer, length);
    DBG_PRINT("\n");
    timeOutDuration = 5000;
    stream->write(buffer, length);
    stream->flush();
  }
}
void ProtocolV2::timerBegin() { timeOutTimer = millis(); }
bool ProtocolV2::timerAvailable() {
  return (millis() - timeOutTimer > timeOutDuration);
}
bool ProtocolV2::protocolAvailable() {
  if (wire) {
    if (!wire->available()) {
      wire->setClock(100000);
      wire->requestFrom(addr, 16);
    }
    while (wire->available()) {
      uint8_t result = wire->read();
      if (husky_lens_protocol_receive(result)) {
        DBG("\n");
        return true;
      }
    }
  } else if (stream) {
    while (stream->available()) {
      uint8_t c = stream->read();
    //   DBG(c, HEX);
      if (husky_lens_protocol_receive(c)) {
        DBG("full packet\n");
        return true;
      }
    }
  }

  return false;
}
bool ProtocolV2::knock(void) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_KNOCK);
#ifdef LARGE_MEMORY
  husky_lens_protocol_write_uint8(BOARD_LARGE_RAM);
#else
  husky_lens_protocol_write_uint8(BOARD_SMALL_RAM);
#endif
  for (uint8_t i = 0; i < 9; i++) {
    husky_lens_protocol_write_uint8(0);
  }
  int length = husky_lens_protocol_write_end();

  for (uint8_t i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    delay(10);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::switchAlgorithm(eAlgorithm_t algo) {
  DBG("\n");
  bool ret = false;

  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_SET_ALGORITHM);

  husky_lens_protocol_write_uint8((uint8_t)algo);
  husky_lens_protocol_write_zero_bytes(9);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

// get result ,获取所有result，将统计信息保存heap中
// 返回result的数目
int8_t ProtocolV2::getResult(eAlgorithm_t &algo) {
  DBG("\n");
  uint8_t *buffer = husky_lens_protocol_write_begin(algo, COMMAND_GET_RESULT);
  int length = husky_lens_protocol_write_end();
  int8_t _count = 0;
  int8_t i = 0;
  PacketData_t info;
  PacketHead_t *head = (PacketHead_t *)receive_buffer;
  for (i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_INFO)) {
      PacketData_t *packet = (PacketData_t *)head->data;
      // algo = (eAlgorithm_t)head->algo_id;
      maxID = packet->maxID;
      info.total_results = packet->total_results;
      info.total_results_learned = packet->total_results_learned;
      info.total_blocks = packet->total_blocks;
      info.total_blocks_learned = packet->total_blocks_learned;
      DBG_PRINT("info.total_results=");
      DBG(info.total_results);
      DBG_PRINT("info.total_blocks=");
      DBG(info.total_blocks);
      if (info.total_results > MAX_RESULT_NUM) {
        info.total_results = MAX_RESULT_NUM;
      }
      if (info.total_blocks > MAX_RESULT_NUM) {
        info.total_blocks = MAX_RESULT_NUM;
      }

      break;
    }
  }
  if (i == retry) {
    DBG("i==retry");
    return -1;
  }

  for (int i = 0; i < info.total_blocks; i++) {
    DBG("\n");
    if (wait(COMMAND_RETURN_BLOCK)) {
      _count++;
#ifdef LARGE_MEMORY
      if (algo == ALGORITHM_FACE_RECOGNITION) {
        DBG("new Face Result\n");
        result[i] = new FaceResult((const void *)receive_buffer);
      } else if (algo == ALGORITHM_HAND_RECOGNITION) {
        DBG("new Hand Result\n");
        result[i] = new HandResult((const void *)receive_buffer);
      } else if (algo == ALGORITHM_POSE_RECOGNITION) {
        DBG("new Pose Result\n");
        result[i] = new PoseResult((const void *)receive_buffer);
      } else {
        DBG("new Result\n");
        result[i] = new Result((const void *)receive_buffer);
      }
#else
      result[i] = new Result(receive_buffer);
#endif
    }
  }
  for (int i = info.total_blocks; i < info.total_results; i++) {
    DBG("\n");
    if (wait(COMMAND_RETURN_ARROW)) {
      _count++;
      result[i] = new Result(receive_buffer);
    }
  }
  DBG("ProtocolV2 return");
  DBG_HEX(_count);
  return _count;
}

#ifdef LARGE_MEMORY
bool ProtocolV2::doSetMultiAlgorithm(eAlgorithm_t algo0, eAlgorithm_t algo1,
                                     eAlgorithm_t algo2) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
      ALGORITHM_ANY, COMMAND_SET_MULTI_ALGORITHM);
  uint8_t multiAlgoNum = 0;
  int16_t algos[3] = {ALGORITHM_ANY, ALGORITHM_ANY, ALGORITHM_ANY};
  DBG("\n");
  if (algo0 != ALGORITHM_ANY) {
    multiAlgoNum++;
    algos[0] = algo0;
  }
  DBG("\n");
  if (algo1 != ALGORITHM_ANY) {
    multiAlgoNum++;
    algos[1] = algo1;
  }
  DBG("\n");
  if (algo2 != ALGORITHM_ANY) {
    multiAlgoNum++;
    algos[2] = algo2;
  }
  DBG("\n");

  husky_lens_protocol_write_uint8(multiAlgoNum);
  DBG("\n");
  husky_lens_protocol_write_uint8(0);
  DBG("\n");
  for (uint8_t i = 0; i < 4; i++) {
    if (i < multiAlgoNum) {
      husky_lens_protocol_write_int16(algos[i]);
    } else {
      husky_lens_protocol_write_int16(0);
    }
  }
  DBG("----");
  DBG_HEX_ARRAY(buffer, 16);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
      return true;
    }
  }
  return false;
}

bool ProtocolV2::setMultiAlgorithmRatio(int8_t ratio0, int8_t ratio1,
                                        int8_t ratio2) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
      ALGORITHM_ANY, COMMAND_SET_MULTI_ALGORITHM_RATIO);
  uint8_t multiAlgoNum = 0;
  DBG("\n");
  int16_t ratios[3];
  if (ratio0 != -1) {
    multiAlgoNum++;
    ratios[0] = ratio0;
  }
  DBG("\n");
  if (ratio1 != -1) {
    multiAlgoNum++;
    ratios[1] = ratio1;
  }
  DBG("\n");
  if (ratio2 != -1) {
    multiAlgoNum++;
    ratios[2] = ratio2;
  }
  DBG("\n");
  husky_lens_protocol_write_uint8(multiAlgoNum);
  husky_lens_protocol_write_uint8(0);
  DBG("\n");
  for (uint8_t i = 0; i < 4; i++) {
    if (i < multiAlgoNum) {
      husky_lens_protocol_write_int16(ratios[i]);
    } else {
      husky_lens_protocol_write_int16(0);
    }
  }
  DBG("\n");
  int length = husky_lens_protocol_write_end();
  DBG("\n");
  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    DBG("\n");
    if (wait(COMMAND_RETURN_ARGS)) {
      DBG("\n");
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}
#endif
uint8_t ProtocolV2::learnBlock(eAlgorithm_t algo, int16_t x, int16_t y,
                               int16_t width, int16_t height) {
  DBG("\n");
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_ACTION_LEARN_BLOCK);
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_uint8(0);

  husky_lens_protocol_write_int16(x);
  husky_lens_protocol_write_int16(y);
  husky_lens_protocol_write_int16(width);
  husky_lens_protocol_write_int16(height);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;
      uint8_t id = packet->first;
      return id;
    }
  }
  return 0;
}

// 后续返回值修改为String
String ProtocolV2::takePhoto(eResolution_t resolution) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_TAKE_PHOTO);
  husky_lens_protocol_write_uint8(resolution);
  husky_lens_protocol_write_zero_bytes(9);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue != 0)
        return "";

      String_t *name = (String_t *)packet->payload;
      return name->toString();
    }
  }
  return "";
}

// 后续返回值修改为String
String ProtocolV2::takeScreenshot() {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
      ALGORITHM_ANY, COMMAND_ACTION_TAKE_SCREENSHOT);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue != 0)
        return "";

      String_t *name = (String_t *)packet->payload;
      return name->toString();
    }
  }
  return "";
}

uint8_t ProtocolV2::learn(eAlgorithm_t algo) {
  DBG("\n");
  uint8_t *buffer = husky_lens_protocol_write_begin(algo, COMMAND_ACTION_LEARN);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;
      uint8_t id = packet->first;
      return id;
    }
  }
  return 0;
}

bool ProtocolV2::forget(eAlgorithm_t algo) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_ACTION_FORGET);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::drawRect(uint32_t color, uint8_t lineWidth, int16_t x,
                          int16_t y, int16_t width, int16_t height) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_DRAW_RECT);
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_uint8(lineWidth);

  husky_lens_protocol_write_int16(x);
  husky_lens_protocol_write_int16(y);
  husky_lens_protocol_write_int16(width);
  husky_lens_protocol_write_int16(height);
  husky_lens_protocol_write_int16(0);
  husky_lens_protocol_write_int32(color);

  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::drawUniqueRect(uint32_t color, uint8_t lineWidth, int16_t x,
                                int16_t y, int16_t width, int16_t height) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
      ALGORITHM_ANY, COMMAND_ACTION_DRAW_UNIQUE_RECT);
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_uint8(lineWidth);

  husky_lens_protocol_write_int16(x);
  husky_lens_protocol_write_int16(y);
  husky_lens_protocol_write_int16(width);
  husky_lens_protocol_write_int16(height);
  husky_lens_protocol_write_int16(0);
  husky_lens_protocol_write_int32(color);

  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::clearRect() {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_CLEAR_RECT);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::drawText(uint32_t color, uint8_t fontSize, int16_t x,
                          int16_t y, String text) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_DRAW_TEXT);
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_uint8(fontSize);

  husky_lens_protocol_write_int16(x);
  husky_lens_protocol_write_int16(y);
  husky_lens_protocol_write_int16(0);
  husky_lens_protocol_write_int16(0);
  husky_lens_protocol_write_uint8(text.length());
  for (uint8_t i = 0; i < text.length(); i++) {
    husky_lens_protocol_write_uint8(text[i]);
  }
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_int32(color);

  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::clearText() {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_CLEAR_TEXT);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::saveKnowledges(eAlgorithm_t algo, uint8_t knowledgeID) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_ACTION_SAVE_KNOWLEDGES);
  husky_lens_protocol_write_uint8(knowledgeID);
  husky_lens_protocol_write_zero_bytes(9);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::loadKnowledges(eAlgorithm_t algo, uint8_t knowledgeID) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_ACTION_LOAD_KNOWLEDGES);
  husky_lens_protocol_write_uint8(knowledgeID);
  husky_lens_protocol_write_zero_bytes(9);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::playMusic(String name, int16_t volume) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(ALGORITHM_ANY, COMMAND_ACTION_PLAY_MUSIC);
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_uint8(0);

  husky_lens_protocol_write_int16(volume);
  husky_lens_protocol_write_zero_bytes(6);
  husky_lens_protocol_write_string(name);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::setNameByID(eAlgorithm_t algo, uint8_t id, String name) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_SET_NAME_BY_ID);
  husky_lens_protocol_write_uint8(id);
  husky_lens_protocol_write_zero_bytes(9);
  husky_lens_protocol_write_string(name);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      return ret;
    }
  }
  return false;
}

bool ProtocolV2::getAlgoParamBool(eAlgorithm_t algo, String key) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_GET_ALGO_PARAM);
  husky_lens_protocol_write_zero_bytes(10);
  husky_lens_protocol_write_string(key);
  husky_lens_protocol_write_uint8(0);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        if (packet->first) {
          ret = true;
        }
      }
      break;
    }
  }
  return ret;
}

float ProtocolV2::getAlgoParamFloat(eAlgorithm_t algo, String key) {
  DBG("\n");
  float ret = 0.0;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_GET_ALGO_PARAM);
  husky_lens_protocol_write_zero_bytes(10);
  husky_lens_protocol_write_string(key);
  husky_lens_protocol_write_uint8(0);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        memcpy(&ret, &packet->first, sizeof(ret));
      }
      return ret;
    }
  }
  return 0.0;
}

String ProtocolV2::getAlgoParamString(eAlgorithm_t algo, String key) {
  DBG("\n");
  String ret = "";
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_GET_ALGO_PARAM);
  husky_lens_protocol_write_zero_bytes(10);
  husky_lens_protocol_write_string(key);
  husky_lens_protocol_write_uint8(0);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        String_t *value = (String_t *)packet->payload;
        ret = value->toString();
      }
      return ret;
    }
  }
  return ret;
}

bool ProtocolV2::updateAlgoParams(eAlgorithm_t algo) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_UPDATE_ALGORITHM_PARAMS);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}

bool ProtocolV2::setAlgoParamBool(eAlgorithm_t algo, String key, bool value) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_SET_ALGO_PARAMS);
  husky_lens_protocol_write_uint8(1);
  husky_lens_protocol_write_uint8(0);

  husky_lens_protocol_write_int16(value);
  husky_lens_protocol_write_zero_bytes(6);
  husky_lens_protocol_write_string(key);
  husky_lens_protocol_write_uint8(0);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}

bool ProtocolV2::setAlgoParamFloat(eAlgorithm_t algo, String key, float value) {
  DBG("\n");
  bool ret = false;
  int16_t *value16 = (int16_t *)&value;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_SET_ALGO_PARAMS);
  husky_lens_protocol_write_uint8(2);
  husky_lens_protocol_write_uint8(0);

  husky_lens_protocol_write_int16(value16[0]);
  husky_lens_protocol_write_int16(value16[1]);
  husky_lens_protocol_write_int16(0);
  husky_lens_protocol_write_int16(0);
  husky_lens_protocol_write_string(key);
  husky_lens_protocol_write_uint8(0);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}

bool ProtocolV2::setAlgoParamString(eAlgorithm_t algo, String key,
                                    String value) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer =
      husky_lens_protocol_write_begin(algo, COMMAND_SET_ALGO_PARAMS);
  husky_lens_protocol_write_zero_bytes(10);
  husky_lens_protocol_write_string(key);
  husky_lens_protocol_write_string(value);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}

bool ProtocolV2::startRecording(eMediaType_t mediaType, int16_t duration,
                                String filename, eResolution_t resolution) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
      ALGORITHM_ANY, COMMAND_ACTION_START_RECORDING);
  husky_lens_protocol_write_uint8(resolution);
  husky_lens_protocol_write_uint8(mediaType);

  husky_lens_protocol_write_int16(duration);
  husky_lens_protocol_write_zero_bytes(6);
  if (filename.length() > 0) {
    husky_lens_protocol_write_string(filename);
  }
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}
bool ProtocolV2::stopRecording(eMediaType_t mediaType) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
      ALGORITHM_ANY, COMMAND_ACTION_STOP_RECORDING);
  husky_lens_protocol_write_uint8(0);
  husky_lens_protocol_write_uint8(mediaType);
  husky_lens_protocol_write_zero_bytes(8);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}


bool ProtocolV2::e2eStartRecording(void) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
    ALGORITHM_ANY, COMMAND_ACTION_E2E_START_RECORDING);
  husky_lens_protocol_write_zero_bytes(10);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}

bool ProtocolV2::e2eStopRecording(void) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
    ALGORITHM_ANY, COMMAND_ACTION_E2E_STOP_RECORDING);
  husky_lens_protocol_write_zero_bytes(10);
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}

bool ProtocolV2::e2eSendAnnotation(String annotation) {
  DBG("\n");
  bool ret = false;
  uint8_t *buffer = husky_lens_protocol_write_begin(
    ALGORITHM_ANY, COMMAND_ACTION_E2E_SEND_ANNOTATION);
  husky_lens_protocol_write_zero_bytes(10);
  if (annotation.length() > 0) {
    husky_lens_protocol_write_string(annotation);
  }
  int length = husky_lens_protocol_write_end();

  for (int i = 0; i < retry; i++) {
    protocolWrite(buffer, length);
    if (wait(COMMAND_RETURN_ARGS)) {
      PacketHead_t *head = (PacketHead_t *)receive_buffer;
      PacketData_t *packet = (PacketData_t *)head->data;

      if (packet->retValue == 0) {
        ret = true;
      }
      break;
    }
  }
  return ret;
}
