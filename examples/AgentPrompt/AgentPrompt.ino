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
#ifndef LARGE_MEMORY
#error "The selected board does not support this example."
#endif

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

// Send one prompt and print the whole answer, return false on any failure
static bool runAgentRound(const String &prompt) {
  if (!huskylens.sendAgentPrompt(prompt)) {
    Serial.println("[AgentPrompt] Send prompt failed");
    return false;
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
    if (status == AGENT_DISABLED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
      return false;
    } else if (status != AGENT_QUERY_FAILED) {
      Serial.print(F("agent status: "));
      Serial.println(agentStatusStr(status));
    } else {
      Serial.println(F("agent status: <query failed>"));
      return false;
    }
    if (millis() - start > AGENT_POLL_TIMEOUT_MS) {
      Serial.println("[AgentPrompt] Poll timeout, give up");
      return false;
    }
    delay(AGENT_POLL_INTERVAL_MS);
  }

  String response = huskylens.getAgentResponse();
  if (response.length() > 0) {
    Serial.println("[AgentPrompt] Response : " + response);
    return true;
  }
  Serial.println("[AgentPrompt] Response failed");
  return false;
}

void loop() {
  Serial.println();
  Serial.println("[AgentPrompt] Start ...");

  runAgentRound("tell me a long joke");
  delay(5000);

  runAgentRound("Turn on the flashlight");
  delay(5000);

  runAgentRound("Turn off the flashlight");
  delay(5000);
}
