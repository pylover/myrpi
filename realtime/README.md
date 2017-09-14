# Cross compiling the realtime kernel for the rpi3

(draft)

## Clone the rpi kernel

```shell
git clone git@github.com:raspberrypi/linux.git
cd linux
git checkout rpi-4.9.y
```

## Download & apply the rt patch

```shell
user@host ~/linux$ curl https://www.kernel.org/pub/linux/kernel/projects/rt/4.9/patch-4.9.47-rt37.patch.gz | zcat | patch -p1
```

### Install and Configure the cross compile tool-chain

```shell
cd ..
user@host ~$ git clone https://github.com/raspberrypi/tools.git
user@host ~$ export ARCH=arm
user@host ~$ export CROSS_COMPILE=$(readlink -f tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf-)

# Later, when you install the modules, they will go into the directory specified by INSTALL_MOD_PATH
user@host ~$ export INSTALL_MOD_PATH=$(readlink -f rtkernel)
```

## Configure the kernel

Next, we need to configure the kernel for using RT Preempt.

For Raspberry Pi Model A(+), B(+), Zero, execute the following commands:

```shell
cd linux
user@host ~/linux$ export KERNEL=kernel
user@host ~/linux$ make bcmrpi_defconfig
```

For Raspberry Pi 2/3 Model B, execute these commands:

```shell
user@host ~/linux$ export KERNEL=kernel7
user@host ~/linux$ make bcm2709_defconfig
```

An alternative way is to export the configuration from a running Raspberry Pi:

```shell
user@host ~/linux$ ssh root@raspberry "modprobe configs"
user@host ~/linux$ scp root@raspberry:/proc/config.gz ./
user@host ~/linux$ zcat config.gz > .config
```
Or: (nerds way!)

```shell
ssh root@rasppberry "cat /proc/config.gz" | zcat config.gz > .config
```

