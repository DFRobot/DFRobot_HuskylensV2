# 发布说明
| 版本 | 日期  | 发布人  | 邮箱 | 说明 |
| :--: | :----: | :--: | :----: | :----: |
| V0.1 | 2025-11-07  | 王辉  | ouki.wang@dfrobot.com | 初始版本 |
| V0.2 | 2025-11-26 | 王辉  | ouki.wang@dfrobot.com | 1. 添加获取读写算法参数api<br/>2.  删除RETURN_OK，统一使用RETURN_ARGS<br/>3.  修改命令号，算法号<br/> 4.  将设置矩形的x1 y1 x2 y2改为x y widht height<br/> |
| V0.3 | 2026-10-13 | 王辉 | ouki.wang@dfrobot.com | 添加智能体（Agent）命令：GET_AGENT_RESPONSE(0x33)、SEND_AGENT_PROMPT(0x34)、GET_AGENT_STATUS(0x35)、IS_AGENT_RESPONSE_READY(0x36) |
| V0.4 | 2026-10-29 | 王辉 | ouki.wang@dfrobot.com | 将Data段从10字节增大到14字节 |

## 通用命令/响应
| Head55 | HeadAA  | CMD  | Data Length | Data | Checksum |
| :--: | :----: | :--: | :----: | :----: | :----: |
| 0x55 | 0xAA | 1 byte  | 1 byte | 0-n bytes | 1 byte|

## 算法ID
| ID | 算法  | 说明  |
| :--: | :----: | :--: |
| 0 | 通用ID（None） | 用于握手，切换算法等通用命令  |
| 1 | 人脸识别（FACE_RECOGNITION） | 有五官数据 |
| 2 | 物体识别（OBJECT_RECOGNITION） |  |
| 3 | 物体追踪（OBJECT_TRACKING） |  |
| 4 | 颜色识别（COLOR_RECOGNITION） |  |
| 5 | 物体分类（OBJECT_CLASSIFICATION） |  |
| 6 | 自学习分类（SELF_LEARNING_CLASSIFICATION） |  |
| 7 | 实例分割（SEGMENT） |  |
| 8 | 手势识别（HAND_RECOGNITION） | 有手指关键点数据 |
| 9 | 姿态识别（POSE_RECOGNITION） | 有人体关键点数据 |
| 10 | 车牌识别（LICENSE_RECOGNITION） |  |
| 11 | 光学字符识别（OCR_RECOGNITION） |  |
| 12 | 巡线（LINE_TRACKING） |  |
| 13 | 表情识别（EMOTION_RECOGNITION） |  |
| 14 | 目光注视（GAZE_RECOGNITION） |  |
| 15 | 面部朝向（FACE_ORIENTATION） |  |
| 16 | 标签识别（TAG_RECOGNITION） |  |
| 17 | 条形码（BARCODE_RECOGNITION） |  |
| 18 | 二维码（QRCODE_RECOGNITION） |  |
| 19 | 跌倒检测（FALLDOWN_RECOGNITION） |  |
| 20 | 深度检测（DEPTH_DETECTION） |  |
| 21 | 自动驾驶-智慧交通（AUTO_DRIVE_1） | 结果包含转向角度(steering)和油门(throttle) |
| 22 | 自动驾驶-城市道路（AUTO_DRIVE_2） | 结果包含转向角度(steering)和油门(throttle) |
| ... | ... |  |
| 100-127 | 预留 |  |
| 128-255| 用户安装的模型 |  |

## ID含义
| ID | 含义  | 特殊说明  |
| :--: | :----: | :--: |
| 0 | 未学习过的ID | 在巡线应用中，默认ID为0，如果学习多种颜色赛道，ID表示学习的颜色ID  |
| 1-n | 学习过的ID |   |

## 可直接使用的内置Clolor宏
| COLOR宏 | 中文名称  | RGB |
| :----: | :--: | :--: |
| COLOR_WHITE | 白色  | (255, 255, 255) |
| COLOR_RED | 红色  | (255, 0, 0) |
| COLOR_ORANGE | 橙色  | (255, 165, 0) |
| COLOR_YELLOW | 黄色  | (255, 255, 0) |
| COLOR_GREEN | 绿色  | (0, 255, 0) |
| COLOR_CYAN | 青色  | (0, 255, 255) |
| COLOR_BLUE | 蓝色  | (0, 0, 255)|
| COLOR_PURPLE | 紫色  | (128, 0, 128)|
| COLOR_PINK | 粉色  | (255, 192, 203)|
| COLOR_GRAY | 灰色  | (128, 128, 128)|
| COLOR_BLACK | 黑色  | (0, 0, 0)|
| COLOR_BROWN | 棕色  | (165, 42, 42)|
| COLOR_OLIVE | 橄榄绿  | (128, 128, 0)|
| COLOR_TEAL | 蓝绿色  | (0, 128, 128)|
| COLOR_INDIGO | 靛蓝色  | (75, 0, 130)|
| COLOR_MAGENTA | 洋红色  | (255, 0, 255)|

