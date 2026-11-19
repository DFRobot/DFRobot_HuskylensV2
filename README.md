# HuskyLens V2

* [中文版](README_CN.md)


## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Algorithm](#algorithm)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

This library provides an interface for driving the HuskyLens V2 on Arduino-compatible boards. It supports both UART and I2C communication protocols and provides various computer vision algorithms for object recognition, face detection, line tracking, and more.

> [!WARNING]
> **Firmware requirement: This Arduino library only supports HuskyLens V2 firmware version 1.4.2 or above.** Please upgrade your device firmware to v1.4.2+ before use, otherwise the library may fail to communicate or return incorrect results.

## Installation

1. Download the library from GitHub
2. Extract the zip file
3. Move the extracted folder to your Arduino libraries directory
4. Restart Arduino IDE
5. Include the library in your sketch: `#include <DFRobot_HuskylensV2.h>`

Alternatively, you can install the library through the Arduino Library Manager by searching for "DFRobot_HuskylensV2".

## Methods

### Initialization Methods

```cpp
/**
 * @fn begin
 * @brief Initialize the HuskyLens V2 using UART communication
 * @param streamInput The serial port to use for communication
 * @return true if initialization succeeds, false otherwise
 */
bool begin(Stream &streamInput);

/**
 * @fn begin
 * @brief Initialize the HuskyLens V2 using I2C communication
 * @param streamInput The I2C interface to use for communication
 * @return true if initialization succeeds, false otherwise
 */
bool begin(TwoWire &streamInput);

/**
 * @fn knock
 * @brief Check if HuskyLens V2 is connected
 * @return true if HuskyLens V2 is connected, false otherwise
 */
bool knock(void);
```

### Algorithm Control Methods

```cpp
/**
 * @fn switchAlgorithm
 * @brief Switch the built-in algorithm of HuskyLens V2
 * @param algo The algorithm to switch to
 * @return true if the algorithm is switched successfully, false otherwise
 */
bool switchAlgorithm(eAlgorithm_t algo);

/**
 * @fn getResult
 * @brief Get recognition results from HuskyLens V2
 * @param algo The algorithm to get results for
 * @return COMMAND_RETURN_ARGS retValue==0 if successful, other values indicate errors
 */
int8_t getResult(eAlgorithm_t algo);

/**
 * @fn available
 * @brief Check if results are available for a specific algorithm
 * @param algo The algorithm to check
 * @return true if results are available, false otherwise
 */
bool available(eAlgorithm_t algo);
```

### Result Retrieval Methods

```cpp
/**
 * @fn popCachedResult
 * @brief Pop a cached result from the result queue
 * @param algo The algorithm to get results for
 * @return A pointer to the result, or NULL if no result is available
 */
Result *popCachedResult(eAlgorithm_t algo);

/**
 * @fn getCachedCenterResult
 * @brief Get the result closest to the center of the camera
 * @param algo The algorithm to get results for
 * @return A pointer to the center result, or NULL if no result is available
 */
Result *getCachedCenterResult(eAlgorithm_t algo);

/**
 * @fn getCachedResultByIndex
 * @brief Get a cached result by index
 * @param algo The algorithm to get results for
 * @param index The index of the result
 * @return A pointer to the result, or NULL if no result is available at the specified index
 */
Result *getCachedResultByIndex(eAlgorithm_t algo, int16_t index);

/**
 * @fn getCachedResultByID
 * @brief Get a cached result by ID
 * @param algo The algorithm to get results for
 * @param ID The ID of the object to retrieve
 * @return A pointer to the result, or NULL if no result is available with the specified ID
 */
Result *getCachedResultByID(eAlgorithm_t algo, int16_t ID);

/**
 * @fn getCachedResultNum
 * @brief Get the number of cached results
 * @param algo The algorithm to get results for
 * @return The number of cached results
 */
int16_t getCachedResultNum(eAlgorithm_t algo);

/**
 * @fn getCachedResultLearnedNum
 * @brief Get the number of learned results
 * @param algo The algorithm to get results for
 * @return The number of learned results
 */
int16_t getCachedResultLearnedNum(eAlgorithm_t algo);
```

### Result Structure

All result retrieval methods above return a pointer to a `Result` object. The `Result` class carries the common fields reported by HuskyLens V2 in the `RETURN_BLOCKS` protocol frame:

