#!/usr/bin/env bash

sudo pip install pybluez
sudo hciconfig hci0 piscan
sudo sdptool add sp
sudo service bluetooth restart