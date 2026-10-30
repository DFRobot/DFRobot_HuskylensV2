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
 2.This code is tested on Microbit,ESP8266,ESP32 boards.
 ****************************************************/

 #ifndef LARGE_MEMORY
#error "The selected board does not support this example."
#endif


#include <DFRobot_HuskylensV2.h>

// HUSKYLENS green line >> SDA; blue line >> SCL
HuskylensV2 huskylens;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    while (!huskylens.begin(Wire)) {
        Serial.println(F("Begin failed!"));
        Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS (System Settings>>Protocol Type>> I2C/UART)"));
        Serial.println(F("2.Please recheck the connection."));
        Serial.println(F("\tgreen line >> SDA/TX; blue line >> SCL/RX"));
        delay(100);
    }
}

void loop() {
    while (!huskylens.getResult(ALGORITHM_FACE_RECOGNITION)) {
        delay(100);
    }
    Serial.print("maxID=");
    Serial.println(huskylens.getCachedResultMaxID(ALGORITHM_FACE_RECOGNITION));
    Serial.print("result->ID=");
    Serial.println(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, ID));
    Serial.print("result->Center=(");
    Serial.print(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, xCenter));
    Serial.print(",");
    Serial.print(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, yCenter));
    Serial.println(")");
    Serial.print("result->width=");
    Serial.println(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, width));
    Serial.print("result->height=");
    Serial.println(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, height));
    Serial.print("result->name=");
    Serial.println(RET_ITEM_STR(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, name));
    Serial.print("result->content=");
    Serial.println(RET_ITEM_STR(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, content));

    Serial.print("result->getCachedResultNumByID()=");
    Serial.println(huskylens.getCachedResultNumByID(ALGORITHM_FACE_RECOGNITION, 2));

    Serial.print("result->getCachedIndexResultByID() xCenter=");
    Serial.println(RET_ITEM_NUM(huskylens.getCachedIndexResultByID(ALGORITHM_FACE_RECOGNITION, 2, 2), FaceResult, xCenter));

    Serial.print("FaceResult->leye_x=");
    Serial.println(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, leye_x));
    Serial.print("FaceResult->leye_y=");
    Serial.println(RET_ITEM_NUM(huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION), FaceResult, leye_y));

    delay(1000);
}