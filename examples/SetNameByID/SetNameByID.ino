/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 ***************************************************
 This example demonstrates how to set a name for an object by ID with HUSKYLENS
 V2 via I2C interface. The code initializes the device, switches to face
 recognition algorithm, and shows how to use setNameByID() function to set names
 for specific IDs.

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
  huskylens.switchAlgorithm(ALGORITHM_FACE_RECOGNITION);
  delay(5000);
}

void loop() {
  bool ret = huskylens.setNameByID(ALGORITHM_FACE_RECOGNITION, 1, "tangyan");
  Serial.print("setNameByID ret=");
  Serial.println(ret);
  delay(5000);
  ret = huskylens.setNameByID(ALGORITHM_FACE_RECOGNITION, 1, "meinv");
  Serial.print("setNameByID ret=");
  Serial.println(ret);
  delay(5000);
}