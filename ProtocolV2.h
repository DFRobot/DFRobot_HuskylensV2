/*
纯底层通信，包含了通用通信协议的处理
 */
#ifndef DFROBOT_HUSKEYLENS_V2_PROTOCOL_H
#define DFROBOT_HUSKEYLENS_V2_PROTOCOL_H
#include <Result.h>

// 小内存（AVR）只使用基类的内容，大内存MCU（esp32 microbit）可以使用派生类内容
class ProtocolV2 {
public:
  ProtocolV2() : result{} {};
  ~ProtocolV2() {};

  void protocolWrite(uint8_t *buffer, int length);
  void timerBegin();
  bool timerAvailable();
  bool protocolAvailable();
  bool wait(uint8_t command = 0);
  bool knock(void);
  int8_t getResult(eAlgorithm_t &algo);
  uint8_t learn(eAlgorithm_t algo);
  uint8_t learnBlock(eAlgorithm_t algo, int16_t x, int16_t y, int16_t width,
                     int16_t height);
  bool forget(eAlgorithm_t algo);
  bool switchAlgorithm(eAlgorithm_t algo);
  String takePhoto(eResolution_t resolution = RESOLUTION_1280x720);
  String takeScreenshot();

  bool drawUniqueRect(uint32_t color, uint8_t lineWidth, int16_t x, int16_t y,
                      int16_t width, int16_t height);
  bool drawRect(uint32_t color, uint8_t lineWidth, int16_t x, int16_t y,
                int16_t width, int16_t height);
  bool clearRect();
  bool drawText(uint32_t color, uint8_t fontSize, int16_t x, int16_t y,
                String text);
  bool clearText();
  bool saveKnowledges(eAlgorithm_t algo, uint8_t knowledgeID);
  bool loadKnowledges(eAlgorithm_t algo, uint8_t knowledgeID);
  bool playMusic(String name, int16_t volume);
  bool setNameByID(eAlgorithm_t algo, uint8_t id, String name);

#ifdef LARGE_MEMORY
  bool doSetMultiAlgorithm(eAlgorithm_t algo0, eAlgorithm_t algo1,
                           eAlgorithm_t algo2 = ALGORITHM_ANY);
  bool setMultiAlgorithmRatio(int8_t ratio0, int8_t ratio1, int8_t ratio2 = -1);
#endif
public:
  bool getAlgoParamBool(eAlgorithm_t algo, String key);
  float getAlgoParamFloat(eAlgorithm_t algo, String key);
  String getAlgoParamString(eAlgorithm_t algo, String key);

  bool setAlgoParamBool(eAlgorithm_t algo, String key, bool value);
  bool setAlgoParamFloat(eAlgorithm_t algo, String key, float value);
  bool setAlgoParamString(eAlgorithm_t algo, String key, String value);
  bool updateAlgoParams(eAlgorithm_t algo);
  bool startRecording(eMediaType_t mediaType, int16_t duration = -1,
                      String filename = "",
                      eResolution_t resolution = RESOLUTION_DEFAULT);
  bool stopRecording(eMediaType_t mediaType);

  bool e2eStartRecording(void);
  bool e2eStopRecording(void);
  bool e2eSendAnnotation(String annotation);

public:
  int16_t maxID;
  int16_t total_results;
  int16_t total_blocks;
  int16_t total_arrows;
  Result *result[MAX_RESULT_NUM];
  int16_t retry = 5;
  TwoWire *wire = NULL;
  Stream *stream = NULL;
  unsigned long timeOutDuration = 5000;
  unsigned long timeOutTimer;
  const uint8_t addr = 0x50;
};

#endif // DFROBOT_HUSKEYLENS_V2_RESULT_H