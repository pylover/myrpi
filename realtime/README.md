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

## Install and Configure the cross compile tool-chain

```shell
cd ..
user@host ~$ git clone https://github.com/raspberrypi/tools.git
user@host ~$ export ARCH=arm
user@host ~$ export CROSS_COMPILE=$(readlink -f tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-)

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
user@host ~/linux$ ssh root@raspberry "modprobe configs && cat /proc/config.gz" | zcat > .config
```

Then, you can start to configure the kernel:

```shell
user@host ~/linux$ make menuconfig
```

In the kernel configuration, enable the following settings:

CONFIG_PREEMPT_RT_FULL: Kernel Features → Preemption Model (Fully Preemptible Kernel (RT)) → Fully Preemptible Kernel (RT)
Enable HIGH_RES_TIMERS: General setup → Timers subsystem → High Resolution Timer Support (Actually, this should already be enabled in the standard configuration.)

## Build the Kernel

```shell
user@host ~/linux$ make -j4 zImage
user@host ~/linux$ make -j4 modules
user@host ~/linux$ make -j4 dtbs
user@host ~/linux$ make -j4 modules_install
```

The last command installs the kernel modules in the directory specified by INSTALL_MOD_PATH above.

## Transfer Kernel Image, Modules, and Device Tree Overlay to their Places on Raspberry Pi

```shell
user@host ~/linux$ mkdir $INSTALL_MOD_PATH/boot
user@host ~/linux$ ./scripts/mkknlimg ./arch/arm/boot/zImage $INSTALL_MOD_PATH/boot/$KERNEL.img
user@host ~/linux$ cp ./arch/arm/boot/dts/*.dtb $INSTALL_MOD_PATH/boot/
user@host ~/linux$ cp -r ./arch/arm/boot/dts/overlays $INSTALL_MOD_PATH/boot
user@host ~/linux$ cd $INSTALL_MOD_PATH
user@host ~/linux$ tar -czf /tmp/linux-image-4.9.50-rt37-v7+.tgz *
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

