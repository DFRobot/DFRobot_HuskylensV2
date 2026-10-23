/***************************************************
 HUSKYLENS V2 An Easy-to-use AI Machine Vision Sensor
 <https://www.dfrobot.com/product-1922.html>

 This example demonstrates the basic functionality of the HUSKYLENS V2 library
 via UART interface. It shows how to initialize the sensor with board-specific
 UART configurations (including SoftwareSerial for Arduino Uno/Nano), establish
 communication, and retrieve detection results from any active algorithm
 (ALGORITHM_ANY). The example prints out detected object properties including
 ID, center coordinates, width, height, name, and content in hexadecimal format
 for coordinate and dimension values.
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

#include <DFRobot_HuskylensV2.h>

// HUSKYLENS green line >> SDA; blue line >> SCL
HuskylensV2 huskylens;

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_NANO)
#include <SoftwareSerial.h>
SoftwareSerial Serial1(10, 11); // RX, TX
#define BAUDRATE 9600
#elif defined(ESP32)
#define BAUDRATE 115200
#define RX_PIN_P0 1
#define TX_PIN_P1 2
#elif defined(ARDUINO_BBC_MICROBIT_V2)
// The sandeepmistry nRF5 core provides no Serial1 and no SoftwareSerial, but
// the nRF52833 has a free UARTE1 peripheral: use it on edge pins 0 (RX) and
// 1 (TX). HUSKYLENS green line (TX) >> pin0; blue line (RX) >> pin1.
Uart Serial1((NRF_UART_Type *)NRF_UARTE1, UARTE1_IRQn, 0, 1); // RX, TX
extern "C" void UARTE1_IRQHandler(void) { Serial1.IrqHandler(); }
#define BAUDRATE 115200
#else
#define BAUDRATE 115200
#endif

void setup() {
  Serial.begin(115200);
#ifdef ARDUINO_ARCH_AVR
  Serial1.begin(BAUDRATE);
#elif defined(ESP32)
  Serial1.begin(BAUDRATE, SERIAL_8N1, RX_PIN_P0, TX_PIN_P1);
#elif defined(ARDUINO_BBC_MICROBIT_V2)
  Serial1.begin(BAUDRATE);
#else
#endif

  while (!huskylens.begin(Serial1)) {
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
  while (!huskylens.getResult(ALGORITHM_ANY)) {
    delay(100);
  }

  while (huskylens.available(ALGORITHM_ANY)) {
    Result *result =
        static_cast<Result *>(huskylens.popCachedResult(ALGORITHM_ANY));

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