## 1. KNOCK(0x00)
和二哈握手，告诉二哈自己是大内存的mcu还是小内存的mcu
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x00  | 1 byte | 14 |14 bytes |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

**Data段**
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1  | boardType<br/>(0 small ram) <br/>(1 large ram) |
| 1 | 13 | RFU  |

## 2. GET_RESULT(0x01)
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x01  | 1 byte | 0 |1 byte |

返回命令序列：RETURN_INFO RETURN_BLOCK... RETURN_ARROW...

## 3. GET_ALGO_PARAM(0x02)
获取算法参数
假设key 的长度为 n

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data |Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x02  | 1 byte | 14+n+1 | 14+n+1 bytes |1 byte|

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | 0 |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 4 | 2 | 0 |
| 6 | 2 | 0 |
| 8 | 2 | 0 |
| 10 | 4 | 0 |
| 14 | 1 | key length |
| 15 | n | key |

## 4. RFU(0x03)
## 5. RFU(0x04)
## 6. RFU(0x05)
## 7. RFU(0x06)
## 8. SET_ALGORITHM(0x0A)
切换算法
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0A | 1 byte | 14 |14 bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | algoID(目标算法ID) |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 4 | 2 | 0 |
| 6 | 2 | 0 |
| 8 | 2 | 0 |
| 10 | 4 | 0 |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 9. SET_NAME_BY_ID(0x0B)
根据已学习ID（ID>0）设置名称（假设设置的名称长度为n   0 < n < =32）,支持中文，中文请使用utf-8编码

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0B | 1 byte | 14+1+n |14+1+n bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | ID（已学习ID） |
| 1 | 1 | RFU0 |
| 2 | 2 | RFU1 |
| 4 | 2 | RFU2 |
| 6 | 2 | RFU3 |
| 8 | 2 | RFU4 |
| 10 | 4 | RFU5 |
| 14 | 1 | name length |
| 15 | n | name |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 10. SET_MULTI_ALGORITHM(0x0C)
创建组合算法，只允许创建一个组合算法，一个组合算法内最多支持3个子算法

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0C | 0 | 14 |14 bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | multiAlgoNum（多算法数目） |
| 1 | 1 | RFU0 |
| 2 | 2 | AlgoID0 |
| 4 | 2 | AlgoID1 |
| 6 | 2 | AlgoID2 |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 11. SET_MULTI_ALGORITHM_RATIO(0x0D)
设置组合算法运算比，运算比个数必须和算法个数相同
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0D | 0 | 14 |14 bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | multiAlgoNum（多算法数目） |
| 1 | 1 | RFU0 |
| 2 | 2 | AlgoID0Ratio |
| 4 | 2 | AlgoID1Ratio |
| 6 | 2 | AlgoID2Ratio |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 12. SET_ALGO_PARAMS(0x0E)
设置算法参数
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0E | 1 byte | 14+n+m+2 |14+n+m+2 bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 |  |
| 1 | 1 |  |
| 2 | 2 | arg0(number) |
| 4 | 2 |  |
| 6 | 2 |  |
| 8 | 2 |  |
| 10 | 4 | RFU0 |
| 14 | 1 | key（string） length |
| 15 | n |  |
| 15+n | 1 | arg0（string）length |
| 15+n+1 | m | arg0（string） |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 12. COMMAND_UPDATE_ALGORITHM_PARAMS(0x0F)

设置算法参数

| Head55 | HeadAA | CMD  | Algo ID | Data Length | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: |
|  0x55  |  0xAA  | 0x0F | 1 byte  |      0      |  1 byte  |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败



## 13. RETURN_ARGS(0x1A)

返回参数最多4个数字参数和2个string参数
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data |Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1A | 1 byte | 14 + 2 + n + m |14 + 2+ n + m bytes|1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | totalIntArgs 返回的int参数个数 |
| 1 | 1 | 执行结果 0表示成功，1表示失败 |
| 2 | 2 | arg0_int |
| 4 | 2 |  |
| 6 | 2 |  |
| 8 | 2 |  |
| 10 | 4 | |
| 14 | 1 | key（string） length |
| 15 | n |  |
| 15+n | 1 | arg0（string）length |
| 15+n+1 | m | arg0（string） |


