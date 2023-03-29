#ifndef SRC_STOPWATCH_HPP
#define SRC_STOPWATCH_HPP

#include <sys/time.h>

#include "src/defines.hpp"

class Stopwatch {
 public:
  Stopwatch(uint64 ms) { Start(ms); }

  INLINE void Start(uint64 ms) {
    time_ = Now();
    timeout_ = time_ + ms * 1000;
  }

  INLINE uint64 Now() const {
    timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1'000'000 + tv.tv_usec;
  }

  INLINE bool Timeout() const { return Now() >= timeout_; }

  INLINE uint64 ElapsedMs() const { return (Now() - time_) / 1000; }

  INLINE double ElapsedFraction() const { return (double)(Now() - time_) / (timeout_ - time_); }

 private:
  uint64 time_;
  uint64 timeout_;
};

#endif
