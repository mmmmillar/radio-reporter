from recognise.lib.track import Track
from datetime import datetime
from dotenv import load_dotenv
import asyncio
import os
import boto3
from shazamio import Shazam, serialize_track

load_dotenv()


def download_from_s3(record):
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    file_path = f'/tmp/{key}'
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)

    with open(file_path, 'wb') as f:
        for chunk in response['Body'].iter_chunks():
            f.write(chunk)

    stream_title = response['Metadata']['stream_title']

    return file_path, stream_title


def create_put_item(pk, sk):
    return {
        'Put': {
            'Item': {
                'pk': {
                    'S': pk
                },
                'sk': {
                    'S': sk
                },
            },
            'TableName': f"{os.environ['DYNAMO_TABLE_NAME']}"
        }
    }


def write_to_dynamo(track):
    dynamo = boto3.client('dynamodb')

    now = datetime.now()
    today = now.strftime('%Y%m%d')
    timestamp = now.isoformat()

    transactItems = []

    trackItem = create_put_item(
        f'TRACK#{track.title}', f'ARTIST#{track.artist}#SHOW#{track.show}#{today}')
    trackItem['Put']['ConditionExpression'] = 'attribute_not_exists(pk) AND attribute_not_exists(sk)'
    trackItem['Put']['Item']['Timestamp'] = {'S': timestamp}
    trackItem['Put']['Item']['Genres'] = {
        'L': [{'S': x} for x in track.genres]}
    transactItems.append(trackItem)

    for genre in track.genres:
        genreItem = create_put_item(
            f'GENRE#{genre}', f'{today}#ARTIST#{track.artist}#TRACK#{track.title}#SHOW#{track.show}')
        transactItems.append(genreItem)

    try:
        dynamo.transact_write_items(TransactItems=transactItems)
    except dynamo.exceptions.TransactionCanceledException as err:
        print('Track already exists in db')


async def get_shazam_track_info(file_path):
    shazam = Shazam()
    result = await shazam.recognize_song(file_path)
    if(len(result['matches']) == 0):
        return None
    return serialize_track(data=result['track'])


async def process_records(records):
    for record in records:
        file_path, stream_title = download_from_s3(record)
        shazam_info = await get_shazam_track_info(file_path)
        os.remove(file_path)

        if(shazam_info is None):
            print(f'No shazam match from {stream_title}')
            return False

        track = Track(shazam_info.title, shazam_info.subtitle, stream_title)
        print(track)
        write_to_dynamo(track)

    return True


def handler(event, _):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process_records(event['Records']))


# if __name__ == '__main__':
#     handler(None, None)