## 14. RETURN_INFO（0x1B）
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1B | 1 byte | 14 |14 bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 |  maxID（已学习的最大数目） |
| 1 | 1 | RFU0 |
| 2 | 2 | total_results（总识别数目） |
| 4 | 2 | total_results_learned（已学习的总数目） |
| 6 | 2 | total_blocks （总识别block数目）|
| 8 | 2 | total_blocks_learned （已学习的block总数目）|
| 10 | 4 | RFU1 |


## 15. RETURN_BLOCKS（0x1C）
假设block的name长度n，content长度为m
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1C | 1 byte | 14+2+n+m+私有数据长度 |14+2+n+m bytes+私有数据长度 bytes |1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | ID |
| 1 | 1 | Algo ID |
| 2 | 2 | xCenter |
| 4 | 2 | yCenter |
| 6 | 2 | width |
| 8 | 2 | height |
| 10 | 4 | confidence |
| 14 | 1 | name length |
| 15 | n | name |
| 15+n | 1 | content length |
| 15+n+1 | m | content |
|  |  | 算法私有数据 |

## 16. RETURN_ARROWS(0x1D)
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1D | 1 byte | 14 |14 bytes |1 byte |

Data段
返回的数据是向量，level 1级别向量的起点是屏幕做下边缘中点（320，480），中垂线为角度0，顺时针旋转可增长到90度，逆时针旋转可减少到-90度。level 2级别的向量起点是level 1级别向量终点。因此支持不同级别向量想加的操作。
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | ID |
| 1 | 1 | RFU0 |
| 2 | 2 | xTarget |
| 4 | 2 | yTarget |
| 6 | 2 | angle（-90，90） |
| 8 | 2 | length |
| 10 | 4 | RFU1 |



## 17. ACTION_TAKE_PHOTO(0x20)
拍照
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x20  | 0 | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败
arg0_str 是照片文件名

## 18. ACTION_TAKE_SCREENSHOT(0x21)
截屏
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x21 | 0 | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败
arg0_str 是截图文件名

## 19. ACTION_LEARN(0x22)
学习成功，返回ID 非0，学习失败返回ID0
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x22 | 0 | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败
arg0_int 是学习id，0 表示为学习到，>=1表示学习的id

## 20. ACTION_FORGET(0x23)
遗忘所有
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x23 | 0 | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 21. ACTION_SAVE_KNOWLEDGES(0x24)
保存当前配置到知识库
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x24  | 1 byte | 14 |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | knowLedges_id  range[0, 4] |
| 1 | 13 | RFU |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 22. ACTION_LOAD_KNOWLEDGES(0x25)
加载知识库
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x25  | 1 byte | 14  |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | knowLedges_id range[0, 4] |
| 1 | 13 | RFU |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 23. ACTION_DRAW_RECT(0x26)
画一个矩形
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x26  | 1 byte | 14 |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | 0 |
| 1 | 1 | lineWidth |
| 2 | 2 | x |
| 4 | 2 | y |
| 6 | 2 | width |
| 8 | 2 | height |
| 10 | 4 | RGBA |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 24. ACTION_CLEAN_RECT(0x27)
清除所有通过通信协议绘制的矩形
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x27  | 1 byte | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 25. ACTION_DRAW_TEXT(0x28)
在特定坐标处绘制文本
fontSize 只支持[20, 24, 26, 27, 28, 32, 36, 40, 48]

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: | ---- |
| 0x55 | 0xAA  | 0x28  | 1 byte | 14+1+n | 14+1+n Bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | fontSize |
| 2 | 2 | x |
| 4 | 2 | y |
| 6 | 2 | RFU1 |
| 8 | 2 | RFU2 |
| 10 | 4 | RGBA |
| 14 | 1 | Text length |
| 15 | n | text |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 26. ACTION_CLEAN_TEXT(0x29)
清除所有通过通信协议绘制的矩形
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x29 | 1 byte | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 27. ACTION_PLAY_MUSIC(0x2A)
播放音频
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x2A | 0 | 14+1+n | 14+1+n bytes | 1byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | RFU1 |
| 2 | 2 | colume |
| 4 | 2 | RFU2 |
| 6 | 2 | RFU3 |
| 8 | 2 | RFU4 |
| 10 | 4 | RFU5 |
| 14 | 1 | name length |
| 15 | n | name |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 28. ACTION_EXIT(0x2B)
退出当前应用，如果当前是在主菜单，则不再退出
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x2B | 1 byte | 0  |1 byte |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 29. ACTION_LEARN_BLOCK(0x2C)
设置学习框的位置和大小（目前只可用于物体追踪）
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data| Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x2C | 1 byte | 14 |14 bytes|1 byte |

