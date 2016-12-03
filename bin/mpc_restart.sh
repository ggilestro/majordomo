#!/bin/bash

sudo kill -9 `pidof mpd`
sleep 1
sudo systemctl restart mpd
bin/say -l EN -s "Radio restarted"
