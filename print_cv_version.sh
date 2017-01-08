#!/bin/bash
set -x
set -e
g++ `pkg-config --cflags opencv` \
  -lopencv_core \
  -lopencv_highgui \
  -lopencv_imgproc \
  -o version.out \
  version_cv.cpp \
  `pkg-config --libs opencv` &&
  ./version.out
