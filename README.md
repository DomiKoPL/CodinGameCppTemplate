# CodinGameCppTemplate

## Rules

Every include path must start from src!

For example:

    #include "src/utils.hpp"


    #include "src/folder_example/foo.hpp"

## Building

I hate CMake, so I use Google Bazel.
It is relatively simple to learn and use.

In order to run main file, simply use:

    bazel run src/main


### Configs

There are 4 different configs in file [bazelrc](.bazelrc).

Simply use:

    bazel run --config=name src/main

It is a very nice feature, because you can switch between optimized version and debug version (--config=opt, --config=asan).


## Merging

    python code_merger.py src/main.cpp
