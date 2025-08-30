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

#include <DFRobot_HuskylensV2.h>

// HUSKYLENS green line >> SDA; blue line >> SCL
HuskylensV2 huskylens;

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
#include <SoftwareSerial.h>
SoftwareSerial Serial1(10, 11); // RX, TX
#define BAUDRATE 9600
#elif defined(ESP32)
#define BAUDRATE  115200
#define RX_PIN_P0 1
#define TX_PIN_P1 2
#else
#define BAUDRATE 115200
#endif

void setup() {
    Serial.begin(115200);
#ifdef ARDUINO_ARCH_AVR
    Serial1.begin(BAUDRATE);
#elif defined(ESP32)
    Serial1.begin(BAUDRATE, SERIAL_8N1, RX_PIN_P0, TX_PIN_P1);
#else
#endif

    while (!huskylens.begin(Serial1)) {
        Serial.println(F("Begin failed!"));
        Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS (General Settings>>Protocol Type>>I2C)"));
        Serial.println(F("2.Please recheck the connection."));
        delay(100);
    }
}

void loop() {
    while (!huskylens.getResult(ALGORITHM_ANY)) {
        delay(100);
    }

    while (huskylens.available(ALGORITHM_ANY)) {
        Result *result = static_cast<Result *>(huskylens.getCachedResult(ALGORITHM_ANY));

        Serial.print("result->ID=");
        Serial.println(result->ID, HEX);

        Serial.print("result->Center=(");
        Serial.print(result->xCenter, HEX);
        Serial.print(",");
        Serial.print(result->yCenter, HEX);
        Serial.println(")");

        Serial.println(result->width, HEX);
        Serial.print("result->height=");
        Serial.println(result->height, HEX);
        Serial.print("result->name=");
        Serial.println(result->name);
        Serial.print("result->content=");
        Serial.println(result->content);
    }
    delay(1000);
}