/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 This example demonstrates the auto drive (city roads) functionality of
 HUSKYLENS V2 via I2C interface. It shows how to initialize the sensor, run
 the end-to-end driving model, and print the steering angle and throttle
 values for controlling a car.
 ***************************************************
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

// HUSKYLENS green line >> SDA/TX; blue line >> SCL/RX
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
  huskylens.switchAlgorithm(ALGORITHM_AUTO_DRIVE_CITY_ROADS);
  delay(5000);
}

void loop() {
  while (!huskylens.getResult(ALGORITHM_AUTO_DRIVE_CITY_ROADS)) {
    delay(100);
  }

  while (huskylens.available(ALGORITHM_AUTO_DRIVE_CITY_ROADS)) {
    Result *result = huskylens.popCachedResult(ALGORITHM_AUTO_DRIVE_CITY_ROADS);

    Serial.println();

    Serial.print("result->steering=");
    Serial.println(result->steering);
    Serial.print("result->throttle=");
    Serial.println(result->throttle);
  }
  delay(1000);
}
