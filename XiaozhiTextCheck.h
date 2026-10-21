// 小智(Xiaozhi)语音平台 listen/detect 文本长度校验器 —— C++17 移植版
//
// 与 Python 参考实现(v5 终极版)行为一一对应。
// 设计原则: 宁可误拒, 绝不误放 —— 所有取整均为向上取整(保守方向)。
//
// 注意: 平台另有与长度无关的内容过滤(纯数字长串、周期重复串、纯空格、
// 个别语义内容), 任何长度函数都无法覆盖, 不在本模块范围内。
//
// 仅依赖 C++ 标准库, 手写 UTF-8 解码, 禁止按字节统计。
//
// 【嵌入式链接说明】部分 Arduino core(如 micro:bit 的 sandeepmistry nRF5)
// 用 gcc 驱动链接且不带 -lstdc++, 因此 Arduino 构建下本模块只暴露不依赖
// std::string 的纯整数 API(measure(const char *, size_t) / can_send)。
// 带 std::string 的完整 API(check_text / 诊断原因串)仅宿主机可用。
// 若目标平台确认链接 -lstdc++(如 ESP32), 可放宽下方 ARDUINO 守卫。

#ifndef XIAOZHI_TEXT_CHECK_H
#define XIAOZHI_TEXT_CHECK_H

// Arduino 构建时经 Result.h 取得 LARGE_MEMORY(ESP32/NRF5/ESP8266/NRF52833)。
// AVR 等小内存无 libstdc++, 本模块整体不参与编译; 宿主机(g++/测试)无
// ARDUINO 宏, 始终参与编译。
#if defined(ARDUINO)
#include <Result.h>
#endif

#if !defined(ARDUINO) || defined(LARGE_MEMORY)

#include <cstddef>
#include <cstdint>
#if !defined(ARDUINO)
#include <string>
#endif

namespace xiaozhi {

enum class CharClass { Hanzi, Heavy, Letter, Digit, Period, Punct };

struct MeasureResult {
  int zh_eff;    // 汉字类等效数(向上取整后)
  int en_eff;    // ASCII 等效数(向上取整后)
  int hanzi;     // 汉字类原始个数(汉字/假名/中文标点)
  int heavy;     // 重型非ASCII个数(emoji/全角/韩文/俄文等)
  int letter;    // ASCII 字母+空格
  int digit;     // ASCII 数字
  int period;    // ASCII 句号 '.'
  int punct;     // 其他 ASCII 标点
  int cjk_punct; // 其中中文标点的个数
};

// 统计文本各类字符数并计算 zh_eff / en_eff
MeasureResult measure(const char *utf8_text, size_t length);

// 判定文本能否发送: true=放行(保证平台接受), false=拒绝。
// 纯整数路径, 不实例化任何 std::string 代码
bool can_send(const char *utf8_text);
bool can_send(const char *utf8_text, size_t length);

#if !defined(ARDUINO)

struct CheckResult {
  bool can_send; // true=放行(保证平台接受), false=拒绝
  MeasureResult m;
  std::string reason; // 判定说明(哪个类别超了)
};

MeasureResult measure(const std::string &utf8_text);

// 判定文本能否发送到小智平台(含诊断原因)
CheckResult check_text(const std::string &utf8_text);

bool can_send(const std::string &utf8_text);

#endif // !defined(ARDUINO)

} // namespace xiaozhi

#endif // !defined(ARDUINO) || defined(LARGE_MEMORY)

#endif // XIAOZHI_TEXT_CHECK_H
