# HuskyLens V2

* [中文版](./README_CN.md)


## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Algorithm](#algorithm)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

This library provides a way to drive the HuskyLensV2 under the Raspberry Pi via smbus2 and pyserial lib

## Installation
This library depends on the smbus2 and pyserial library, please ensure that smbus2 and pyserial have been installed via the following cmd before using this library. 

````bash title="library Install"
pip install smbus2
pip install pyserial
````
Then clone this repo into your Raspberry Pi. Enter the python code path and run the example code.

````bash title="Git Clone"
git clone https://github.com/DFRobot/DFRobot_HuskylensV2.git
cd DFRobot_HuskylensV2/python/smbus2/examples
python3 CenterObjectRecognition.py
````


## Methods
```python
"""
@fn knock
@brief Check whether the HuskyLens V2 exists on the I2C bus.
@return True:HuskyLens V2 exists, False:HuskyLens V2 does not exist.
"""
def knock(self):

'''
@fn switchAlgorithm
@brief Switch the built-in algorithm for HuskyLens V2
@params algo：Huskylens built-in algorithms. For algorithm details, please refer to the table below.
@return result
'''
def switchAlgorithm(self, algo):

'''
@fn getResult
@brief Get recognition result from HuskyLens V2
@params algo：Huskylens built-in algorithms. For algorithm details, please refer to the table below.
@return COMMAND_RETURN_ARGS
'''
def getResult(self, algo):

'''
@fn available
@brief If the result of this algorithm present in the current results.
@params algo：Huskylens built-in algorithms. For algorithm details, please refer to the table below.
@return True/False
'''
def available(self, algo):

'''
@fn getCachedCenterResult
@brief Get the result information closest to the camera center of HuskyLens V2
@params algo：HuskyLens built-in algorithms. For algorithm details, please refer to the table below.
@return self.result[algo]["blocks"]: The outputs of different algorithms vary slightly. See the table below for details.
'''
def getCachedCenterResult(self, algo):

'''
@fn getCachedResultByIndex
@brief Get the result information of Index of HuskyLens V2
@params algo：HuskyLens built-in algorithms. For algorithm details, please refer to the table below.
        index: The X-th face
@return self.result[algo]["blocks"]: The outputs of different algorithms vary slightly. See the table below for details.
'''
def getCachedResultByIndex(self, algo, index):


'''
@fn getCachedResultByID
@brief Get the result information of ID of HuskyLens V2
@params algo：HuskyLens built-in algorithms. For algorithm details, please refer to the table below.
        ID: ID of detect object
@return self.result[algo]["blocks"]: The outputs of different algorithms vary slightly. See the table below for details.
'''
def getCachedResultByID(self, algo, ID):

'''
@fn getCachedIndexResultByID
@brief Get the result information of ID and index of HuskyLens V2
@params algo：HuskyLens built-in algorithms. For algorithm details, please refer to the table below.
        ID: ID of detect object
        index: The X-th face
@return self.result[algo]["blocks"]: The outputs of different algorithms vary slightly. See the table below.
'''
def getCachedIndexResultByID(self, algo, ID, index):

```

## Algorithm
Huskylens incorporates multiple algorithms, each yielding distinct elements within the result.
Refer to the table below for the permitted parameters of the **algo** and **result** fields in the above API.

