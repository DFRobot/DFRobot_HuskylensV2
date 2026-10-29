# Release Note
| Version | Date  | Publisher  | E-mail | Description |
| :--: | :----: | :--: | :----: | :----: |
| V0.1 | 2025-11-07  | ouki.wang  | ouki.wang@dfrobot.com | First version |
| V0.2 | 2025-11-26 | ouki.wang  | ouki.wang@dfrobot.com | 1. Add API for retrieving read/write algorithm parameters<br/>2. Remove RETURN_OK and uniformly use RETURN_ARGS<br/>3. Modify command numbers and algorithm numbers<br/>4. Change rectangle setting from x1 y1 x2 y2 to x y width height |
| V0.3 | 2026-10-13 | ouki.wang | ouki.wang@dfrobot.com | Add agent commands: GET_AGENT_RESPONSE(0x33), SEND_AGENT_PROMPT(0x34), GET_AGENT_STATUS(0x35), IS_AGENT_RESPONSE_READY(0x36) |
| V0.4 | 2026-10-29 | ouki.wang | ouki.wang@dfrobot.com | Increase the Data segment from 10 bytes to 14 bytes |

## General Command/Response
| Head55 | HeadAA  | CMD  | Data Length | Data | Checksum |
| :--: | :----: | :--: | :----: | :----: | :----: |
| 0x55 | 0xAA | 1 byte  | 1 byte | 0-n bytes | 1 byte|

## Algorithm ID
| ID | Algorithm  | Description  |
| :--: | :----: | :--: |
| 0 | Universal ID（None） | For handshakes, algorithm switching, and other general-purpose commands  |
| 1 | FACE_RECOGNITION | Contain facial feature data |
| 2 | OBJECT_RECOGNITION |  |
| 3 | OBJECT_TRACKING |  |
| 4 | COLOR_RECOGNITION |  |
| 5 | OBJECT_CLASSIFICATION |  |
| 6 | SELF_LEARNING_CLASSIFICATION |  |
| 7 | SEGMENT |  |
| 8 | HAND_RECOGNITION | Contain finger key point data |
| 9 | POSE_RECOGNITION | Contain human body key point data |
| 10 | LICENSE_RECOGNITION |  |
| 11 | OCR_RECOGNITION |  |
| 12 | LINE_TRACKING |  |
| 13 | EMOTION_RECOGNITION |  |
| 14 | GAZE_RECOGNITION |  |
| 15 | FACE_ORIENTATION |  |
| 16 | TAG_RECOGNITION |  |
| 17 | BARCODE_RECOGNITION |  |
| 18 | QRCODE_RECOGNITION |  |
| 19 | FALLDOWN_RECOGNITION |  |
| 20 | DEPTH_DETECTION |  |
| 21 | AUTO_DRIVE_1 | Auto Drive Smart Traffic; result contains steering and throttle |
| 22 | AUTO_DRIVE_2 | Auto Drive City Roads; result contains steering and throttle |
| ... | ... |  |
| 100-127 | RESERVE |  |
| 128-255| User installed model |  |

## ID
| ID | Meaning  | Description  |
| :--: | :----: | :--: |
| 0 | Unlearned ID | In the line-following application, the default ID is 0. If multiple colored tracks are learned, the ID represents the color ID being learned.  |
| 1-n | Learned ID |   |

## Color Macros
| COLOR Macro | Name  | RGB |
| :----: | :--: | :--: |
| COLOR_WHITE | White  | (255, 255, 255) |
| COLOR_RED | Red  | (255, 0, 0) |
| COLOR_ORANGE | Orange  | (255, 165, 0) |
| COLOR_YELLOW | Yellow  | (255, 255, 0) |
| COLOR_GREEN | Green  | (0, 255, 0) |
| COLOR_CYAN | Cyan  | (0, 255, 255) |
| COLOR_BLUE | Blue  | (0, 0, 255)| 
| COLOR_PURPLE | Purple  | (128, 0, 128)| 
| COLOR_PINK | Pink  | (255, 192, 203)| 
| COLOR_GRAY | Gray  | (128, 128, 128)| 
| COLOR_BLACK | Black  | (0, 0, 0)| 
| COLOR_BROWN | Brown  | (165, 42, 42)| 
| COLOR_OLIVE | Olive  | (128, 128, 0)| 
| COLOR_TEAL | Teal  | (0, 128, 128)| 
| COLOR_INDIGO | Indigo  | (75, 0, 130)| 
| COLOR_MAGENTA | Magenta  | (255, 0, 255)| 

