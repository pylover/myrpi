
export ARCH=arm
export CROSS_COMPILE=$(readlink -f rpi-tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-)
export INSTALL_MOD_PATH=$(readlink -f output)
