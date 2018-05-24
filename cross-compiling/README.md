
# Cross compiling for rpi3 stretch


## Setup (Clone the rpi kernel and toolchain)

```shell
./setup.sh
```
## Build kernel


```bash
source activate.sh
./build-kernel.sh
```

# Copy the image into the rpi using ssh

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

