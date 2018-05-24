#! /usr/bin/env bash

echo "Clone the rpi kernel"
if [ ! -d rpi-linux ]; then
  git clone git@github.com:raspberrypi/linux.git rpi-linux
  git -C rpi-linux checkout rpi-4.16.y
fi


echo "Install and Configure the cross compile tool-chain"

if [ ! -d rpi-tools ]; then
  git clone https://github.com/raspberrypi/tools.git rpi-tools
fi


mkdir -p output
