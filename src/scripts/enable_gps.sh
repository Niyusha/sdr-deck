#!/bin/sh

sudo systemctl stop gpsd
sudo echo -e '\xB5\x62\x02\x41\x08\x00\x00\x00\x00\x00\x01\x00\x00\x00\x4C\x37' > /dev/ttyS0
sudo systemctl start gpsd
