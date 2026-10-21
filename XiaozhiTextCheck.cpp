#include "XiaozhiTextCheck.h"

#if !defined(ARDUINO) || defined(LARGE_MEMORY)

#include <cstring>

namespace xiaozhi {

namespace {

// zh_eff = 0..16 时最多允许的 en_eff (实测标定表)
const int MIXED_BUDGET[17] = {35, 31, 26, 26, 24, 24, 20, 16, 16,
                              14, 14, 10, 8,  7,  4,  3,  0};
const int MAX_CJK = 16;
const int MAX_ASCII = 35;

// 非法 UTF-8 字节的兜底码点标记(不可能与合法码点冲突)
const uint32_t kInvalidCp = 0xFFFFFFFFu;

bool is_continuation(unsigned char c) { return (c & 0xC0) == 0x80; }

// 中文标点集合: ，。！？；：、“”‘’（）《》〈〉【】「」『』—…·
bool is_cjk_punct(uint32_t cp) {
  switch (cp) {
  case 0x3001: // 、
  case 0x3002: // 。
  case 0x3008: // 〈
  case 0x3009: // 〉
  case 0x300A: // 《
  case 0x300B: // 》
  case 0x300C: // 「
  case 0x300D: // 」
  case 0x300E: // 『
  case 0x300F: // 』
  case 0x3010: // 【
  case 0x3011: // 】
  case 0x2014: // —
  case 0x2018: // ‘
  case 0x2019: // ’
  case 0x201C: // “
  case 0x201D: // ”
  case 0x2026: // …
  case 0x00B7: // ·
  case 0xFF01: // ！
  case 0xFF08: // （
  case 0xFF09: // ）
  case 0xFF0C: // ，
  case 0xFF1A: // ：
  case 0xFF1B: // ；
  case 0xFF1F: // ？
    return true;
  default:
    return false;
  }
}

// 解码 data[i] 处的一个 UTF-8 序列。
// 合法: 返回码点并把 i 前移整个序列; 非法(截断/坏续字节/过长编码/代理区/
// 超出 U+10FFFF): 返回 kInvalidCp 且 i 仅前移 1 字节 —— 该字节按"重型
// 非ASCII"兜底(保守方向)。
uint32_t decode_one(const char *data, size_t n, size_t &i) {
  const unsigned char c0 = static_cast<unsigned char>(data[i]);
  if (c0 < 0x80) { // 1 字节 0xxxxxxx
    ++i;
    return c0;
  }
  if ((c0 & 0xE0) == 0xC0 && i + 1 < n &&
      is_continuation(static_cast<unsigned char>(data[i + 1]))) {
    uint32_t cp = (static_cast<uint32_t>(c0 & 0x1F) << 6) |
                  (static_cast<unsigned char>(data[i + 1]) & 0x3F);
    if (cp >= 0x80) { // 拒绝过长编码
      i += 2;
      return cp;
    }
  } else if ((c0 & 0xF0) == 0xE0 && i + 2 < n &&
             is_continuation(static_cast<unsigned char>(data[i + 1])) &&
             is_continuation(static_cast<unsigned char>(data[i + 2]))) {
    uint32_t cp = (static_cast<uint32_t>(c0 & 0x0F) << 12) |
                  ((static_cast<uint32_t>(static_cast<unsigned char>(data[i + 1])) & 0x3F) << 6) |
                  (static_cast<unsigned char>(data[i + 2]) & 0x3F);
    if (cp >= 0x800 && !(cp >= 0xD800 && cp <= 0xDFFF)) { // 拒绝过长/代理区
      i += 3;
      return cp;
    }
  } else if ((c0 & 0xF8) == 0xF0 && i + 3 < n &&
             is_continuation(static_cast<unsigned char>(data[i + 1])) &&
             is_continuation(static_cast<unsigned char>(data[i + 2])) &&
             is_continuation(static_cast<unsigned char>(data[i + 3]))) {
    uint32_t cp = (static_cast<uint32_t>(c0 & 0x07) << 18) |
                  ((static_cast<uint32_t>(static_cast<unsigned char>(data[i + 1])) & 0x3F) << 12) |
                  ((static_cast<uint32_t>(static_cast<unsigned char>(data[i + 2])) & 0x3F) << 6) |
                  (static_cast<unsigned char>(data[i + 3]) & 0x3F);
    if (cp >= 0x10000 && cp <= 0x10FFFF) { // 拒绝过长/超范围
      i += 4;
      return cp;
    }
  }
  ++i; // 非法序列: 仅跳过当前字节, 按重型非ASCII计
  return kInvalidCp;
}

// 与 Python _classify() 一一对应
CharClass classify(uint32_t cp) {
  if (cp < 0x80) {
    if (cp >= '0' && cp <= '9')
      return CharClass::Digit;
    if ((cp >= 'A' && cp <= 'Z') || (cp >= 'a' && cp <= 'z') || cp == ' ')
      return CharClass::Letter;
    if (cp == '.')
      return CharClass::Period;
    return CharClass::Punct; // 其余 ASCII(含控制字符/0x7F)
  }
  if ((cp >= 0x4E00 && cp <= 0x9FFF) || // CJK 统一表意文字
      (cp >= 0x3400 && cp <= 0x4DBF) || // CJK 扩展A
      (cp >= 0x3040 && cp <= 0x30FF) || // 日文假名
      is_cjk_punct(cp)) {               // 中文标点
    return CharClass::Hanzi;
  }
  return CharClass::Heavy; // emoji/全角/韩文/俄文/拉丁扩展/符号等
}

// 判定规则的唯一实现: 纯整数运算, 不触碰 std::string。
// 部分嵌入式工具链(如 micro:bit 的 sandeepmistry nRF5 core)用 gcc 驱动
// 链接且不带 -lstdc++, Arduino 构建下本文件不编译任何 std::string 代码,
// 从结构上保证链接不受 gc-sections 有效性影响。
bool rules_pass(const MeasureResult &m) {
  if (m.zh_eff > MAX_CJK)
    return false;
  if (m.cjk_punct >= 3 && m.hanzi >= 14)
    return false;
  if (m.cjk_punct >= 2 && m.hanzi >= 15)
    return false;
  if (m.en_eff == 0)
    return true;
  if (m.zh_eff == 0)
    return m.en_eff <= MAX_ASCII;
  int budget = MIXED_BUDGET[m.zh_eff];
  if (m.heavy > 0)
    budget -= 1; // 重型非ASCII混用, 预算保守减1
  return m.en_eff <= budget;
}

#if !defined(ARDUINO)

std::string detail_str(const MeasureResult &m) {
  return "zh=" + std::to_string(m.zh_eff) + "(汉字" + std::to_string(m.hanzi) +
         "+重型" + std::to_string(m.heavy) + ") en=" + std::to_string(m.en_eff) +
         "(字母" + std::to_string(m.letter) + "+数字" + std::to_string(m.digit) +
         "+句号" + std::to_string(m.period) + "+标点" + std::to_string(m.punct) +
         ")";
}

// 与 rules_pass 同序遍历, 仅用于生成诊断文案(结论一律以 rules_pass 为准)
std::string explain(const MeasureResult &m) {
  if (m.zh_eff > MAX_CJK)
    return "zh 超过 " + std::to_string(MAX_CJK) + ", 确定被拒";
  if (m.cjk_punct >= 3 && m.hanzi >= 14)
    return "中文标点>=3且汉字类>=14, 保守拒绝";
  if (m.cjk_punct >= 2 && m.hanzi >= 15)
    return "中文标点>=2且汉字类>=15, 保守拒绝";
  if (m.en_eff == 0)
    return "纯非ASCII <= " + std::to_string(MAX_CJK);
  if (m.zh_eff == 0) {
    if (m.en_eff <= MAX_ASCII)
      return "纯ASCII <= " + std::to_string(MAX_ASCII);
    return "纯ASCII 超过 " + std::to_string(MAX_ASCII) + ", 确定被拒";
  }
  int budget = MIXED_BUDGET[m.zh_eff];
  if (m.heavy > 0)
    budget -= 1;
  if (m.en_eff <= budget)
    return "混合预算 zh=" + std::to_string(m.zh_eff) +
           " -> en<=" + std::to_string(budget);
  return "超出混合预算 zh=" + std::to_string(m.zh_eff) +
         " -> en<=" + std::to_string(budget) + ", 确定被拒";
}

CheckResult verdict(const MeasureResult &m, bool ok, const std::string &why) {
  CheckResult r;
  r.can_send = ok;
  r.m = m;
  r.reason = detail_str(m) + ", " + why;
  return r;
}

#endif // !defined(ARDUINO)

} // namespace

MeasureResult measure(const char *utf8_text, size_t length) {
  MeasureResult r = {};
  size_t i = 0;
  while (i < length) {
    uint32_t cp = decode_one(utf8_text, length, i);
    CharClass cls = (cp == kInvalidCp) ? CharClass::Heavy : classify(cp);
    switch (cls) {
    case CharClass::Hanzi:
      ++r.hanzi;
      if (is_cjk_punct(cp))
        ++r.cjk_punct;
      break;
    case CharClass::Heavy:
      ++r.heavy;
      break;
    case CharClass::Letter:
      ++r.letter;
      break;
    case CharClass::Digit:
      ++r.digit;
      break;
    case CharClass::Period:
      ++r.period;
      break;
    case CharClass::Punct:
      ++r.punct;
      break;
    }
  }
  // 向上取整, 纯整数运算(保守方向):
  // ceil(hanzi + 1.5*heavy) = (2*hanzi + 3*heavy + 1) / 2
  r.zh_eff = (2 * r.hanzi + 3 * r.heavy + 1) / 2;
  // ceil(digit * 1.125) = (digit*9 + 7) / 8
  r.en_eff = r.letter + (r.digit * 9 + 7) / 8 + 3 * r.period + 5 * r.punct;
  return r;
}

#if !defined(ARDUINO)

MeasureResult measure(const std::string &utf8_text) {
  return measure(utf8_text.data(), utf8_text.size());
}

CheckResult check_text(const std::string &utf8_text) {
  MeasureResult m = measure(utf8_text);
  return verdict(m, rules_pass(m), explain(m));
}

#endif // !defined(ARDUINO)

bool can_send(const char *utf8_text, size_t length) {
  if (utf8_text == NULL)
    return false;
  return rules_pass(measure(utf8_text, length));
}

bool can_send(const char *utf8_text) {
  if (utf8_text == NULL)
    return false;
  return can_send(utf8_text, strlen(utf8_text));
}

#if !defined(ARDUINO)

bool can_send(const std::string &utf8_text) {
  return check_text(utf8_text).can_send;
}

#endif // !defined(ARDUINO)

} // namespace xiaozhi

#endif // !defined(ARDUINO) || defined(LARGE_MEMORY)
