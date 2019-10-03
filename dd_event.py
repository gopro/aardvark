import argparse
import datadog
import json
import os

from boto3.session import Session


DEFAULT_REGION = 'us-east-2'
DATADOG_EVENTS = {
    'start': {
        'title': 'Aardvark cronjob start',
        'text': '',
        'aggregation_key': 'aardvark',
        'alert_type': 'info',
        'tags': ['aardvark']
    },
    'end': {
        'title': 'Aardvark cronjob end',
        'text': '',
        'aggregation_key': 'aardvark',
        'alert_type': 'info',
        'tags': ['aardvark']
    }
}


def get_args_parser():
    parser = argparse.ArgumentParser(description='Send datadog events signaling the start/end of aardvark collector cronjob.')
    parser.add_argument('event',
                        choices=['start', 'end'],
                        action='store')
    args = parser.parse_args()
    return args, parser


def get_session():
    session = Session()
    return session


def get_sm_secret(secret_id, cl):
    secret = cl.get_secret_value(SecretId=secret_id)
    return secret['SecretString']


if __name__ == '__main__':
    args, parser = get_args_parser()
    session = get_session()
    datadog_secret = os.environ['DATADOG_SECRET']
    aws_region = os.environ.get('AWS_REGION', DEFAULT_REGION)

    cl_sm = session.client('secretsmanager', region_name=aws_region)
    datadog_keys = json.loads(get_sm_secret(secret_id=datadog_secret, cl=cl_sm))
    datadog.initialize(**datadog_keys)
    datadog.api.Event.create(DATADOG_EVENTS[args.event])