## 1. KNOCK(0x00)
Shake hands with HUSKYLENS V2 and tell it whether you're a large-memory MCU or a small-memory MCU.
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x00  | 1 byte | 14 |14 bytes |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

**Data**
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1  | boardType<br/>(0 small ram) <br/>(1 large ram) |
| 1 | 13 | RFU  |

## 2. GET_RESULT(0x01)
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x01  | 1 byte | 0 |1 byte |

Return: RETURN_INFO RETURN_BLOCK... RETURN_ARROW...

## 3. GET_ALGO_PARAM(0x02)
Get algorithm parameters
Assume the key length is n

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data |Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x02  | 1 byte | 14+n+1 | 14+n+1 bytes |1 byte|

Data
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
Switch Algorithm
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0A | 1 byte | 14 |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | algoID(Target algorithm ID) |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 4 | 2 | 0 |
| 6 | 2 | 0 |
| 8 | 2 | 0 |
| 10 | 4 | 0 |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 9. SET_NAME_BY_ID(0x0B)
Set the name based on the learned ID (ID > 0). (Assuming the set name length is n, where 0 < n ≤ 32) Supports Chinese characters. For Chinese characters, please use UTF-8 encoding.

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0B | 1 byte | 14+1+n |14+1+n bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | ID（Learnt ID） |
| 1 | 1 | RFU0 |
| 2 | 2 | RFU1 |
| 4 | 2 | RFU2 |
| 6 | 2 | RFU3 |
| 8 | 2 | RFU4 |
| 10 | 4 | RFU5 |
| 14 | 1 | name length |
| 15 | n | name |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 10. SET_MULTI_ALGORITHM(0x0C)
Create a combination algorithm. Only one combination algorithm may be created. Each combination algorithm supports up to three sub-algorithms.

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0C | 0 | 14 |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | multiAlgoNum (Number of multi-algorithms) |
| 1 | 1 | RFU0 |
| 2 | 2 | AlgoID0 |
| 4 | 2 | AlgoID1 |
| 6 | 2 | AlgoID2 |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 11. SET_MULTI_ALGORITHM_RATIO(0x0D)
Set the ratio of algorithm operations in the combination. The number of ratios must match the number of algorithms.
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0D | 0 | 14 |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | multiAlgoNum (Number of multi-algorithms) |
| 1 | 1 | RFU0 |
| 2 | 2 | AlgoID0Ratio |
| 4 | 2 | AlgoID1Ratio |
| 6 | 2 | AlgoID2Ratio |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 12. SET_ALGO_PARAMS(0x0E)
Set algorithm parameters
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x0E | 1 byte | 14+n+m+2 |14+n+m+2 bytes |1 byte |

Data
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

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 12. COMMAND_UPDATE_ALGORITHM_PARAMS(0x0F)

Set algorithm parameters

| Head55 | HeadAA | CMD  | Algo ID | Data Length | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: |
|  0x55  |  0xAA  | 0x0F | 1 byte  |      0      |  1 byte  |

Return command: RETURN_ARGS retValue=0 indicates successful execution, other values indicate execution failure

## 13. RETURN_ARGS(0x1A)

Return parameters: up to 4 numeric parameters and 2 string parameters
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data |Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1A | 1 byte | 14 + 2 + n + m |14 + 2 + n + m bytes|1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | totalIntArgs (Number of int parameters returned) |
| 1 | 1 | Execution result: 0 indicates success, 1 indicates failure. |
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

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 |  maxID(Maximum number learned)| 
| 1 | 1 | RFU0 |
| 2 | 2 | total_results(Total number of identifications) |
| 4 | 2 | total_results_learned(Total number studied) |
| 6 | 2 | total_blocks (Total number of blocks)|
| 8 | 2 | total_blocks_learned (Total number of blocks studied)|
| 10 | 4 | RFU1 |


