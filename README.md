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

## Merging

    python code_merger.py src/main.cpp
