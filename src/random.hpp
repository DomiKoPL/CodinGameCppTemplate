#ifndef SRC_RANDOM_HPP
#define SRC_RANDOM_HPP

#include "src/defines.hpp"

class Random {
 public:
  Random(int seed) : seed_(seed) {}

  inline bool NextBool() { return (XRandom() & 4) == 4; }

  // return random int in range [0, range)
  inline uint32 NextInt(uint32 range) { return XRandom() % range; }

  // return random int in range [a, b]
  inline int32 NextInt(int32 a, int32 b) { return (int32)NextInt((uint32)(b - a + 1)) + a; }

  // return random float in range [0, 1]
  inline float NextFloat() {
    uint32 xr = XRandom();
    if (xr == 0U) return 0.0f;
    union {
      float f;
      uint32 i;
    } pun = {(float)xr};
    pun.i -= 0x10000000U;

    return pun.f;
  }

  // return random float in range [a, b]
  inline float NextFloat(float a, float b) { return NextFloat() * (b - a) + a; }

 private:
  inline uint32 XRandom() {
    seed_ = seed_ * kM + kA;
    return (uint32)(seed_ >> (29 - (seed_ >> 61)));
  }

  uint64 seed_;
  static constexpr uint64 kM = 0x9b60933458e17d7d;
  static constexpr uint64 kA = 0xd737232eeccdf7ed;
};

template <class T>
void RandomShuffle(T begin, T end, Random& rnd) {
  const auto size = end - begin;
  if (size == 0) {
    return;
  }
  for (auto i = size - 1; i > 0; --i) {
    std::swap(*(begin + i), *(begin + rnd.NextInt(i + 1)));
  }
}

#endif