## 15. RETURN_BLOCKS（0x1C）
Assume the block's name has length n and its content has length m.
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1C | 1 byte | 14+2+n+m+private_data_length |14+2+n+m bytes+private_data_length bytes |1 byte |

Data
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
|  |  | Algorithm Private Data |

## 16. RETURN_ARROWS(0x1D)
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x1D | 1 byte | 14 |14 bytes |1 byte |

Data
The returned data is a vector. The starting point of the Level 1 vector is the midpoint of the screen's bottom edge (320, 480). The vertical line corresponds to an angle of 0 degrees. Rotating clockwise increases the angle up to 90 degrees, while rotating counterclockwise decreases it down to -90 degrees. The starting point of the Level 2 vector is the endpoint of the Level 1 vector. This design supports operations that add vectors of different levels.

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
Take a photo
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x20  | 0 | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.
arg0_str is the photo filename.

## 18. ACTION_TAKE_SCREENSHOT(0x21)
Screenshot
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x21 | 0 | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.
arg0_str is the screenshot filename.

## 19. ACTION_LEARN(0x22)
Learning successful, return ID non-zero; learning failed, return ID 0.
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x22 | 0 | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.
arg0_int is the learned ID. 0 indicates not learned, while >=1 indicates the learned ID.

## 20. ACTION_FORGET(0x23)
Forget everything
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x23 | 0 | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 21. ACTION_SAVE_KNOWLEDGES(0x24)
Save current configuration to the knowledge base
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x24  | 1 byte | 14 |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | knowLedges_id range[0, 4] |
| 1 | 13 | RFU |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 22. ACTION_LOAD_KNOWLEDGES(0x25)
Load Knowledge Base
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x25  | 1 byte | 14  |14 bytes |1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | knowLedges_id range[0, 4] |
| 1 | 13 | RFU |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 23. ACTION_DRAW_RECT(0x26)
Draw a rectangle
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

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 24. ACTION_CLEAN_RECT(0x27)
Clear all rectangles drawn via the communication protocol
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x27  | 1 byte | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 25. ACTION_DRAW_TEXT(0x28)
Draw text at the specified coordinates.
fontSize only supports [20, 24, 26, 27, 28, 32, 36, 40, 48]

| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Data | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: | :--: |
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

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 26. ACTION_CLEAN_TEXT(0x29)
Clear all text drawn via the communication protocol
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x29  | 1 byte | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 27. ACTION_PLAY_MUSIC(0x2A)
Play music
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

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 28. ACTION_EXIT(0x2B)
Exit the current application. If you are currently on the main menu, you will not exit.
| Head55 | HeadAA  | CMD  | Algo ID | Data Length | Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |
| 0x55 | 0xAA  | 0x2B | 1 byte | 0  |1 byte |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 29. ACTION_LEARN_BLOCK(0x2C)
Set the position and size of the learning box [Currently only available for object tracking]
| Head55 | HeadAA  | CMD  | Algo ID | Data Length |Data| Checksum |
| :--: | :----: | :--: | :--: | :--: | :--: |:--: |
| 0x55 | 0xAA  | 0x2C | 1 byte | 14 |14 bytes|1 byte |

Data
| offset | length  | name  |
| :--: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | RFU1 |
| 2 | 2 | x |
| 4 | 2 | y |
| 6 | 2 | width |
| 8 | 2 | height |
| 10 | 4 | RFU2 |

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.
arg0_int is the learned ID. 0 indicates not learned, while >=1 indicates the learned ID.

## 30. ACTION_DRAW_UNIQUE_RECT(0x2D)
Drawing a single rectangle will clear any previously drawn rectangles on the screen.
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

Return: RETURN_ARGS retValue=0 indicates successful execution. Other values indicate execution failure.

