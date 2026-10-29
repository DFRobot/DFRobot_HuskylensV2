# PacketData_t 从 10 字节扩展到 14 字节的影响分析

## 背景

在 `Result.h` 的 `PacketData_t` 末尾（offset 10 处）新增了：

```c
union {
  int32_t fifth;
  float   confidence;
};
```

结构体由 10 字节变为 14 字节，`payload[0]` 的起始偏移从 10 变为 14。

**改动性质**：这是把结构体对齐到协议文档 V0.2+ 的线格式——文档中**所有**命令的 Data 段固定头都是 14 字节（offset 10 为 4 字节字段，字符串一律从 offset 14 开始），改动方向正确。但结构体只是接收侧的"覆盖层"，库中仍有多处代码假设旧的 10 字节布局，需配套修改。

---

## 一、必须改的 C++ 代码

### 1. `Result.cpp:3-13` — Result 构造函数漏拷贝新字段（真 bug）

构造函数逐个拷贝了 `ID/level/xCenter/yCenter/width/height`，但**没有拷贝新加的 `fifth/confidence`**。`new Result(...)` 不做零初始化，用户读 `result->confidence` 会拿到未初始化的垃圾值。

修改方法：在构造函数中补一行：

```c
fifth = packet->fifth;   // 或 confidence = packet->confidence;
```

`FaceResult` / `HandResult` / `PoseResult` 继承自 `Result`，基类修好后派生类自动获得该字段。

### 2. 发送侧：请求包的 Data 段也要从 10 补到 14

发送是逐字节拼装的（`husky_lens_protocol_write_*`），不受结构体影响，但协议文档中每个命令的请求表也都是 14 字节固定头，目前代码全部按 10 字节填零，需要逐处 +4：

| 位置 | 命令 | 现状 | 改法 |
|---|---|---|---|
| `ProtocolV2.cpp:263` | KNOCK | 1+9=10（文档 §1 明确要 14） | 补零到 13 |
| `:292` | SET_ALGORITHM | 1+9 | 9→13 |
| `:410-420` | SET_MULTI_ALGORITHM | 1+1+8=10，无 padding | 末尾补 4 字节 |
| `:465-474` | SET_MULTI_ALGORITHM_RATIO | 同上 | 末尾补 4 字节 |
| `:500-507` | LEARN_BLOCK | 1+1+8=10，无 padding | 末尾补 4 字节 |
| `:528` | TAKE_PHOTO | 1+9 | 9→13 |
| `:763` | SAVE_KNOWLEDGES | 1+9 | 9→13 |
| `:787` | LOAD_KNOWLEDGES | 1+9 | 9→13 |
| `:814` | PLAY_MUSIC | 补零 6 | 6→10 |
| `:839` | SET_NAME_BY_ID | 1+9 | 9→13 |
| `:863` / `:890` / `:915` | GET_ALGO_PARAM（bool/float/string） | 补零 10 | 10→14 |
| `:967` | SET_ALGO_PARAMS（bool） | 补零 6 | 6→10 |
| `:993-999` | SET_ALGO_PARAMS（float） | 1+1+8=10，无 padding | key 字符串前补 4 字节 |
| `:1025` | SET_ALGO_PARAMS（string） | 补零 10 | 10→14 |
| `:1055` | START_RECORDING | 补零 6 | 6→10 |
| `:1082` | STOP_RECORDING | 补零 8 | 8→12 |
| `:1106` / `:1129` / `:1152` | E2E_START/STOP_RECORDING、E2E_SEND_ANNOTATION | 补零 10 | 10→14 |

> 注：`setAlgoParamFloat` 中 float 仍按两个 int16 写在 offset 2-5，保持不变，只是在 key 字符串前补 4 字节。

### 3. 需要重排字段的发送函数（不只是补零）

**`drawRect`（`ProtocolV2.cpp:616-624`）和 `drawUniqueRect`（`:649-657`）**

现在写 `int16(0)` 占 offset 10-11、`int32(color)` 落在 12-15，共 16 字节。文档（§23/§30）是 **RGBA 在 offset 10、总长 14**。应删掉 `write_int16(0)`，把 color 直接写到 offset 10。

**`drawText`（`:704-716`）**

