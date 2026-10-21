// 40 条测试用例 —— 期望值来自任务规格(保守校验器输出)。
// 约定:
//   "汉字N" = N 个汉字
//   "EN N"  = "the quick brown fox jumps over the lazy dog and runs far away" 前 N 字符
//   "RD N"  = "41421356237309504880168872420969807856967187537694" 前 N 字符

#include "../../XiaozhiTextCheck.h"

#include <cstring>
#include <iostream>
#include <string>
#include <vector>

using xiaozhi::check_text;

namespace {

const std::string EN_BASE =
    "the quick brown fox jumps over the lazy dog and runs far away";
const std::string RD_BASE =
    "41421356237309504880168872420969807856967187537694";

std::string rep(const char *unit, int n) {
  std::string s;
  s.reserve(std::strlen(unit) * static_cast<size_t>(n));
  for (int i = 0; i < n; ++i)
    s += unit;
  return s;
}

std::string hz(int n) { return rep(u8"汉", n); }         // 汉字
std::string en(int n) { return EN_BASE.substr(0, static_cast<size_t>(n)); }
std::string rd(int n) { return RD_BASE.substr(0, static_cast<size_t>(n)); }
std::string emoji(int n) { return rep(u8"\U0001F600", n); } // 😀
std::string kana(int n) { return rep(u8"あ", n); }          // 日文假名
std::string hangul(int n) { return rep(u8"한", n); }        // 韩文

struct Case {
  int no;
  std::string name;
  std::string input;
  bool expect; // true=通过(放行), false=拒绝
};

} // namespace

int main() {
  const std::vector<Case> cases = {
      {1, "汉字x16", hz(16), true},
      {2, "汉字x17", hz(17), false},
      {3, "EN x35", en(35), true},
      {4, "EN x36", en(36), false},
      {5, "汉字x1 + EN x31", hz(1) + en(31), true},
      {6, "汉字x1 + EN x32", hz(1) + en(32), false},
      {7, "汉字x5 + EN x24", hz(5) + en(24), true},
      {8, "汉字x5 + EN x25", hz(5) + en(25), false},
      {9, "汉字x8 + EN x16", hz(8) + en(16), true},
      {10, "汉字x8 + EN x17", hz(8) + en(17), false},
      {11, "汉字x10 + EN x14", hz(10) + en(14), true},
      {12, "汉字x12 + EN x9", hz(12) + en(9), false},
      {13, "汉字x13 + EN x7", hz(13) + en(7), true},
      {14, "汉字x15 + EN x3", hz(15) + en(3), true},
      {15, "汉字x16 + EN x1", hz(16) + en(1), false},
      {16, u8"我的电话是13812345678", u8"我的电话是13812345678", true},
      {17, u8"订单AB1234昨天发的货还没到", u8"订单AB1234昨天发的货还没到", true},
      {18, "hello, how are you?", "hello, how are you?", true},
      {19, "hello, how are you doing today!!?",
       "hello, how are you doing today!!?", false},
      {20, "汉字x5 + RD x20", hz(5) + rd(20), true},
      {21, "汉字x5 + RD x22", hz(5) + rd(22), false},
      {22, "汉字x8 + RD x16", hz(8) + rd(16), false},
      {23, "汉字x8 + ....", hz(8) + "....", true},
      {24, "汉字x14 + ,", hz(14) + ",", false},
      {25, "汉字x10 + hello!", hz(10) + "hello!", true},
      {26, "汉字x8 + the, quick brown f", hz(8) + "the, quick brown f", false},
      {27, "emoji x10", emoji(10), true},
      {28, "emoji x11", emoji(11), false},
      {29, "emoji x8 + EN x8 (重型混用预算-1)", emoji(8) + en(8), false},
      {30, "emoji x8 + EN x9", emoji(8) + en(9), false},
      {31, u8"全角１２３４５ + EN x14", u8"１２３４５" + en(14), true},
      {32, "あ x16", kana(16), true},
      {33, "あ x17", kana(17), false},
      {34, "한 x16", hangul(16), false},
      {35, u8"汉字x13 + ，。", hz(13) + u8"，。", false},
      {36, u8"汉字x12 + ，。！", hz(12) + u8"，。！", false},
      {37, u8"汉字x14 + ，。", hz(14) + u8"，。", false},
      {38, u8"汉字x10 + ，。！？", hz(10) + u8"，。！？", false},
      {39, u8"汉字x10 + ，。！？；", hz(10) + u8"，。！？；", false},
      {40, u8"汉字x15 + ，", hz(15) + u8"，", true},
  };

  int passed = 0;
  for (const Case &c : cases) {
    xiaozhi::CheckResult r = check_text(c.input);
    // 三个入口(std::string / C字符串 / C字符串+长度)结论必须一致
    bool ok = (r.can_send == c.expect) &&
              (xiaozhi::can_send(c.input) == c.expect) &&
              (xiaozhi::can_send(c.input.c_str()) == c.expect) &&
              (xiaozhi::can_send(c.input.c_str(), c.input.size()) == c.expect);
    if (ok)
      ++passed;
    std::cout << (ok ? "[PASS] " : "[FAIL] ") << '#' << c.no << ' ' << c.name
              << " | 期望=" << (c.expect ? "通过" : "拒绝")
              << " 实际=" << (r.can_send ? "通过" : "拒绝") << '\n';
    if (!ok)
      std::cout << "       " << r.reason << '\n';
  }

  std::cout << "\n通过 " << passed << '/' << cases.size() << " ("
            << (100.0 * passed / cases.size()) << "%)\n";
  return passed == static_cast<int>(cases.size()) ? 0 : 1;
}
