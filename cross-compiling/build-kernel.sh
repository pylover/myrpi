#! /usr/bin/env bash

## Configure the kernel
cd rpi-linux

# For Raspberry Pi Model A(+), B(+), Zero, execute the following commands:
#export KERNEL=kernel
#make bcmrpi_defconfig

# For Raspberry Pi 2/3 Model B, execute these commands:
export KERNEL=kernel7
make bcm2709_defconfig

# An alternative way is to export the configuration from a running Raspberry Pi:
ssh root@ha "modprobe configs && cat /proc/config.gz" | zcat > .config

make menuconfig

## Build the Kernel

make -j8 zImage && \
make -j8 modules && \
make -j8 dtbs && \
make -j8 modules_install


## Transfer Kernel Image, Modules, and Device Tree Overlay to their Places on Raspberry Pi
mkdir -p $INSTALL_MOD_PATH/boot
./scripts/mkknlimg ./arch/arm/boot/zImage $INSTALL_MOD_PATH/boot/$KERNEL.img
cp ./arch/arm/boot/dts/*.dtb $INSTALL_MOD_PATH/boot/
cp -r ./arch/arm/boot/dts/overlays $INSTALL_MOD_PATH/boot
cd $INSTALL_MOD_PATH
IMAGE="linux-image-4.16.10-v7+.tgz"
tar -czf /tmp/$IMAGE *

echo "Copy the image: /tmp/$IMAGE into the rpi"