## 31. ACTION_START_RECORDING(0x2E)

Start recording audio or video, file name can be omitted

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

Return command: RETURN_ARGS retValue=0 indicates successful execution, other values indicate execution failure, with attached file name or error information



## 32. ACTION_STOP_RECORDING(0x2F)

Stop recording audio or video

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x2F |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length |                             name                             |
| :----: | :----: | :----------------------------------------------------------: |
|   0    |   1    |                              0                               |
|   1    |   1    | 1:           audio<br/> 2:           video <br/>3:      ( audio+video ) |
|   2    |   12   |                              0                               |

Return command: RETURN_ARGS retValue=0 indicates successful execution, other values indicate execution failure, with attached file name or error information



## 33. GET_AGENT_RESPONSE(0x33)

Get the agent's response. A long response is returned in fragments: the host sends this command repeatedly and the device advances through the fragments in order. Each response carries fragmentCount and fragmentIndex, which the host uses to detect duplicated or missing fragments. The full response is obtained by concatenating all fragmentCount fragments.

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x33 |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType (0: xiaozhi agent) |
| 2 | 12 | RFU |

Return command: RETURN_ARGS

Response Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU |
| 1 | 1 | retValue: 0 indicates success, other values indicate failure (e.g. response not ready) |
| 2 | 2 | fragmentCount (total number of fragments) |
| 4 | 2 | fragmentIndex (current fragment index, starting from 0) |
| 6 | 2 | RFU0 |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |
| 14 | 1 | response fragment length |
| 15 | n | response fragment content (UTF-8) |

## 34. SEND_AGENT_PROMPT(0x34)

Send a prompt to the agent. The prompt is sent as a UTF-8 byte stream in fragments. Data Length is a single byte and the whole Data field must not exceed 255 bytes, so each fragment carries at most 244 bytes of content (the reference implementation uses 238 bytes). fragmentIndex starts from 0, and the device starts processing once all fragmentCount fragments have been received.

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x34 |    0    |   14+1+n   | 14+1+n bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType (0: xiaozhi agent) |
| 2 | 2 | fragmentCount (total number of fragments) |
| 4 | 2 | fragmentIndex (current fragment index, starting from 0) |
| 6 | 2 | RFU0 |
| 8 | 2 | RFU1 |
| 10 | 4 | RFU2 |
| 14 | 1 | prompt fragment length |
| 15 | n | prompt fragment content (UTF-8) |

Return command: RETURN_ARGS retValue=0 indicates the fragment was received successfully, other values indicate failure

## 35. GET_AGENT_STATUS(0x35)

Query the current status of the agent.

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x35 |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType (0: xiaozhi agent) |
| 2 | 12 | RFU |

Return command: RETURN_ARGS

Response Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU |
| 1 | 1 | retValue: 0 indicates the query succeeded, other values indicate failure |
| 2 | 2 | RFU |
| 4 | 2 | status code: 0=idle<br/>1=processing<br/>2=broadcasting<br/>3=disabled (xiaozhi switch is off)<br/> |
| 6 | 8 | RFU |

Note: older firmware may not include the status code field in the response; the host should treat this case as idle.

## 36. IS_AGENT_RESPONSE_READY(0x36)

Query whether the agent's response is ready.

| Head55 | HeadAA | CMD  | Algo ID | Data Length |   Data   | Checksum |
| :----: | :----: | :--: | :-----: | :---------: | :------: | :------: |
|  0x55  |  0xAA  | 0x36 |    0    |     14      | 14 bytes |  1 byte  |

Data

| offset | length | name |
| :----: | :----: | :--: |
| 0 | 1 | RFU0 |
| 1 | 1 | agentType (0: xiaozhi agent) |
| 2 | 12 | RFU |

Return command: RETURN_ARGS retValue=0 indicates the response is ready and can be fetched with GET_AGENT_RESPONSE; other values indicate it is not ready yet

# Private data

## FACE_RECOGNITION Private Data
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

## HAND_RECOGNITION Private Data
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

## POSE_RECOGNITION Private Data
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
