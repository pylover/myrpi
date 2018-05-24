
# Cross compiling for rpi3 stretch


## Clone the rpi kernel

```shell
git clone git@github.com:raspberrypi/linux.git rpi-linux
cd rpi-linux
git checkout rpi-4.16.y
```

## Install and Configure the cross compile tool-chain

```shell
cd ..
git clone https://github.com/raspberrypi/tools.git rpi-tools
export ARCH=arm
export CROSS_COMPILE=$(readlink -f rpi-tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-)

# Later, when you install the modules, they will go into the directory specified by INSTALL_MOD_PATH
export INSTALL_MOD_PATH=$(readlink -f rpi-kernel)
```

## Configure the kernel

Next, we need to configure the kernel.

For Raspberry Pi Model A(+), B(+), Zero, execute the following commands:

```shell
cd rpi-linux
export KERNEL=kernel
make bcmrpi_defconfig
```

For Raspberry Pi 2/3 Model B, execute these commands:

```shell
cd linux
export KERNEL=kernel7
make bcm2709_defconfig
```

An alternative way is to export the configuration from a running Raspberry Pi:

```shell
ssh root@ha "modprobe configs"
scp root@ha:/proc/config.gz ./
zcat config.gz > .config
```
Or: (nerds way!)

```shell
ssh root@ha "modprobe configs && cat /proc/config.gz" | zcat > .config
```

Then, you can start to configure the kernel:

```shell
make menuconfig
```

## Build the Kernel

```shell
make -j4 zImage
make -j4 modules
#############################################################################################
make -j4 dtbs
make -j4 modules_install
```

The last command installs the kernel modules in the directory specified by INSTALL_MOD_PATH above.

## Transfer Kernel Image, Modules, and Device Tree Overlay to their Places on Raspberry Pi

```shell
mkdir -p $INSTALL_MOD_PATH/boot
./scripts/mkknlimg ./arch/arm/boot/zImage $INSTALL_MOD_PATH/boot/$KERNEL.img
cp ./arch/arm/boot/dts/*.dtb $INSTALL_MOD_PATH/boot/
cp -r ./arch/arm/boot/dts/overlays $INSTALL_MOD_PATH/boot
cd $INSTALL_MOD_PATH
tar -czf /tmp/linux-image-4.9.50-rt37-v7+.tgz *
```

Copy the image into the rpi using ssh

```shell
user@host ~/linux$ scp /tmp/linux-image-4.9.50-rt37-v7+.tgz pi@raspberry:/tmp
```

Then on the Pi, install the real-time kernel (this will overwrite the old kernel image!):

```shell
pi@raspberry ~$ cd /tmp
pi@raspberry ~$ tar -xzf linux-image-4.9.50-rt37-v7+.tgz
pi@raspberry ~$ sudo rm -r /lib/firmware/
pi@raspberry ~$ sudo rm -r /boot/overlays/
pi@raspberry ~$ cd boot
pi@raspberry ~$ sudo cp -rd * /boot/
pi@raspberry ~$ cd ../lib
pi@raspberry ~$ sudo cp -dr * /lib/
```

Most people also disable the Low Latency Mode (llm) for the SD card:

```shell
pi@raspberry ~$ sudo nano /boot/cmdline.txt
```

Add the following option:

```ini
sdhci_bcm2708.enable_llm=0
```

## Reboot

## Testing

```shell
pi@raspberry ~$ git clone git://git.kernel.org/pub/scm/linux/kernel/git/clrkwllms/rt-tests.git
pi@raspberry ~$ cd rt-tests/
pi@raspberry ~/rt-test$ make all
pi@raspberry ~/rt-test$ sudo ./cyclictest -m -t1 -p 80 -n -i 500 -l 100000
```

## Enabling rt access

```shell
sudo su -c 'echo @audio - rtprio 99 >> /etc/security/limits.conf'
sudo su -c 'echo @audio - nice -19 >> /etc/security/limits.conf'
sudo su -c 'echo @audio - memlock unlimited >> /etc/security/limits.conf'
```


pulseaudio --dump-resample-methods

pacat -r --latency-msec=1 -d alsa_input.usb-Creative_Technology_Ltd_SB_X-Fi_Surround_5.1_Pro_000005i3-00-Pro.analog-stereo | pacat -p --latency-msec=1 -d bluez_sink.00_22_37_3D_DB_1A

