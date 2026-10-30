/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 This example shows the multi-algorithm function of library for HUSKYLENS V2 via
 I2C. It demonstrates how to run multiple algorithms simultaneously (face
 recognition, object tracking, and hand recognition) and adjust their
 priorities. The example implements an interactive flow where users can draw a
 rectangle using hand gestures, learn objects within that rectangle, and then
 track those objects.
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
 2.This code is tested on Microbit,ESP8266,ESP32
 boards.
 ****************************************************/
#ifndef LARGE_MEMORY
#error "The selected board does not support this example."
#endif


#include "DFRobot_HuskylensV2.h"

// HUSKYLENS green line >> SDA; blue line >> SCL
HuskylensV2 huskylens;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  while (!huskylens.begin(Wire)) {
    Serial.println(F("Begin failed!"));
    Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS "
                     "(General Settings>>Protocol Type>>I2C)"));
    Serial.println(F("2.Please recheck the connection."));
    delay(100);
  }
  huskylens.setMultiAlgorithm(ALGORITHM_OBJECT_TRACKING,
                              ALGORITHM_HAND_RECOGNITION);
  delay(5000);
  huskylens.setMultiAlgorithmRatio(0, 1);
  delay(1000);
}

int x1_, y1_, x2_, y2_;
bool start = false;
bool learned = false;

void loop() {
  while (!huskylens.getResult(ALGORITHM_HAND_RECOGNITION)) {
    delay(100);
  }

  HandResult *handResult = static_cast<HandResult *>(
      huskylens.popCachedResult(ALGORITHM_HAND_RECOGNITION));
  if (handResult != NULL) {
    float tipDistance =
        sqrt(SQUARE(handResult->index_finger_tip_x - handResult->thumb_tip_x) +
             SQUARE(handResult->index_finger_tip_y - handResult->thumb_tip_y));

    float palmLength =
        sqrt(SQUARE(handResult->index_finger_pip_x - handResult->wrist_x) +
             SQUARE(handResult->index_finger_pip_y - handResult->wrist_y));

    float ratio = tipDistance / palmLength;

    printf("tip_distance(%f)/palm_length(%f) = ratio(%f)\n", tipDistance,
           palmLength, ratio);

    if (!start && ratio < 0.15) {
      huskylens.clearText();
      huskylens.drawText(COLOR_RED, 20, 10, 10, "Draw Rect");
      x1_ = ((int)handResult->index_finger_tip_x + handResult->thumb_tip_x) / 2;
      y1_ = ((int)handResult->index_finger_tip_y + handResult->thumb_tip_y) / 2;
      start = true;
    } else if (start && ratio <= 0.6) {
      x2_ = ((int)handResult->index_finger_tip_x + handResult->thumb_tip_x) / 2;
      y2_ = ((int)handResult->index_finger_tip_y + handResult->thumb_tip_y) / 2;
      huskylens.drawUniqueRect(COLOR_RED, 2, x1_, y1_, x2_ - x1_, y2_ - y1_);
    } else if (start && ratio > 1) {
      start = false;
      if (abs((x2_ - x1_) * (y2_ - y1_)) > 2500) {
        huskylens.clearText();
        huskylens.drawText(COLOR_YELLOW, 20, 10, 10, "Learning ...");
        huskylens.drawUniqueRect(COLOR_YELLOW, 2, x1_, y1_, x2_ - x1_,
                                 y2_ - y1_);

        huskylens.learnBlock(ALGORITHM_OBJECT_TRACKING, x1_, y1_, x2_ - x1_,
                             y2_ - y1_);

        huskylens.clearRect();
        huskylens.clearText();
        huskylens.drawText(COLOR_GREEN, 20, 10, 10, "Learned");

        delay(300);
        huskylens.setMultiAlgorithmRatio(1, 0);
        huskylens.clearText();
      }
    }
  } else {
    return;
  }

  Result *trackerResult = huskylens.popCachedResult(ALGORITHM_OBJECT_TRACKING);
  if (trackerResult != NULL) {
    // process tracking event
  }
}
