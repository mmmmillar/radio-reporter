import re
import time
from urllib.request import urlopen, Request
import boto3
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
SAMPLE_SIZE_IN_BYTES = 250000


def get_stream_data(response):
    return response.read(SAMPLE_SIZE_IN_BYTES)


def get_stream_title(stream, data):
    icy_metaint_header = stream.headers.get('icy-metaint')

    if icy_metaint_header is not None:
        meta_start = int(icy_metaint_header)
        meta_end = meta_start + 255
        content = data[meta_start:meta_end].decode('ascii', 'ignore')
        return re.search(r"StreamTitle='(.*)';", content).group(1)

    return None


def upload_to_s3(title, data):
    s3 = boto3.client('s3')
    s3.upload_fileobj(BytesIO(data),
                      os.environ['BUCKET_NAME'], f'{time.monotonic() }',
                      ExtraArgs={"Metadata": {"stream_title": title}})


def handler(event, _):
    request = Request(event['stream_url'], None, {'icy-metadata': 1})
    stream = urlopen(request)

    data = get_stream_data(stream)
    title = get_stream_title(stream, data)
    print(f'Sampled {event["stream_url"]}, StreamTitle={title}')

    upload_to_s3(title, data)

    return True


# if __name__ == '__main__':
#     handler(None, None)
