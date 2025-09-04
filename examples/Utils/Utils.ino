/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 ***************************************************
 This example shows the basic function of library for HUSKYLENS V2 via I2c.

 Created 2025-07-04
 By [Ouki Wang](ouki.wang@dfrobot.com)

 GNU Lesser General Public License.
 See <http://www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
 ****************************************************/

/***********Notice and Trouble shooting***************
 1.Connection and Diagram can be found here
 <https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336#target_23>
 2.This code is tested on Arduino Uno, Leonardo, Mega boards.
 ****************************************************/

#include "DFRobot_HuskylensV2.h"

// HUSKYLENS green line >> SDA; blue line >> SCL
HuskylensV2 huskylens;
#define RX_PIN_P0 1
#define TX_PIN_P1 2

void setup() {
    Serial.begin(115200);
    Serial1.begin(115200, SERIAL_8N1, RX_PIN_P0, TX_PIN_P1);
    while (!huskylens.begin(Serial1)) {
        Serial.println(F("Begin failed!"));
        Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS (System Settings>>Protocol Type>> I2C/UART)"));
        Serial.println(F("2.Please recheck the connection."));
        Serial.println(F("\tgreen line >> SDA/TX; blue line >> SCL/RX"));
        delay(100);
    }
}

void loop() {
    huskylens.clearText(ALGORITHM_OBJECT_RECOGNITION);
    delay(2000);
    huskylens.drawText(ALGORITHM_OBJECT_RECOGNITION, 0, 10, 10, "DFRobot Test");
    delay(2000);
    huskylens.clearRect(ALGORITHM_OBJECT_RECOGNITION);
    delay(2000);
    huskylens.drawRect(ALGORITHM_OBJECT_RECOGNITION, 0, 10, 10, 200, 30);
    delay(2000);
    huskylens.learn(ALGORITHM_OBJECT_RECOGNITION);
    delay(2000);
    huskylens.forgot(ALGORITHM_OBJECT_RECOGNITION);
    delay(2000);
    huskylens.saveKnowledges(ALGORITHM_OBJECT_RECOGNITION, 1);
    delay(2000);
    huskylens.loadKnowledges(ALGORITHM_OBJECT_RECOGNITION, 1);
    delay(2000);
    huskylens.playMusic("test.mp3", 100);
    delay(2000);
}