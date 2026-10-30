/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 ***************************************************
 This example demonstrates how to record audio and play music with HUSKYLENS
 V2 via I2C interface. The code initializes the device and shows how to use
 startRecording() and playMusic() functions to record and play audio files.

 Created 2025-07-04
 By [Ouki Wang](ouki.wang@dfrobot.com)

 GNU Lesser General Public License.
 See <http://www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
 ****************************************************/

/***********Notice and Trouble shooting***************
 1.Connection and Diagram can be found here
 <https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336#target_23>
 2.This code is tested on Arduino Uno, Leonardo, Mega, Microbit,ESP8266,ESP32
 boards.
 ****************************************************/

#include "DFRobot_HuskylensV2.h"

// HUSKYLENS green line >> SDA; blue line >> SCL
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
    delay(100);
  }
  huskylens.switchAlgorithm((eAlgorithm_t)(128));
  delay(5000);
}

void loop() {
  bool ret = huskylens.startRecording(MEDIA_TYPE_AUDIO, 8, "test10s.mp3");
  Serial.print("startRecording 10s ret=");
  Serial.println(ret);
  delay(12 * 1000);

  ret = huskylens.playMusic("test10s.mp3", 100);
  Serial.print("playMusic test10s.mp3 ret=");
  Serial.println(ret);
  delay(12 * 1000);

  ret = huskylens.startRecording(MEDIA_TYPE_AUDIO, 0, "test5s.mp3");
  Serial.print("startRecording 5s ret=");
  Serial.println(ret);
  delay(5000);

  ret = huskylens.stopRecording(MEDIA_TYPE_AUDIO);
  Serial.print("stopRecording ret=");
  Serial.println(ret);
  delay(5000);

  ret = huskylens.playMusic("test5s.mp3", 100);
  Serial.print("playMusic test5s.mp3 ret=");
  Serial.println(ret);
  delay(5000);
}