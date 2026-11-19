# 二哈识图V2

* [English Version](README.md)


## 目录

* [简介](#简介)
* [安装](#安装)
* [方法](#方法)
* [算法](#算法)
* [兼容性](#兼容性)
* [更改历史](#更改历史)
* [作者](#作者)

## 简介

这个库提供了一个在Arduino兼容板上驱动二哈识图V2的接口。它支持UART和I2C通信协议，并提供各种计算机视觉算法，如物体识别、人脸检测、巡线等功能。

> [!WARNING]
> **固件要求：本Arduino库仅支持v1.4.2及以上版本的二哈识图V2固件。** 使用前请将设备固件升级至v1.4.2及以上版本，否则可能出现通信失败或返回结果错误的情况。

## 安装

1. 从GitHub下载库文件
2. 解压zip文件
3. 将解压后的文件夹移动到您的Arduino库目录
4. 重启Arduino IDE
5. 在您的ino文件中包含库：`#include <DFRobot_HuskylensV2.h>`

或者，您也可以通过Arduino库管理器搜索"DFRobot_HuskylensV2"来安装此库。

## 方法

### 初始化方法

```cpp
/**
 * @fn begin
 * @brief 使用UART通信初始化二哈识图V2
 * @param streamInput 用于通信的串口
 * @return 初始化成功返回true，否则返回false
 */
bool begin(Stream &streamInput);

/**
 * @fn begin
 * @brief 使用I2C通信初始化二哈识图V2
 * @param streamInput 用于通信的I2C接口
 * @return 初始化成功返回true，否则返回false
 */
bool begin(TwoWire &streamInput);

/**
 * @fn knock
 * @brief 检查二哈识图V2是否已连接
 * @return 二哈识图V2已连接返回true，否则返回false
 */
bool knock(void);
```

### 算法控制方法

```cpp
/**
 * @fn switchAlgorithm
 * @brief 切换二哈识图V2的算法，如果是自己安装的算法，请到目标算法UI的菜单中中找到Algo ID
 * @param algo 要切换的算法
 * @return 算法切换成功返回true，否则返回false
 */
bool switchAlgorithm(eAlgorithm_t algo);

/**
 * @fn getResult
 * @brief 获取二哈识图V2的识别结果
 * @param algo 要获取结果的算法
 * @return 成功返回COMMAND_RETURN_ARGS，retValue==0，其他值表示错误
 */
int8_t getResult(eAlgorithm_t &algo);

/**
 * @fn available
 * @brief 检查特定算法是否有结果可用
 * @param algo 要检查的算法
 * @return 有结果可用返回true，否则返回false
 */
bool available(eAlgorithm_t algo);
```

### 结果获取方法

```cpp
/**
 * @fn popCachedResult
 * @brief 从结果队列中弹出一个缓存的结果
 * @param algo 要获取结果的算法
 * @return 指向结果的指针，如果没有可用结果则返回NULL
 */
Result *popCachedResult(eAlgorithm_t algo);

/**
 * @fn getCachedCenterResult
 * @brief 获取最接近屏幕中心的结果
 * @param algo 要获取结果的算法
 * @return 指向中心结果的指针，如果没有可用结果则返回NULL
 */
Result *getCachedCenterResult(eAlgorithm_t algo);

/**
 * @fn getCachedResultByIndex
 * @brief 通过索引获取缓存的结果
 * @param algo 要获取结果的算法
 * @param index 结果的索引
 * @return 指向结果的指针，如果指定索引处没有可用结果则返回NULL
 */
Result *getCachedResultByIndex(eAlgorithm_t algo, int16_t index);

/**
 * @fn getCachedResultByID
 * @brief 通过ID获取缓存的结果
 * @param algo 要获取结果的算法
 * @param ID 要检索的对象ID
 * @return 指向结果的指针，如果没有指定ID的结果则返回NULL
 */
Result *getCachedResultByID(eAlgorithm_t algo, int16_t ID);

/**
 * @fn getCachedResultNum
 * @brief 获取缓存结果的数量
 * @param algo 要获取结果的算法
 * @return 缓存结果的数量
 */
int16_t getCachedResultNum(eAlgorithm_t algo);

/**
 * @fn getCachedResultLearnedNum
 * @brief 获取已学习结果的数量
 * @param algo 要获取结果的算法
 * @return 已学习结果的数量
 */
int16_t getCachedResultLearnedNum(eAlgorithm_t algo);
```

### 结果结构

上述所有结果获取方法均返回一个指向 `Result` 对象的指针。`Result` 类携带了 HuskyLens V2 在 `RETURN_BLOCKS` 协议帧中上报的通用字段：

| 字段 | 类型 | 说明 |
| :--: | :----: | :--: |
| ID | uint8_t | 对象的学习ID，0表示未学习 |
| xCenter | int16_t | 区块中心X坐标 |
| yCenter | int16_t | 区块中心Y坐标 |
| width | int16_t | 区块宽度 |
| height | int16_t | 区块高度 |
| conf | float | 识别结果的置信度（仅对方块（block）类型结果有效；巡线返回的箭头类型结果不包含此字段） |
| name | String | 识别对象的名称 |
| content | String | 识别对象的内容（如二维码文本），算法不上报时为空 |

### 学习和知识管理方法

```cpp
/**
 * @fn learn
 * @brief 使用当前算法学习对象
 * @param algo 用于学习的算法
 * @return 学习成功返回true，否则返回false
 */
bool learn(eAlgorithm_t algo);

/**
 * @fn learnBlock
 * @brief 学习特定的区块
 * @param algo 用于学习的算法
 * @param x 区块左上角的x坐标
 * @param y 区块左上角的y坐标
 * @param width 区块的宽度
 * @param height 区块的高度
 * @return 学习成功返回true，否则返回false
 */
bool learnBlock(eAlgorithm_t algo, int16_t x, int16_t y, int16_t width, int16_t height);

/**
 * @fn forget
 * @brief 忘记特定算法的所有已学习对象
 * @param algo 要忘记已学习对象的算法
 * @return 忘记成功返回true，否则返回false
 */
bool forget(eAlgorithm_t algo);

/**
 * @fn saveKnowledges
 * @brief 将已学习的知识保存到特定的知识ID
 * @param algo 要保存知识的算法
 * @param knowledgeID 保存知识的ID
 * @return 保存成功返回true，否则返回false
 */
bool saveKnowledges(eAlgorithm_t algo, uint8_t knowledgeID);

/**
 * @fn loadKnowledges
 * @brief 从特定的知识ID加载已学习的知识
 * @param algo 要加载知识的算法
 * @param knowledgeID 加载知识的ID
 * @return 加载成功返回true，否则返回false
 */
bool loadKnowledges(eAlgorithm_t algo, uint8_t knowledgeID);
```

### 显示控制方法

```cpp
/**
 * @fn drawRect
 * @brief 在二哈识图显示屏上绘制矩形
 * @param algo 算法上下文
 * @param colorID 矩形的颜色ID
 * @param lineWidth 矩形的线宽
 * @param x 左上角的x坐标
 * @param y 左上角的y坐标
 * @param width 矩形的宽度
 * @param height 矩形的高度
 * @return 绘制成功返回true，否则返回false
 */
bool drawRect(eAlgorithm_t algo, uint8_t colorID, uint8_t lineWidth, int16_t x, int16_t y, int16_t width, int16_t height);

/**
 * @fn drawRect
 * @brief 在二哈识图显示屏上唯一矩形，执行这个函数时，之前绘制的矩形会被自动擦除
 * @param algo 算法上下文
 * @param colorID 矩形的颜色ID
 * @param lineWidth 矩形的线宽
 * @param x 左上角的x坐标
 * @param y 左上角的y坐标
 * @param width 矩形的宽度
 * @param height 矩形的高度
 * @return 绘制成功返回true，否则返回false
 */
bool drawUniqueRect(eAlgorithm_t algo, uint8_t colorID, uint8_t lineWidth, int16_t x, int16_t y, int16_t width, int16_t height);


/**
 * @fn drawText
 * @brief 在二哈识图显示屏上绘制文本
 * @param algo 算法上下文
 * @param colorID 文本的颜色ID
 * @param fontSize 文本的字体大小
 * @param x 文本位置的x坐标
 * @param y 文本位置的y坐标
 * @param text 要绘制的文本
 * @return 绘制成功返回true，否则返回false
 */
bool drawText(eAlgorithm_t algo, uint8_t colorID, uint8_t fontSize, int16_t x, int16_t y, String text);

/**
 * @fn clearRect
 * @brief 清除二哈识图显示屏上的所有矩形
 * @param algo 算法上下文
 * @return 清除成功返回true，否则返回false
 */
bool clearRect(eAlgorithm_t algo);

/**
 * @fn clearText
 * @brief 清除二哈识图显示屏上的所有文本
 * @param algo 算法上下文
 * @return 清除成功返回true，否则返回false
 */
bool clearText(eAlgorithm_t algo);
```

### 多算法支持（适用于大内存开发板）

```cpp
/**
 * @fn setMultiAlgorithm
 * @brief 设置多个算法同时运行（仅适用于大内存开发板）
 * @param algo0 第一个算法id
 * @param algo1 第二个算法id
 * @param algo2 第三个算法id（默认：ALGORITHM_ANY）
 * @return 设置成功返回true，否则返回false
 */
bool setMultiAlgorithm(eAlgorithm_t algo0, eAlgorithm_t algo1, eAlgorithm_t algo2 = ALGORITHM_ANY);

/**
 * @fn setMultiAlgorithmRatio
 * @brief 设置多个算法同时运行（仅适用于大内存开发板）
 * @param ratio0 第一个算法时间占用比
 * @param ratio1 第二个算法时间占用比
 * @param ratio2 第三个算法时间占用比（默认：0）
 * @return 设置成功返回true，否则返回false
 */
bool setMultiAlgorithmRatio(uint8_t ratio0, uint8_t ratio1, uint8_t ratio2 = 0);
```

## 算法

二哈识图V2包含多种算法，每种算法在结果中产生不同的元素。
有关上述API中**algo**和**result**形参允许的实参，请参见下表。

| 算法枚举 | 算法说明 | 结果元素 |
| :--: | :----: | :--: |
| ALGORITHM_ANY | 任意算法 | 根据活动算法而变化 |
| ALGORITHM_FACE_RECOGNITION | 人脸识别 | ID、name、xCenter、yCenter、width、height、眼睛坐标、嘴巴坐标、鼻子坐标 |
| ALGORITHM_OBJECT_TRACKING | 物体追踪 | ID、name、xCenter、yCenter、width、height |
| ALGORITHM_OBJECT_RECOGNITION | 物体识别 | ID、name、xCenter、yCenter、width、height |
| ALGORITHM_LINE_TRACKING | 巡线追踪 | xTarget、yTarget、angle、length |
| ALGORITHM_COLOR_RECOGNITION | 颜色识别 | ID、name、xCenter、yCenter、width、height |
| ALGORITHM_TAG_RECOGNITION | 标签识别 | ID、name、xCenter、yCenter、width、height、content |
| ALGORITHM_SELF_LEARNING_CLASSIFICATION | 自学习分类 | ID、name |
| ALGORITHM_OCR_RECOGNITION | 光学字符识别 | ID、name、xCenter、yCenter、width、height、content |
| ALGORITHM_LICENSE_RECOGNITION | 车牌识别 | ID、name、xCenter、yCenter、width、height、content |
| ALGORITHM_QRCODE_RECOGNITION | 二维码识别 | ID、name、xCenter、yCenter、width、height、content |
| ALGORITHM_BARCODE_RECOGNITION | 条形码识别 | ID、name、xCenter、yCenter、width、height、content |
| ALGORITHM_EMOTION_RECOGNITION | 表情识别 | ID、name、xCenter、yCenter、width、height |
| ALGORITHM_POSE_RECOGNITION | 姿态识别 | ID、name、xCenter、yCenter、width、height、身体关节坐标 |
| ALGORITHM_HAND_RECOGNITION | 手势识别 | ID、name、xCenter、yCenter、width、height、手部关节坐标 |
| ALGORITHM_SEGMENT | 实例分割 | ID、name、xCenter、yCenter、width、height |

## 兼容性

| 开发板 | 正常运行 | 运行失败 | 未测试 | 备注 |
| ------------ | :--: | :----: | :----: | :--: |
| Arduino UNO | √ | | | |
| Arduino Mega | √ | | | |
| Arduino Leonardo | √ | | | |
| ESP32 | √ | | | 大内存支持 |
| ESP8266 | √ | | | 大内存支持 |
| Raspberry Pi Pico | √ | | | |
| micro:bit | √ | | | 大内存支持 |

## 更改历史

- 2025/11/08 - 版本1.0.0发布。

## 作者

Written by Ouki.Wang(ouki.wang@dfrobot.com), 2025.11.08 (欢迎访问我们的[网站](https://www.dfrobot.com.cn/))
