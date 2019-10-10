#!/usr/bin/env bash
set -ex

# lambda layers expect package content under "python"
mkdir -p /tmp/staging/python

# pip install to staging dir
pip install -r /var/task/requirements.txt -t /tmp/staging/python

# zipping the dir
cd /tmp/staging
zip -r9 -FS /tmp/build/common-layer.zip .

# hack: generate description with requirement checksum
cd /tmp/build/
echo "Description: $(cat common-layer.md5)" > common-layer.yaml

du -h common-layer.zip
cat common-layer.yaml