| Field | Type | Description |
| :--: | :----: | :--: |
| ID | uint8_t | The learned ID of the object. 0 means unlearned |
| xCenter | int16_t | X coordinate of the block center |
| yCenter | int16_t | Y coordinate of the block center |
| width | int16_t | Width of the block |
| height | int16_t | Height of the block |
| conf | float | Confidence of the recognition result (only valid for block-type results; arrow results from line tracking do not carry this field) |
| name | String | Name of the recognized object |
| content | String | Content of the recognized object (e.g. QR code text), empty if the algorithm reports none |

### Learning and Knowledge Management Methods

```cpp
/**
 * @fn learn
 * @brief Learn an object using the current algorithm
 * @param algo The algorithm to use for learning
 * @return true if learning is successful, false otherwise
 */
bool learn(eAlgorithm_t algo);

/**
 * @fn learnBlock
 * @brief Learn a specific block region
 * @param algo The algorithm to use for learning
 * @param x The x-coordinate of the top-left corner of the block
 * @param y The y-coordinate of the top-left corner of the block
 * @param width The width of the block
 * @param height The height of the block
 * @return true if learning is successful, false otherwise
 */
bool learnBlock(eAlgorithm_t algo, int16_t x, int16_t y, int16_t width, int16_t height);

/**
 * @fn forget
 * @brief Forget all learned objects for a specific algorithm
 * @param algo The algorithm to forget learned objects for
 * @return true if forgetting is successful, false otherwise
 */
bool forget(eAlgorithm_t algo);

/**
 * @fn saveKnowledges
 * @brief Save learned knowledge to a specific knowledge ID
 * @param algo The algorithm to save knowledge for
 * @param knowledgeID The ID to save the knowledge to
 * @return true if saving is successful, false otherwise
 */
bool saveKnowledges(eAlgorithm_t algo, uint8_t knowledgeID);

/**
 * @fn loadKnowledges
 * @brief Load learned knowledge from a specific knowledge ID
 * @param algo The algorithm to load knowledge for
 * @param knowledgeID The ID to load the knowledge from
 * @return true if loading is successful, false otherwise
 */
bool loadKnowledges(eAlgorithm_t algo, uint8_t knowledgeID);
```

### Display Control Methods

```cpp
/**
 * @fn drawRect
 * @brief Draw a rectangle on the HuskyLens display
 * @param algo The algorithm context
 * @param color The color of the rectangle
 * @param lineWidth The line width of the rectangle
 * @param x The x-coordinate of the top-left corner
 * @param y The y-coordinate of the top-left corner
 * @param width The width of the rectangle
 * @param height The height of the rectangle
 * @return true if drawing is successful, false otherwise
 */
bool drawRect(eAlgorithm_t algo, uint32_t color, uint8_t lineWidth, int16_t x, int16_t y, int16_t width, int16_t height);

/**
 * @fn drawUniqueRect
 * @brief Draw a unique rectangle on the HuskyLens display, previous rectangles will be erased automatically
 * @param algo The algorithm context
 * @param color The color of the rectangle
 * @param lineWidth The line width of the rectangle
 * @param x The x-coordinate of the top-left corner
 * @param y The y-coordinate of the top-left corner
 * @param width The width of the rectangle
 * @param height The height of the rectangle
 * @return true if drawing is successful, false otherwise
 */
bool drawUniqueRect(eAlgorithm_t algo, uint32_t color, uint8_t lineWidth, int16_t x, int16_t y, int16_t width, int16_t height);

/**
 * @fn drawText
 * @brief Draw text on the HuskyLens display
 * @param algo The algorithm context
 * @param color The color of the text
 * @param fontSize The font size of the text
 * @param x The x-coordinate of the text position
 * @param y The y-coordinate of the text position
 * @param text The text to draw
 * @return true if drawing is successful, false otherwise
 */
bool drawText(eAlgorithm_t algo, uint32_t color, uint8_t fontSize, int16_t x, int16_t y, String text);

/**
 * @fn clearRect
 * @brief Clear all rectangles on the HuskyLens display
 * @param algo The algorithm context
 * @return true if clearing is successful, false otherwise
 */
bool clearRect(eAlgorithm_t algo);

/**
 * @fn clearText
 * @brief Clear all text on the HuskyLens display
 * @param algo The algorithm context
 * @return true if clearing is successful, false otherwise
 */
bool clearText(eAlgorithm_t algo);
```