| algo | Algorithm Description  | result  | Result Element Description |
| :--: | :----: | :--: | :----: |
|  ALGORITHM_FACE_RECOGNITION   |  Face Recognition     |  ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>leye_x<br/>leye_y<br/>reye_x<br/>reye_y<br/>lmouth_x<br/>lmouth_y<br/>rmouth_x<br/>rmouth_y<br/>nose_x<br/>nose_y  | ID of the detected face<br/>Name of the detected face<br/>X-coordinate of the center of the detected face<br/>Y-coordinate of the center of the detected face<br/>Width of the detected face<br/>Height of the detected face<br/>X-coordinate of the left eye<br/>Y-coordinate of the left eye<br/>X-coordinate of the right eye<br/>Y-coordinate of the right eye<br/>X-coordinate of the left corner of the mouth<br/>Y-coordinate of the left corner of the mouth<br/>X-coordinate of the right corner of the mouth<br/>Y-coordinate of the right corner of the mouth<br/>X-coordinate of the nose<br/>Y-coordinate of the nose |
| ALGORITHM_OBJECT_RECOGNITION | Recognizing objects in daily life  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height  | ID of the detected object<br/>Name of the detected object<br/>X-coordinate of the center of the detected object<br/>Y-coordinate of the center of the detected object<br/>Width of the detected object<br/>Height of the detected object |
| ALGORITHM_OBJECT_TRACKING | Tracking a marked object  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height  | ID of the tracked object<br/>Name of the tracked object<br/>X-coordinate of the center of the tracked object<br/>Y-coordinate of the center of the tracked object<br/>Width of the tracked object<br/>Height of the tracked object |
| ALGORITHM_COLOR_RECOGNITION | Color Block Recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height   | ID of the detected color block<br/>Name of the detected color block<br/>X-coordinate of the center of the detected color block<br/>Y-coordinate of the center of the detected color block<br/>Width of the detected color block<br/>Height of the detected color block |
| ALGORITHM_SELF_LEARNING_CLASSIFICATION | Users learn to recognize a specific object on their own.  | ID<br/>name  | ID of the self-learned object<br/>Name of the self-learned object |
| ALGORITHM_SEGMENT | Instance Segmentation  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height  | ID of the detected segment<br/>Name of the detected segment<br/>X-coordinate of the center of the detected segment<br/>Y-coordinate of the center of the detected segment<br/>Width of the detected segment<br/>Height of the detected segment |
| ALGORITHM_HAND_RECOGNITION | Gesture/Hand recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br>wrist_x<br/>wrist_y<br/>thumb_cmc_x<br/>thumb_cmc_y<br/>thumb_mcp_x<br/>thumb_mcp_y<br/>thumb_ip_x<br/>thumb_ip_y<br/>thumb_tip_x<br/>thumb_tip_y<br/>index_finger_mcp_x<br/>index_finger_mcp_y<br/>index_finger_pip_x<br>index_finger_pip_y<br/>index_finger_dip_x<br/>index_finger_dip_y<br>index_finger_tip_x<br/>index_finger_tip_y<br/>middle_finger_mcp_x<br/>middle_finger_mcp_y<br>middle_finger_pip_x<br>middle_finger_pip_y<br/>middle_finger_dip_x<br/>middle_finger_dip_y<br>middle_finger_tip_x<br/>middle_finger_tip_y<br/>ring_finger_mcp_x<br/>ring_finger_mcp_y<br/>ring_finger_pip_x<br/>ring_finger_pip_y<br/>ring_finger_dip_x<br/>ring_finger_dip_y<br/>ring_finger_tip_x<br/>ring_finger_tip_y<br/>pinky_finger_mcp_x<br/>pinky_finger_mcp_y<br/>pinky_finger_pip_x<br/>pinky_finger_pip_y<br/>pinky_finger_dip_x<br/>pinky_finger_dip_y<br/>pinky_finger_tip_x<br/>pinky_finger_tip_y | ID of the detected gesture/hand<br/>Name of the detected gesture/hand<br/>X-coordinate of the center of the detected gesture/hand<br/>Y-coordinate of the center of the detected gesture/hand<br/>Width of the detected gesture/hand<br/>Height of the detected gesture/hand<br/>X-coordinate of the wrist<br/>Y-coordinate of the wrist<br/>X-coordinate of the thumb Carpometacarpal joint<br/>Y-coordinate of the thumb Carpometacarpal joint<br/>X-coordinate of the thumb Metacarpophalangeal joint<br/>Y-coordinate of the thumb Metacarpophalangeal joint<br/>X-coordinate of the thumb Interphalangeal joint<br/>Y-coordinate of the thumb Interphalangeal joint<br/>X-coordinate of the thumb tip<br/>Y-coordinate of the thumb tip<br/>X-coordinate of the index finger Metacarpophalangeal joint<br/>Y-coordinate of the index finger Metacarpophalangeal joint<br/>X-coordinate of the index finger Proximal Interphalangeal joint<br/>Y-coordinate of the index finger Proximal Interphalangeal joint<br/>X-coordinate of the index finger Distal Interphalangeal joint<br/>Y-coordinate of the index finger Distal Interphalangeal joint<br/>X-coordinate of the index finger tip<br/>Y-coordinate of the index finger tip<br/>X-coordinate of the middle finger Metacarpophalangeal joint<br/>Y-coordinate of the middle finger Metacarpophalangeal joint<br/>X-coordinate of the middle finger Proximal Interphalangeal joint<br/>Y-coordinate of the middle finger Proximal Interphalangeal joint<br/>X-coordinate of the middle finger Distal Interphalangeal joint<br/>Y-coordinate of the middle finger Distal Interphalangeal joint<br/>X-coordinate of the middle finger tip<br/>Y-coordinate of the middle finger tip<br/>X-coordinate of the ring finger Metacarpophalangeal joint<br/>Y-coordinate of the ring finger Metacarpophalangeal joint<br/>X-coordinate of the ring finger Proximal Interphalangeal joint<br/>Y-coordinate of the ring finger Proximal Interphalangeal joint<br/>X-coordinate of the ring finger Distal Interphalangeal joint<br/>Y-coordinate of the ring finger Distal Interphalangeal joint<br/>X-coordinate of the ring finger tip<br/>Y-coordinate of the ring finger tip<br/>X-coordinate of the pinky finger Metacarpophalangeal joint<br/>Y-coordinate of the pinky finger Metacarpophalangeal joint<br/>X-coordinate of the pinky finger Proximal Interphalangeal joint<br/>Y-coordinate of the pinky finger Proximal Interphalangeal joint<br/>X-coordinate of the pinky finger Distal Interphalangeal joint<br/>Y-coordinate of the pinky finger Distal Interphalangeal joint<br/>X-coordinate of the pinky finger tip<br/>Y-coordinate of the pinky finger tip|
| ALGORITHM_POSE_RECOGNITION | Human Pose Recognition  |  ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>nose_x<br/>nose_y<br/>leye_x<br/>leye_y<br/>reye_x<br/>reye_y<br/>lear_x<br/>lear_y<br/>rear_x<br/>rear_y<br/>lshoulder_x<br/>lshoulder_y<br/>rshoulder_x<br/>rshoulder_y<br/>lelbow_x<br/>lelbow_y<br/>relbow_x<br/>relbow_y<br/>lwrist_x<br/>lwrist_y<br/>rwrist_x<br/>rwrist_y<br/>lhip_x<br/>lhip_y<br/>rhip_x<br/>rhip_y<br/>lknee_x<br/>lknee_y<br/>rknee_x<br/>rknee_y<br/>lankle_x<br/>lankle_y<br/>rankle_x<br/>rankle_y<br/> | ID of the detected pose<br/>Name of the detected pose<br/>X-coordinate of the center of the detected pose<br/>Y-coordinate of the center of the detected pose<br/>Width of the detected pose<br/>Height of the detected pose<br/>X-coordinate of the nose<br/>Y-coordinate of the nose<br/>X-coordinate of the left eye<br/>Y-coordinate of the left eye<br/>X-coordinate of the right eye<br/>Y-coordinate of the right eye<br/>X-coordinate of the left ear<br/>Y-coordinate of the left ear<br/>X-coordinate of the right ear<br/>Y-coordinate of the right ear<br/>X-coordinate of the left shoulder<br/>Y-coordinate of the left shoulder<br/>X-coordinate of the right shoulder<br/>Y-coordinate of the right shoulder<br/>X-coordinate of the left elbow<br/>Y-coordinate of the left elbow<br/>X-coordinate of the right elbow<br/>Y-coordinate of the right elbow<br/>X-coordinate of the left wrist<br/>Y-coordinate of the left wrist<br/>X-coordinate of the right wrist<br/>Y-coordinate of the right wrist<br/>X-coordinate of the left hip<br/>Y-coordinate of the left hip<br/>X-coordinate of the right hip<br/>Y-coordinate of the right hip<br/>X-coordinate of the left knee<br/>Y-coordinate of the left knee<br/>X-coordinate of the right knee<br/>Y-coordinate of the right knee<br/>X-coordinate of the left ankle<br/>Y-coordinate of the left ankle<br/>X-coordinate of the right ankle<br/>Y-coordinate of the right ankle |
| ALGORITHM_LICENSE_RECOGNITION | License Plate Recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | ID of the detected license plate<br/>Name of the detected license plate<br/>X-coordinate of the center of the detected license plate<br/>Y-coordinate of the center of the detected license plate<br/>Width of the detected license plate<br/>Height of the detected license plate<br/>Content of the detected license plate (e.g., license number) |
| ALGORITHM_OCR_RECOGNITION | Optical Character Recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | ID of the detected character<br/>Name of the detected character<br/>X-coordinate of the center of the detected character<br/>Y-coordinate of the center of the detected character<br/>Width of the detected character<br/>Height of the detected character<br/>Content of the detected character|
| ALGORITHM_LINE_TRACKING | Line tracking  | xTarget<br/>yTarget<br/>angle<br/>length  | X compnent of the tracked line<br/>Y compnent of the tracked line<br/>Angle of the tracked line<br/>Length of the tracked line|
| ALGORITHM_EMOTION_RECOGNITION | Emotion Recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>  | ID of the detected emotion<br/>Name of the detected emotion<br/>X-coordinate of the center of the detected emotion<br/>Y-coordinate of the center of the detected emotion<br/>Width of the detected emotion<br/>Height of the detected emotion<br/> | 
| ALGORITHM_TAG_RECOGNITION | April Tag recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | ID of the detected april tag<br/>Name of the detected april tag<br/>X-coordinate of the center of the detected april tag<br/>Y-coordinate of the center of the detected april tag<br/>Width of the detected april tag<br/>Height of the detected april tag<br/>Content of the detected april tag |
| ALGORITHM_QRCODE_RECOGNITION | QR Code Recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | ID of the detected QR code<br/>Name of the detected QR code<br/>X-coordinate of the center of the detected QR code<br/>Y-coordinate of the center of the detected QR code<br/>Width of the detected QR code<br/>Height of the detected QR code<br/>Content of the detected QR code|
| ALGORITHM_BARCODE_RECOGNITION | Barcode Recognition  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | ID of the detected barcode<br/>Name of the detected barcode<br/>X-coordinate of the center of the detected barcode<br/>Y-coordinate of the center of the detected barcode<br/>Width of the detected barcode<br/>Height of the detected barcode<br/>Content of the detected barcode|

## Compatibility

|Dev Board         | Work Well | Work Wrong  | Untested | Remarks |
| ------------ | :--: | :----: | :----: | :--: |
| Raspberry Pi 4B |  √   |        |        |      |


* Python version 

| Python  | Work Well | Work Wrong | Untested | Remarks |
| ------- | :--: | :----: | :----: | ---- |
| Python2 |     |        |     √   |      |
| Python3 |  √   |        |        |      |
## History 

- 2026/04/22 - Version 1.0.0 released.

## Credits

Written by Yx(yixuan.niu@dfrobot.com), 2026.4.22 (Welcome to our [website](https://www.dfrobot.com/))