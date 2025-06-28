#!/usr/bin/env bash
# Install common external stego tools automatically.
set -e
if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y outguess steghide zsteg stegexpose
elif command -v brew >/dev/null 2>&1; then
    brew update
    brew install outguess steghide zsteg stegexpose
else
    echo "Unsupported platform. Install tools manually." >&2
    exit 1
fi
