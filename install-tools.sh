#!/usr/bin/env bash
set -e
if command -v apt-get >/dev/null 2>&1; then
    ./install-apt.sh
elif command -v brew >/dev/null 2>&1; then
    ./install-brew.sh
else
    echo "Unsupported platform. Install dependencies manually." >&2
    exit 1
fi
./setup.sh
