#!/bin/sh
sudo apt-get update
sudo apt-get install -y outguess steghide zsteg stegexpose python3-pip ffmpeg dnsutils
pip3 install -r requirements.txt