Data段
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | RFU1 |
| 2 | 2 | x |
| 4 | 2 | y |
| 6 | 2 | width |
| 8 | 2 | height |
| 10 | 4 | RFU2 |

返回命令：RETURN_ARGS，其中retValue=0表示执行成功，其他值表示执行失败。arg0_int是学习ID，0表示未学习到，>=1表示学习的ID

## 30. ACTION_DRAW_UNIQUE_RECT(0x2D)
画唯一矩形，屏幕上之前绘制的其他矩形会被清除
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data| Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x2D | 1 byte | 14 |14 bytes|1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | RFU |
| 1 | 1 | lineWidth |
| 2 | 2 | x |
| 4 | 2 | y |
| 6 | 2 | width |
| 8 | 2 | height |
| 10 | 4 | RGB |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败

## 31. ACTION_START_RECORDING(0x2E)

开始录制音频或视频，filename可省略

| Head55 | HeadAA | CMD  | Algo ID | Data Length |     Data     | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :----------: | :------: |
|  0x55  |  0xAA  | 0x2E |    0    |   14+1+n    | 14+1+n bytes |  1 byte  |

Data

| offset | length |                             name                             |
| :----: | :----: | :----------------------------------------------------------: |
|   0    |   1    | 0:              default<br/> 1:           640x480 <br/>2:       1280x720 <br/>3:     1920x1080<br/> |
|   1    |   1    | 1:           audio<br/> 2:           video <br/>3:      ( audio+video ) |
|   2    |   2    |                           duration                           |
|   4    |   2    |                             RFU0                             |
|   6    |   2    |                             RFU1                             |
|   8    |   2    |                             RFU2                             |
|   10   |   4    |                             RFU3                             |
|   14   |   1    |                       filename length                        |
|   15   |   n    |                           filename                           |

返回命令：RETURN_ARGS retValue=0 表示执行成功 其他值表示执行失败，附带文件名或错误信息



## 32. ACTION_STOP_RECORDING(0x2F)

停止录制音频或视频

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x2F |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length |                             name                             |
| :----: | :----: | :----------------------------------------------------------: |
|   0    |   1    |                              0                               |
|   1    |   1    | 1:           audio<br/> 2:           video <br/>3:      ( audio+video ) |
|   2    |   12   |                              0                               |

返回命令：RETURN_ARGS，其中retValue=0表示执行成功，其他值表示执行失败，附带文件名或错误信息

## 33. GET_AGENT_RESPONSE(0x33)

获取智能体（Agent）的回答内容。回答较长时设备按分片返回：主机循环发送本命令，设备按序推进分片，应答中携带 fragmentCount 和 fragmentIndex，主机据此去重检漏，收齐全部 fragmentCount 个分片后拼接得到完整回答。

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x33 |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType（0：小智Agent） |
| 2 | 12 | RFU |

返回命令：RETURN_ARGS

应答 Data 段

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU |
| 1 | 1 | retValue：0 表示成功，其他值表示失败（如回答未就绪） |
| 2 | 2 | fragmentCount（回答总分片数） |
| 4 | 2 | fragmentIndex（当前分片序号，从 0 开始） |
| 6 | 2 | RFU0 |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |
| 14 | 1 | 回答分片 length |
| 15 | n | 回答分片内容（UTF-8） |

## 34. SEND_AGENT_PROMPT(0x34)

向智能体（Agent）发送提示词。提示词按 UTF-8 字节流分片发送，Data Length 为单字节，整包数据段不能超过 255 字节，因此每片内容最多 244 字节（参考实现使用 238 字节）。分片序号从 0 开始，设备收齐 fragmentCount 个分片后开始处理。

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x34 |    0    |   14+1+n   | 14+1+n bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType（0：小智Agent） |
| 2 | 2 | fragmentCount（总分片数） |
| 4 | 2 | fragmentIndex（当前分片序号，从 0 开始） |
| 6 | 2 | RFU0 |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |
| 14 | 1 | 提示词分片 length |
| 15 | n | 提示词分片内容（UTF-8） |

返回命令：RETURN_ARGS retValue=0 表示本分片接收成功，其他值表示失败

## 35. GET_AGENT_STATUS(0x35)

查询智能体（Agent）当前状态。

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x35 |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType（0：小智Agent） |
| 2 | 12 | RFU |

返回命令：RETURN_ARGS

应答 Data 段

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU |
| 1 | 1 | retValue：0 表示查询成功，其他值表示失败 |
| 2 | 2 | RFU |
| 4 | 2 | 状态码：0=idle（空闲）<br/>1=processing（处理中）<br/>2=broadcasting（播报中）<br/>3=disabled（小智开关未打开）<br/> |
| 6 | 8 | RFU |

