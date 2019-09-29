#!/usr/bin/env bash
set -ex

# lambda layers expect package content under "python"
mkdir -p /tmp/staging/python

# pip install to staging dir
pip install -r /var/task/requirements.txt -t /tmp/staging/python

# zipping the dir
cd /tmp/staging/
zip -r9 -FS /var/build/layer.zip .

# hack: generate description with layer zip checksum
cd /var/build/
echo "Description: Python3.7 common layer, checksum=$(cat requirements.md5)" > template-fragment.yaml