现在文本紧接 offset 10、color 在包尾。文档（§25）是 **RGBA 在 10、text length 在 14**。应改为：写完 `fontSize/x/y` 和两个 RFU int16 后直接 `write_int32(color)`，再 `write_string(text)`，去掉手写的 length 循环和包尾的 color。

**Agent 相关四处**

- `getAgentStatus:1231`、`isAgentResponseReady:1262`、`getAgentResponse:1293`：补零 8→12（文档 §33/35/36 请求 Data 均为 14 字节）
- `sendAgentPrompt:1201`：补零 4→8（文档 §34 字符串从 offset 14 开始）

---

## 二、不用改的部分（自动适配）

- **帧接收状态机和校验和**（`ProtocolV2.cpp:111-190` 附近）：按长度字节组帧，与布局无关。
- **约 30 处只读 offset 0–9 的解析点**（`retValue`、`first~fourth`、`total_*` 等）：偏移未变。
- **`Result.cpp` 中所有 `packet->payload` 用法**：包括 Face/Hand/PoseResult 的私有数据指针运算，以及 `data_length == pname - packet` 这类动态偏移比较——`payload` 现在落在 14，正好符合文档 §13/§15（之前指在 10 反而与文档不符）。`ProtocolV2.cpp:540/564/927/1311` 的字符串读取同理。
- **`DFRobot_HuskylensV2.h/cpp` 上层 API 和全部 examples**：不接触字节布局。
- **缓冲区尺寸**（`FRAME_BUFFER_SIZE`/`CMD_BUFFER_SIZE`）：多 4 字节后仍在 128/64 限制内（AVR 上 `drawText` 可发文本上限少 4 字节，留意即可）。

---

## 三、Python 镜像需同步（两份文件）

`python/pinpong/dfrobot_huskylensv2.py` 和 `python/smbus2/dfrobot_huskylensv2.py` 结构相同（仅传输层不同），均仍按 10 字节硬编码：

1. **ctypes `PacketData_t`**：缺 offset 10 的 4 字节，需新增：

   ```python
   class UnionInt32_0(ctypes.Union):
       _fields_ = [
           ("fifth", ctypes.c_int32),
           ("confidence", ctypes.c_float),
       ]
   ```

   并在 `PacketData_t._fields_` 追加 `("u6", UnionInt32_0)`、`_anonymous_` 追加 `"u6"`。

   另外 `UnionInt8_1` 中现有的 `confidence = c_int8`（offset 1）是旧协议残留，与 C++ 不一致，顺手清理。

2. **`Result.__init__`**（pinpong 版 218-232 行）：`base + 10` → `base + 14`，共 3 处（`nameLength`、`contentLength`、`str_idx`），外加 `dataLength > 10` 的判断改为 `> 14`。

3. **`getResult`**（`:364`）：`receive_index != CONTENT_INDEX + 10` → `+ 14`（RETURN_INFO 的 Data 现为 14 字节）。

4. **`wait()`**（`:434`）：RETURN_ARGS 字符串区起点 `offset = CONTENT_INDEX + 10` → `+ 14`。

5. **所有 `husky_lens_protocol_write_zero_bytes` 调用**：与 C++ 发送侧同样 +4/重排。

6. **`:947` 的 `Result([0] * 16)`** 空占位：改为 `[0] * 20`（6 字节帧头 + 14 字节 Data）。

---

## 四、注意事项

1. **固件版本匹配**：改完后库只兼容按 14 字节 Data 头收发的新固件。若设备仍是旧固件（10 字节），所有带 name/content 的解析和带字符串的命令会整体错位 4 字节。建议先拿真机验证 RETURN_BLOCK 的 Data Length 是 `14+2+n+m` 再合并。
2. **文档笔误**（可选顺手修）：
   - 英文版 `HuskyLens2_Protocol.md` 的 RETURN_BLOCKS 表多了一个 RFU（name length 误写为 offset 16）；RETURN_ARGS 表 key length 误写为 13。
   - CN 版 §3 GET_ALGO_PARAM 的 key 误写为 offset 13。
   - 以 CN 版 §13/§15 的 14 为准，当前结构体是正确的。
3. **`keywords.txt`**：可选加入 `confidence`，便于 Arduino IDE 高亮。