注：旧版固件的应答中可能不包含状态码字段，此时主机应按 idle 处理。

## 36. IS_AGENT_RESPONSE_READY(0x36)

查询智能体（Agent）的回答是否已就绪。

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x36 |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType（0：小智Agent） |
| 2 | 12 | RFU |

返回命令：RETURN_ARGS retValue=0 表示回答已就绪，可通过 GET_AGENT_RESPONSE 获取；其他值表示尚未就绪

# 私有数据

## 人脸私有数据
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 2 | leye_x |
| 2 | 2 | leye_y |
| 4 | 2 | reye_x |
| 6 | 2 | reye_y |
| 8 | 2 | nose_x |
| 10 | 2 | nose_y |
| 12 | 2 | lmouth_x |
| 14 | 2 | lmouth_y |
| 16 | 2 | rmouth_x |
| 18 | 2 | rmouth_y |

## 手势私有数据
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 2 | wrist_x |
| 2 | 2 | wrist_y |
| 4 | 2 | thumb_cmc_x |
| 6 | 2 | thumb_cmc_y |
| 8 | 2 | thumb_mcp_x |
| 10 | 2 | thumb_mcp_y |
| 12 | 2 | thumb_ip_x |
| 14 | 2 | thumb_ip_y |
| 16 | 2 | thumb_tip_x |
| 18 | 2 | thumb_tip_y |
| 20 | 2 | index_finger_mcp_x |
| 22 | 2 | index_finger_mcp_y |
| 24 | 2 | index_finger_pip_x |
| 26 | 2 | index_finger_pip_y |
| 28 | 2 | index_finger_dip_x |
| 30 | 2 | index_finger_dip_y |
| 32 | 2 | index_finger_tip_x |
| 34 | 2 | index_finger_tip_y |
| 36 | 2 | middle_finger_mcp_x |
| 38 | 2 | middle_finger_mcp_y |
| 40 | 2 | middle_finger_pip_x |
| 42 | 2 | middle_finger_pip_y |
| 44 | 2 | middle_finger_dip_x |
| 46 | 2 | middle_finger_dip_y |
| 48 | 2 | middle_finger_tip_x |
| 50 | 2 | middle_finger_tip_y |
| 52 | 2 | ring_finger_mcp_x |
| 54 | 2 | ring_finger_mcp_y |
| 56 | 2 | ring_finger_pip_x |
| 58 | 2 | ring_finger_pip_y |
| 60 | 2 | ring_finger_dip_x |
| 62 | 2 | ring_finger_dip_y |
| 64 | 2 | ring_finger_tip_x |
| 66 | 2 | ring_finger_tip_y |
| 68 | 2 | pinky_finger_mcp_x |
| 70 | 2 | pinky_finger_mcp_y |
| 72 | 2 | pinky_finger_pip_x |
| 74 | 2 | pinky_finger_pip_y |
| 76 | 2 | pinky_finger_dip_x |
| 78 | 2 | pinky_finger_dip_y |
| 80 | 2 | pinky_finger_tip_x |
| 82 | 2 | pinky_finger_tip_y |

## 姿态私有数据
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 2 | nose_x |
| 2 | 2 | nose_y |
| 4 | 2 | leye_x |
| 6 | 2 | leye_y |
| 8 | 2 | reye_x |
| 10 | 2 | reye_y |
| 12 | 2 | lear_x |
| 14 | 2 | lear_y |
| 16 | 2 | rear_x |
| 18 | 2 | rear_y |
| 20 | 2 | lshoulder_x |
| 22 | 2 | lshoulder_y |
| 24 | 2 | rshoulder_x |
| 26 | 2 | rshoulder_y |
| 28 | 2 | lelbow_x |
| 30 | 2 | lelbow_y |
| 32 | 2 | relbow_x |
| 34 | 2 | relbow_y |
| 36 | 2 | lwrist_x |
| 38 | 2 | lwrist_y |
| 40 | 2 | rwrist_x |
| 42 | 2 | rwrist_y |
| 44 | 2 | lhip_x |
| 46 | 2 | lhip_y |
| 48 | 2 | rhip_x |
| 50 | 2 | rhip_y |
| 52 | 2 | lknee_x |
| 54 | 2 | lknee_y |
| 56 | 2 | rknee_x |
| 58 | 2 | rknee_y |
| 60 | 2 | lankle_x |
| 62 | 2 | lankle_y |
| 64 | 2 | rankle_x |
| 66 | 2 | rankle_y |
