import logging
import os

import awsgi
from aws_xray_sdk.core import patch_all

from todoapi import create_app

patch_all()

app = create_app()

logging.getLogger().setLevel(os.getenv('LOG_LEVEL', 'WARNING'))


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
