#ifndef SRC_DEFINES_HPP
#define SRC_DEFINES_HPP

// Uncomment when everything is tested!
// #define NDEBUG

#undef _GLIBCXX_DEBUG  // disable run-time bound checking, etc
#pragma GCC optimize("Ofast,unroll-loops")

// PASTE ALL INCLUDES!

#pragma GCC target("avx2")

#define INLINE inline __attribute__((always_inline))
#define NOINLINE __attribute__((noinline))

using int8 = signed char;
using int16 = signed short;
using int32 = signed int;
using int64 = signed long long;
using uint8 = unsigned char;
using uint16 = unsigned short;
using uint32 = unsigned int;
using uint64 = unsigned long long;

#endif