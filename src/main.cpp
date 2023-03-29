#include <iostream>

#include "src/folder_example/foo.hpp"
#include "src/stopwatch.hpp"
#include "src/utils.hpp"

int main() {
  // Good luck with new project :D

  Stopwatch watch(50);

  DEBUG(watch.Now());

  Foo();

  return 0;
}