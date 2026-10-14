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

// Total polling timeout: the cloud may take tens of seconds to generate a
// long answer; give up this round on timeout to avoid an endless loop
#define AGENT_POLL_TIMEOUT_MS 90000
#define AGENT_POLL_INTERVAL_MS 500


// Convert the enum status to a readable string for serial monitoring
static const char *agentStatusStr(eAgentStatus_t status) {
  switch (status) {
  case AGENT_PROCESSING:
    return "processing";   // Submitted, waiting for the cloud to generate
  case AGENT_BROADCASTING:
    return "broadcasting"; // Broadcasting the answer
  case AGENT_DISABLED:
    return "disabled";     // The agent switch is not turned on
  case AGENT_IDLE:
  default:
    return "idle";
  }
}

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


void loop() {
  Serial.println();
  Serial.println("[AgentPrompt] Start ...");

  if (!huskylens.sendAgentPrompt("tell me a long joke")) {
    Serial.println("[AgentPrompt] Send prompt failed");
    eAgentStatus_t status = huskylens.getAgentStatus();
    if (status != AGENT_QUERY_FAILED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
    } else {
      Serial.println(F("agent status: <query failed>"));
    }
    delay(1000);
    return;
  }

  // Wait for the device to start processing before checking the ready flag:
  // right after sending a prompt the agent has not entered processing yet,
  // so a stale ready state from the previous round may be read, which would
  // skip polling and fetch the answer immediately
  delay(2000);

  // Poll until the answer is ready or the total timeout expires
  uint32_t start = millis();
  while (!huskylens.isAgentResponseReady()) {
    eAgentStatus_t status = huskylens.getAgentStatus();
    if(status == AGENT_DISABLED){
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
      return;
    }else if (status != AGENT_QUERY_FAILED) {
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


  if (!huskylens.sendAgentPrompt("Turn on the flashlight")) {
    Serial.println("[AgentPrompt] Send prompt failed");
    delay(1000);
    return;
  }

  // Wait for the device to start processing before checking the ready flag:
  // right after sending a prompt the agent has not entered processing yet,
  // so a stale ready state from the previous round may be read, which would
  // skip polling and fetch the answer immediately
  delay(2000);

  // Poll until the answer is ready or the total timeout expires
  start = millis();
  while (!huskylens.isAgentResponseReady()) {
    eAgentStatus_t status = huskylens.getAgentStatus();
    if (status == AGENT_DISABLED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
      return;
    }else if (status != AGENT_QUERY_FAILED) {
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



  if (!huskylens.sendAgentPrompt("Turn off the flashlight")) {
    Serial.println("[AgentPrompt] Send prompt failed");
    delay(1000);
    return;
  }

  // Wait for the device to start processing before checking the ready flag:
  // right after sending a prompt the agent has not entered processing yet,
  // so a stale ready state from the previous round may be read, which would
  // skip polling and fetch the answer immediately
  delay(2000);

  // Poll until the answer is ready or the total timeout expires
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