### Multi-algorithm Support (for large memory boards)

```cpp
/**
 * @fn setMultiAlgorithm
 * @brief Set multiple algorithms to run simultaneously (only available on large memory boards)
 * @param algo0 The first algorithm
 * @param algo1 The second algorithm
 * @param algo2 The third algorithm (default: ALGORITHM_ANY)
 * @return true if setting is successful, false otherwise
 */
bool setMultiAlgorithm(eAlgorithm_t algo0, eAlgorithm_t algo1, eAlgorithm_t algo2 = ALGORITHM_ANY);

/**
 * @fn setMultiAlgorithmRatio
 * @brief Set the running ratio of multiple algorithms (only available on large memory boards)
 * @param ratio0 The time occupation ratio of the first algorithm
 * @param ratio1 The time occupation ratio of the second algorithm
 * @param ratio2 The time occupation ratio of the third algorithm (default: 0)
 * @return true if setting is successful, false otherwise
 */
bool setMultiAlgorithmRatio(uint8_t ratio0, uint8_t ratio1, uint8_t ratio2 = 0);
```

## Algorithm

HuskyLens V2 incorporates multiple algorithms, each yielding distinct elements within the result.
Refer to the table below for the supported algorithms and their result elements.

| Algorithm Enum | Algorithm Description | Result Elements |
| :--: | :----: | :--: |
| ALGORITHM_ANY | Any algorithm | Varies based on active algorithm |
| ALGORITHM_FACE_RECOGNITION | Face Recognition | ID, name, xCenter, yCenter, width, height, eye coordinates, mouth coordinates, nose coordinates |
| ALGORITHM_OBJECT_TRACKING | Object Tracking | ID, name, xCenter, yCenter, width, height |
| ALGORITHM_OBJECT_RECOGNITION | Object Recognition | ID, name, xCenter, yCenter, width, height |
| ALGORITHM_LINE_TRACKING | Line Tracking | xTarget, yTarget, angle, length |
| ALGORITHM_COLOR_RECOGNITION | Color Recognition | ID, name, xCenter, yCenter, width, height |
| ALGORITHM_TAG_RECOGNITION | Tag Recognition | ID, name, xCenter, yCenter, width, height, content |
| ALGORITHM_SELF_LEARNING_CLASSIFICATION | Self-learning Classification | ID, name |
| ALGORITHM_OCR_RECOGNITION | Optical Character Recognition | ID, name, xCenter, yCenter, width, height, content |
| ALGORITHM_LICENSE_RECOGNITION | License Plate Recognition | ID, name, xCenter, yCenter, width, height, content |
| ALGORITHM_QRCODE_RECOGNITION | QR Code Recognition | ID, name, xCenter, yCenter, width, height, content |
| ALGORITHM_BARCODE_RECOGNITION | Barcode Recognition | ID, name, xCenter, yCenter, width, height, content |
| ALGORITHM_EMOTION_RECOGNITION | Emotion Recognition | ID, name, xCenter, yCenter, width, height |
| ALGORITHM_POSE_RECOGNITION | Pose Recognition | ID, name, xCenter, yCenter, width, height, coordinates of body joints |
| ALGORITHM_HAND_RECOGNITION | Hand Recognition | ID, name, xCenter, yCenter, width, height, coordinates of hand joints |
| ALGORITHM_SEGMENT | Instance Segmentation | ID, name, xCenter, yCenter, width, height |

## Compatibility

| Development Board | Work Well | Work Wrong | Untested | Remarks |
| ------------ | :--: | :----: | :----: | :--: |
| Arduino UNO | √ | | | |
| Arduino Mega | √ | | | |
| Arduino Leonardo | √ | | | |
| ESP32 | √ | | | Large memory support |
| ESP8266 | √ | | | Large memory support |
| Raspberry Pi Pico | √ | | | |
| micro:bit | √ | | | Large memory support |

## History

- 2025/11/08 - Version 1.0.0 released.

## Credits

Written by Ouki.Wang(ouki.wang@dfrobot.com), 2025.11.08 (Welcome to our [website](https://www.dfrobot.com/))
