#!/bin/sh
# Install Python package wheels from local vendor directory without internet.

set -e

if [ ! -d "vendor" ]; then
  echo "Vendor directory not found. Please place wheel files in ./vendor" >&2
  exit 1
fi

pip install --no-index --find-links=vendor -r requirements.txt
