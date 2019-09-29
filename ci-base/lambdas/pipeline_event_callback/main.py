import json
import logging
import os

import boto3

logging.getLogger().setLevel(logging.DEBUG)

# Sample event data
#
# [
#     {
#         "version": "0",
#         "id": "CWE-event-id",
#         "detail-type": "CodePipeline Pipeline Execution State Change",
#         "source": "aws.codepipeline",
#         "account": "123456789012",
#         "time": "2017-04-22T03:31:47Z",
#         "region": "us-east-1",
#         "resources": [
#             "arn:aws:codepipeline:us-east-1:123456789012:pipeline:myPipeline"
#         ],
#         "detail": {
#             "pipeline": "myPipeline",
#             "version": "1",
#             "state": "STARTED",
#             "execution-id": "01234567-0123-0123-0123-012345678901"
#         }
#     }
#     {
#         "version": "0",
#         "id": "CWE-event-id",
#         "detail-type": "CodePipeline Stage Execution State Change",
#         "source": "aws.codepipeline",
#         "account": "123456789012",
#         "time": "2017-04-22T03:31:47Z",
#         "region": "us-east-1",
#         "resources": [
#             "arn:aws:codepipeline:us-east-1:123456789012:pipeline:myPipeline"
#         ],
#         "detail": {
#             "pipeline": "myPipeline",
#             "version": "1",
#             "execution-id": "01234567-0123-0123-0123-012345678901",
#             "stage": "Prod",
#             "state": "STARTED"
#         }
#     }
#     {
#         "version": "0",
#         "id": "CWE-event-id",
#         "detail-type": "CodePipeline Action Execution State Change",
#         "source": "aws.codepipeline",
#         "account": "123456789012",
#         "time": "2017-04-22T03:31:47Z",
#         "region": "us-east-1",
#         "resources": [
#             "arn:aws:codepipeline:us-east-1:123456789012:pipeline:myPipeline"
#         ],
#         "detail": {
#             "pipeline": "myPipeline",
#             "version": 1,
#             "execution-id": "01234567-0123-0123-0123-012345678901",
#             "stage": "Prod",
#             "action": "myAction",
#             "state": "STARTED",
#             "region": "us-west-2",
#             "type": {
#                 "owner": "AWS",
#                 "category": "Deploy",
#                 "provider": "CodeDeploy",
#                 "version": 1
#             }
#         }
#     }
# ]

PIPELINE_PREFIX = os.getenv('PIPELINE_PREFIX', '')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

sns = boto3.client('sns')


def lambda_handler(event: dict, context):
    logging.debug(event)

    pipeline_name = event['detail']['pipeline']

    # only response to pipeline starts with defined prefix
    if PIPELINE_PREFIX:
        if not pipeline_name.startswith(PIPELINE_PREFIX):
            logging.warning(f'Ignoring events for {pipeline_name}.')
            return

    # get optional other data
    pipeline_version = event['detail'].get('version', 0)
    stage_name = event['detail'].get('stage', None)
    action_name = event['detail'].get('action', None)

    # format title
    title = f"{event['detail']['state']} - Pipeline={pipeline_name}:{pipeline_version}"
    if stage_name:
        title += f"->{stage_name}"
    if action_name:
        title += f"->{action_name}"

    logging.debug(f'{title}')

    # use json as message body
    message = json.dumps(event, indent=2)
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject=title,
    )

    logging.debug(response)
