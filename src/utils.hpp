#ifndef SRC_UTILS_HPP
#define SRC_UTILS_HPP

#include <cassert>
#include <concepts>
#include <iostream>
#include <sstream>

namespace {

template <typename _T>
inline void Debug(const char *s, _T x) {
  std::cerr << s << " = " << x << '\n';
}

template <typename _T, typename... args>
void Debug(const char *s, _T x, args... a) {
  while (*s != ',') std::cerr << *s++;
  s++;
  while (*s == ' ') s++;

  std::cerr << " = " << x << ", ";

  Debug(s, a...);
}

template <typename T, typename... Args>
void StrCat(std::stringstream &ss, const T &val, const Args &...vals) {
  ss << val;
  if constexpr (sizeof...(vals) > 0) {
    StrCat(ss, vals...);
  }
}

}  // namespace

#ifndef NDEBUG

#define ASSERT(condition, msg)                                       \
  if (not(condition)) {                                              \
    std::cerr << __FILE__ << ":" << __LINE__ << ": " << msg << "\n"; \
    assert(condition);                                               \
  }

#define DEBUG(...) ::Debug(#__VA_ARGS__, __VA_ARGS__)

#else

#define ASSERT(...)
#define DEBUG(...)

#endif

template <typename... Args>
std::string StrCat(const Args &...vals) {
  std::stringstream ss;
  if constexpr (sizeof...(vals) > 0) {
    StrCat(ss, vals...);
  }
  return ss.str();
}

template <class T>
// requires std::forward_iterator<T>
std::string StrJoin(T begin, T end, std::string_view separator) {
  if (begin == end) {
    return "";
  }
  std::stringstream ss;
  ss << *begin;
  for (T it = begin; ++it != end;) {
    ss << separator;
    ss << *it;
  }
  return ss.str();
}

#endif