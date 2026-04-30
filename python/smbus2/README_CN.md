# 二哈识图V2

* [English Version](./README.md)


## 目录

* [简介](#简介)
* [安装](#安装)
* [方法](#方法)
* [算法](#算法)
* [兼容性](#兼容性)
* [更改历史](#更改历史)
* [作者](#作者)

## 简介

这个库提供了一种在树莓派上通过smbus2和pyserial库驱动二哈识图V2

## 安装
此库依赖于 **smbus2** 库和 **pyserial** 库，请在使用本库之前，先通过以下命令安装依赖库。


````bash title="Pinpong Install"
pip install smbus2
pip install pyserial
````
然后将此仓库克隆到你的 **树莓派（Raspberry Pi）** 中，进入 **Python 代码路径**，并运行示例代码。
````bash title="Git Clone"
git clone https://github.com/DFRobot/DFRobot_HuskylensV2.git
cd DFRobot_HuskylensV2/python/smbus2/examples
python3 CenterObjectRecognition.py
````


## 方法
```python
"""
@fn knock
@brief 检查 I2C 总线上 是否存在 二哈识图 V2
@return True:二哈识图 V2存在, False:二哈识图 V2不存在
"""
def knock(self):

'''
@fn switchAlgorithm
@brief 切换二哈识图V2的内置算法。
@params algo：二哈识图V2内置算法。有关算法的详细信息，请参阅算法章节。
@return result
'''
def switchAlgorithm(self, algo):

'''
@fn getResult
@brief 获取二哈识图V2的识别结果。
@params algo：二哈识图内置算法。有关算法的详细信息，请参阅算法章节。
@return COMMAND_RETURN_ARGS
'''
def getResult(self, algo):

'''
@fn available
@brief 如果此算法的结果存在于当前结果中。
@params algo：二哈识图内置算法。有关算法的详细信息，请参阅算法章节。
@return True/False
'''
def available(self, algo):

'''
@fn getCachedCenterResult
@brief 获取二哈识图V2中最接近摄像头中心的结果信息。
@params algo：二哈识图内置算法。有关算法的详细信息，请参阅算法章节。
@return result[algo]["blocks"]: 不同算法的输出会略有差异。详情请参阅算法章节。
'''
def getCachedCenterResult(self, algo):

'''
@fn getCachedResultByIndex
@brief 获取二哈识图V2中指定索引的结果信息。
@params algo：二哈识图内置算法。有关算法详情，请参见算法章节。
        index: 结果索引号。比如：第n张人脸
@return result[algo]["blocks"]: 不同算法的输出略有差异。详情请参见算法章节。
'''
def getCachedResultByIndex(self, algo, index):


'''
@fn getCachedResultByID
@brief 获取二哈识图V2中指定ID的结果信息。
@params algo：二哈识图内置算法。有关算法详情，请参见算法章节。
        ID: 指定ID
@return result[algo]["blocks"]: 不同算法的输出略有差异。详情请参见算法章节。
'''
def getCachedResultByID(self, algo, ID):

'''
@fn getCachedIndexResultByID
@brief 获取二哈识图V2中指定ID和索引的结果信息。
@params algo：二哈识图内置算法。有关算法详情，请参见算法章节。
        ID: 指定ID
        index: 结果索引号。比如：第n张人脸
@return self.result[algo]["blocks"]: 不同算法的输出略有差异。详情请参见算法章节。
'''
def getCachedIndexResultByID(self, algo, ID, index):

```

## 算法
二哈识图包含多种算法，每种算法在结果中产生不同的元素。
有关上述 API 中 **algo** 和 **result** 形参允许的实参，请参见下表。

| algo | 算法说明  | result  | 结果元素说明 |
| :--: | :----: | :--: | :----: |
|  ALGORITHM_FACE_RECOGNITION   |  人脸识别     |  ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>leye_x<br/>leye_y<br/>reye_x<br/>reye_y<br/>lmouth_x<br/>lmouth_y<br/>rmouth_x<br/>rmouth_y<br/>nose_x<br/>nose_y  | 识别到的人脸ID<br/>识别到的人脸名称<br/>识别到的人脸中心X坐标<br/>识别到的人脸中心Y坐标<br/>识别到的人脸宽度<br/>识别到的人脸高度<br/>识别到的人脸左眼X坐标<br/>识别到的人脸左眼Y坐标<br/>识别到的人脸右眼X坐标<br/>识别到的人脸右眼Y坐标<br/>识别到的左嘴角X坐标<br/>识别到的左嘴角Y坐标<br/>识别到的右嘴角X坐标<br/>识别到的右嘴角Y坐标<br/>识别到的鼻子X坐标<br/>识别到的鼻子Y坐标 |
| ALGORITHM_OBJECT_RECOGNITION | 物体识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height  | 识别到的物体ID<br/>识别到的物体名称<br/>识别到的物体中心X坐标<br/>识别到的物体中心Y坐标<br/>识别到的物体宽度<br/>识别到的物体高度 |
| ALGORITHM_OBJECT_TRACKING | 物体追踪  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height  | 追踪到的物体ID<br/>追踪到的物体名称<br/>追踪到的物体中心X坐标<br/>追踪到的物体中心Y坐标<br/>追踪到的物体宽度<br/>追踪到的物体高度 |
| ALGORITHM_COLOR_RECOGNITION | 颜色识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height   | 识别到的颜色ID<br/>识别到的颜色名称<br/>识别到的颜色中心X坐标<br/>识别到的颜色中心Y坐标<br/>识别到的颜色宽度<br/>识别到的颜色高度 |
| ALGORITHM_SELF_LEARNING_CLASSIFICATION | 自学习分类  | ID<br/>name  | 检测到的自学习分类物体ID<br/>检测到的自学习分类物体名称 |
| ALGORITHM_SEGMENT | 实例分割  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height  | 检测到的实例ID<br/>检测到的实例名称<br/>检测到的实例中心X坐标<br/>检测到的实例中心Y坐标<br/>检测到的实例宽度<br/>检测到的实例高度 |
| ALGORITHM_HAND_RECOGNITION | 手势识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br>wrist_x<br/>wrist_y<br/>thumb_cmc_x<br/>thumb_cmc_y<br/>thumb_mcp_x<br/>thumb_mcp_y<br/>thumb_ip_x<br/>thumb_ip_y<br/>thumb_tip_x<br/>thumb_tip_y<br/>index_finger_mcp_x<br/>index_finger_mcp_y<br/>index_finger_pip_x<br>index_finger_pip_y<br/>index_finger_dip_x<br/>index_finger_dip_y<br>index_finger_tip_x<br/>index_finger_tip_y<br/>middle_finger_mcp_x<br/>middle_finger_mcp_y<br>middle_finger_pip_x<br/>middle_finger_pip_y<br/>middle_finger_dip_x<br/>middle_finger_dip_y<br>middle_finger_tip_x<br/>middle_finger_tip_y<br/>ring_finger_mcp_x<br/>ring_finger_mcp_y<br/>ring_finger_pip_x<br/>ring_finger_pip_y<br/>ring_finger_dip_x<br/>ring_finger_dip_y<br/>ring_finger_tip_x<br/>ring_finger_tip_y<br/>pinky_finger_mcp_x<br/>pinky_finger_mcp_y<br/>pinky_finger_pip_x<br/>pinky_finger_pip_y<br/>pinky_finger_dip_x<br/>pinky_finger_dip_y<br/>pinky_finger_tip_x<br/>pinky_finger_tip_y | 识别到的手势ID<br/>识别到的手势名称<br/>识别到的手势中心X坐标<br/>识别到的手势中心Y坐标<br/>识别到的手势宽度<br/>识别到的手势高度<br/>手腕X坐标<br/>手腕Y坐标<br/>拇指基部X坐标<br/>拇指基部Y坐标<br/>拇指掌侧关节X坐标<br/>拇指掌侧关节Y坐标<br/>拇指近端关节X坐标<br/>拇指近端关节Y坐标<br/>拇指指尖X坐标<br/>拇指指尖Y坐标<br/>食指根部X坐标<br/>食指根部Y坐标<br/>食指近节关节X坐标<br/>食指近节关节Y坐标<br/>食指中节关节X坐标<br/>食指中节关节Y坐标<br/>食指指尖X坐标<br/>食指指尖Y坐标<br/>中指根部X坐标<br/>中指根部Y坐标<br/>中指近节关节X坐标<br/>中指近节关节Y坐标<br/>中指中节关节X坐标<br/>中指中节关节Y坐标<br/>中指指尖X坐标<br/>中指指尖Y坐标<br/>无名指根部X坐标<br/>无名指根部Y坐标<br/>无名指近节关节X坐标<br/>无名指近节关节Y坐标<br/>无名指中节关节X坐标<br/>无名指中节关节Y坐标<br/>无名指指尖X坐标<br/>无名指指尖Y坐标<br/>小指根部X坐标<br/>小指根部Y坐标<br/>小指近节关节X坐标<br/>小指近节关节Y坐标<br/>小指中节关节X坐标<br/>小指中节关节Y坐标<br/>小指指尖X坐标<br/>小指指尖Y坐标 |
| ALGORITHM_POSE_RECOGNITION | 姿态识别  |  ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>nose_x<br/>nose_y<br/>leye_x<br/>leye_y<br/>reye_x<br/>reye_y<br/>lear_x<br/>lear_y<br/>rear_x<br/>rear_y<br/>lshoulder_x<br/>lshoulder_y<br/>rshoulder_x<br/>rshoulder_y<br/>lelbow_x<br/>lelbow_y<br/>relbow_x<br/>relbow_y<br/>lwrist_x<br/>lwrist_y<br/>rwrist_x<br/>rwrist_y<br/>lhip_x<br/>lhip_y<br/>rhip_x<br/>rhip_y<br/>lknee_x<br/>lknee_y<br/>rknee_x<br/>rknee_y<br/>lankle_x<br/>lankle_y<br/>rankle_x<br/>rankle_y<br/> | 识别到的姿态ID<br/>识别到的姿态名称<br/>识别到的姿态中心X坐标<br/>识别到的姿态中心Y坐标<br/>识别到的姿态宽度<br/>识别到的姿态高度<br/>鼻子X坐标<br/>鼻子Y坐标<br/>左眼X坐标<br/>左眼Y坐标<br/>右眼X坐标<br/>右眼Y坐标<br/>左耳X坐标<br/>左耳Y坐标<br/>右耳X坐标<br/>右耳Y坐标<br/>左肩X坐标<br/>左肩Y坐标<br/>右肩X坐标<br/>右肩Y坐标<br/>左肘X坐标<br/>左肘Y坐标<br/>右肘X坐标<br/>右肘Y坐标<br/>左腕X坐标<br/>左腕Y坐标<br/>右腕X坐标<br/>右腕Y坐标<br/>左髋X坐标<br/>左髋Y坐标<br/>右髋X坐标<br/>右髋Y坐标<br/>左膝X坐标<br/>左膝Y坐标<br/>右膝X坐标<br/>右膝Y坐标<br/>左踝X坐标<br/>左踝Y坐标<br/>右踝X坐标<br/>右踝Y坐标 |
| ALGORITHM_LICENSE_RECOGNITION | 车牌识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | 检测到的车牌ID<br/>检测到的车牌名称<br/>检测到的车牌中心X坐标<br/>检测到的车牌中心Y坐标<br/>检测到的车牌宽度<br/>检测到的车牌高度<br/>车牌内容（例如车牌号码） |
| ALGORITHM_OCR_RECOGNITION | 光学字符识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | 检测到的字符ID<br/>检测到的字符名称<br/>检测到的字符中心X坐标<br/>检测到的字符中心Y坐标<br/>检测到的字符宽度<br/>检测到的字符高度<br/>检测到的字符内容 |
| ALGORITHM_LINE_TRACKING | 巡线追踪  | xTarget<br/>yTarget<br/>angle<br/>length  | 被追踪直线的X分量<br/>被追踪直线的Y分量<br/>被追踪直线的角度<br/>被追踪直线的长度 |
| ALGORITHM_EMOTION_RECOGNITION | 表情识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>  | 检测到的表情ID<br/>检测到的表情名称<br/>检测到的表情中心X坐标<br/>检测到的表情中心Y坐标<br/>检测到的表情宽度<br/>检测到的表情高度 |
| ALGORITHM_TAG_RECOGNITION | 标签识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | 检测到的标签 ID<br/>检测到的标签名称<br/>检测到的标签中心X坐标<br/>检测到的标签中心Y坐标<br/>检测到的标签宽度<br/>检测到的标签高度<br/>检测到的标签内容 |
| ALGORITHM_QRCODE_RECOGNITION | 二维码识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | 检测到的二维码ID<br/>检测到的二维码名称<br/>检测到的二维码中心X坐标<br/>检测到的二维码中心Y坐标<br/>检测到的二维码宽度<br/>检测到的二维码高度<br/>检测到的二维码内容 |
| ALGORITHM_BARCODE_RECOGNITION | 条形码识别  | ID<br/>name<br/>xCenter<br/>yCenter<br/>width<br/>height<br/>content  | 检测到的条形码ID<br/>检测到的条形码名称<br/>检测到的条形码中心X坐标<br/>检测到的条形码中心Y坐标<br/>检测到的条形码宽度<br/>检测到的条形码高度<br/>检测到的条形码内容 |

## 兼容性

|开发板         | 正常运行 | 运行失败  | 未测试 | 备注 |
| ------------ | :--: | :----: | :----: | :--: |
| 树莓派 4B |  √   |        |        |      |


* Python 版本

| Python  | 正常运行 | 运行失败 | 未测试 | 备注 |
| ------- | :--: | :----: | :----: | ---- |
| Python2 |      |        |     √  |      |
| Python3 |  √   |        |        |      |

## 更改历史 

- 2026/4/22 - Version 1.0.0 released.

## 作者

Written by Yx(yixuan.niu@dfrobot.com), 2026.4.22 (Welcome to our [website](https://www.dfrobot.com.cn/))