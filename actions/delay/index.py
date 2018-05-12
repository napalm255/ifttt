#!/usr/bin/env python
"""
NapOnline IFTTT.

Action: Notify
"""
# pylint: disable=broad-except

from __future__ import print_function
import sys
import logging
import json
from urllib.parse import parse_qsl
# import boto3


# logging configuration
logging.getLogger().setLevel(logging.INFO)


def header():
    """Return header object."""
    return {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'}


def error(message, code=403):
    """Return error object."""
    output = {'statusCode': code,
              'body': json.dumps({'status': 'ERROR',
                                  'message': message}),
              'headers': header()}
    logging.error(output)
    return output


def handler(event, context):
    """Lambda handler."""
    # pylint: disable=unused-argument
    logging.info(event)

    # read event headers
    headers = dict((k.lower(), v) for k, v in event['headers'].items())

    # load data
    try:
        # content-type
        ctype = 'application/x-www-form-urlencoded'
        assert ctype in headers['content-type'].lower(), 'invalid content-type'
        data = dict(parse_qsl(event['body']))
        logging.info(data)
    except (ValueError, AssertionError) as ex:
        return error(str(ex))
    except Exception as ex:
        return error('unexpected error loading data (%s)' % ex)

    output = {'statusCode': 200,
              'body': json.dumps({'status': 'OK',
                                  'data': data}),
              'headers': header()}
    logging.info(output)
    return output


if __name__ == '__main__':
    KEY = sys.argv[1]
    BODY = sys.argv[2]
    print(BODY)
    print(handler({'headers': {'x-api-key': KEY,
                               'Content-Type':
                               'application/x-www-form-urlencoded'},
                   'requestContext': {'identity': {'sourceIp': '6.9.6.9'}},
                   'body': BODY}, None))
