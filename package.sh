#!/usr/bin/env bash

zip -x '.idea/*' '.git/*' '.env' '*.zip' '*/.aws-sam/*' -9 -FS source.zip -r .
aws s3 cp source.zip "s3://${SOURCE_BUCKET}"
