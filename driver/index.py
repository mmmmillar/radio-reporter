import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()


def handler(_, __):
    client = boto3.client('lambda')
    urls = os.environ['STREAM_URLS'].split(",")
    for url in urls:
        client.invoke(FunctionName=os.environ['SAMPLE_LAMBDA_NAME'],
                      InvocationType='Event',
                      Payload=bytes(json.dumps({'stream_url': url}), encoding='utf8'))
    return True


# if __name__ == '__main__':
#     handler(None, None)
