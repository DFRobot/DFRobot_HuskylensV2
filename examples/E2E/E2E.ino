/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 This example demonstrates the E2E recording and annotation workflow of
 HUSKYLENS V2 via I2C interface. It initializes the sensor, starts an E2E
 recording task, sends timestamped sample sensor annotation data, and then
 stops the recording task.
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
 2.This code is tested on Arduino Uno, Leonardo, Mega, Microbit,ESP8266,ESP32
 boards.
 ****************************************************/

#include "DFRobot_HuskylensV2.h"

int sensor_data1,sensor_data2,sensor_data3;
String annotation;
HuskylensV2 huskylens;

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
  // 初始化随机种子
  randomSeed(analogRead(A0));
}

void loop() {
  Serial.println();
  Serial.println("[E2E] Start recording...");

  if (!huskylens.e2eStartRecording()) {
    Serial.println("[E2E] Start recording failed");
    delay(1000);
    return;
  }

  Serial.println("[E2E] Recording started");

  for (uint8_t i = 0; i < 10; ++i) {
    unsigned long timestamp = millis();
    sensor_data1 = random(1000);  // 0~999
    sensor_data2 = random(1000);
    sensor_data3 = random(1000);
    annotation = String(timestamp) + "," +
                 String(sensor_data1) + "," +
                 String(sensor_data2) + "," +
                 String(sensor_data3);

    bool ret = huskylens.e2eSendAnnotation(annotation);

    Serial.print("[E2E] Annotation ");
    Serial.print(i + 1);
    Serial.print("/10 ");
    Serial.print(ret ? "sent" : "failed");
    Serial.print(": time=");
    Serial.print(timestamp);
    Serial.print(", data=[");
    Serial.print(sensor_data1);
    Serial.print(", ");
    Serial.print(sensor_data2);
    Serial.print(", ");
    Serial.print(sensor_data3);
    Serial.print("], payload=\"");
    Serial.print(annotation);
    Serial.println("\"");

    delay(500);
  }

  bool ret = huskylens.e2eStopRecording();
  Serial.print("[E2E] Stop recording ");
  Serial.println(ret ? "success" : "failed");
  delay(2000);
}
