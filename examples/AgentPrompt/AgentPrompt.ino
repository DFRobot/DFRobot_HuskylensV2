/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 This example demonstrates the xiaozhi agent chat workflow of HUSKYLENS V2:
 send a text prompt, poll the agent status (idle/processing/broadcasting)
 until the response is ready, then fetch and print the full response.

 The agent APIs are only available on large-memory platforms
 (ESP32/ESP8266/NRF52/micro:bit), not on AVR boards like Uno.
 ***************************************************
 Created 2026-06-11
 By [thdyyl](yuanlong.yu@dfrobot.com)

 The MIT License (MIT).
 See <https://opensource.org/licenses/MIT> for details.
 All above must be included in any redistribution
 ****************************************************/

/***********Notice and Trouble shooting***************
 1.Connection and Diagram can be found here
 <https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336#target_23>
 2.Agent APIs require a large-memory board (ESP32 recommended).
 ****************************************************/

#include "DFRobot_HuskylensV2.h"

HuskylensV2 huskylens;

// 轮询总超时：云端生成长回答可能需要数十秒，超时后放弃本轮，避免死循环
#define AGENT_POLL_TIMEOUT_MS 90000
#define AGENT_POLL_INTERVAL_MS 500

void setup() {
  Serial.begin(115200);
  Wire.begin();
  while (!huskylens.begin(Wire)) {
    Serial.println(F("Begin failed!"));
    Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS "
                     "(System Settings>>Protocol Type>> I2C/UART)"));
    Serial.println(F("2.Please recheck the connection."));
    Serial.println(F("\tgreen line >> SDA/TX; blue line >> SCL/RX"));
    delay(200);
  }
}

// 把枚举状态转成可读字符串，便于串口观察
static const char *agentStatusStr(eAgentStatus_t status) {
  switch (status) {
  case AGENT_PROCESSING:
    return "processing";   // 已提交，等待云端生成
  case AGENT_BROADCASTING:
    return "broadcasting"; // 正在播报回答
  case AGENT_IDLE:
  default:
    return "idle";
  }
}

void loop() {
  Serial.println();
  Serial.println("[AgentPrompt] Start ...");

  if (!huskylens.sendAgentPrompt("tell me a long joke")) {
    Serial.println("[AgentPrompt] Send prompt failed");
    delay(1000);
    return;
  }

  // 等设备开始处理后再查就绪标志：刚发完 prompt 时 agent 尚未进入
  // processing，可能读到上一轮遗留的 ready 状态，导致跳过轮询直接取回答
  delay(2000);

  // 轮询直到回答就绪或总超时
  uint32_t start = millis();
  while (!huskylens.isAgentResponseReady()) {
    eAgentStatus_t status = huskylens.getAgentStatus();
    if (status != AGENT_QUERY_FAILED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
    } else {
      Serial.println(F("agent status: <query failed>"));
    }
    if (millis() - start > AGENT_POLL_TIMEOUT_MS) {
      Serial.println("[AgentPrompt] Poll timeout, give up");
      delay(1000);
      return;
    }
    delay(AGENT_POLL_INTERVAL_MS);
  }

  String response;
  response = huskylens.getAgentResponse();
  if (response.length() > 0) {
    Serial.println("[AgentPrompt] Response : " + response);
  } else {
    Serial.println("[AgentPrompt] Response failed");
  }
  delay(5000);


  if (!huskylens.sendAgentPrompt("打开闪光灯")) {
    Serial.println("[AgentPrompt] Send prompt failed");
    delay(1000);
    return;
  }

  // 等设备开始处理后再查就绪标志：刚发完 prompt 时 agent 尚未进入
  // processing，可能读到上一轮遗留的 ready 状态，导致跳过轮询直接取回答
  delay(2000);

  // 轮询直到回答就绪或总超时
  start = millis();
  while (!huskylens.isAgentResponseReady()) {
    eAgentStatus_t status = huskylens.getAgentStatus();
    if (status != AGENT_QUERY_FAILED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
    } else {
      Serial.println(F("agent status: <query failed>"));
    }
    if (millis() - start > AGENT_POLL_TIMEOUT_MS) {
      Serial.println("[AgentPrompt] Poll timeout, give up");
      delay(1000);
      return;
    }
    delay(AGENT_POLL_INTERVAL_MS);
  }


  response = huskylens.getAgentResponse();
  if (response.length() > 0) {
    Serial.println("[AgentPrompt] Response : " + response);
  } else {
    Serial.println("[AgentPrompt] Response failed");
  }
  delay(5000);



  if (!huskylens.sendAgentPrompt("关闭闪光灯")) {
    Serial.println("[AgentPrompt] Send prompt failed");
    delay(1000);
    return;
  }

  // 等设备开始处理后再查就绪标志：刚发完 prompt 时 agent 尚未进入
  // processing，可能读到上一轮遗留的 ready 状态，导致跳过轮询直接取回答
  delay(2000);

  // 轮询直到回答就绪或总超时
  start = millis();
  while (!huskylens.isAgentResponseReady()) {
    eAgentStatus_t status = huskylens.getAgentStatus();
    if (status != AGENT_QUERY_FAILED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
    } else {
      Serial.println(F("agent status: <query failed>"));
    }
    if (millis() - start > AGENT_POLL_TIMEOUT_MS) {
      Serial.println("[AgentPrompt] Poll timeout, give up");
      delay(1000);
      return;
    }
    delay(AGENT_POLL_INTERVAL_MS);
  }


  response = huskylens.getAgentResponse();
  if (response.length() > 0) {
    Serial.println("[AgentPrompt] Response : " + response);
  } else {
    Serial.println("[AgentPrompt] Response failed");
  }
  delay(5000);

}