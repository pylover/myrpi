#!/usr/bin/env bash

sudo apt-get install pulseaudio pulseaudio-utils pavumeter pavucontrol paman paprefs


pactl load-module module-loopback latency_msec=1

pactl unload-module $(pactl list short modules | awk '$2 =="module-loopback" { print $1 }' - )
