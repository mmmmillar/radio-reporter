# Radio reporter

Radio reporter listens to your favourite streaming radio stations and identifies and reports on what songs are being played.

Songs have quite a bit of metadata associated with them so I wrote this to build a dataset that I could visualise. I'll also be able to build dope playlists with it.

## Requirements

This application is designed to live on AWS (requires account) and requires Python 3, Node.js, and Serverless

- [Python](https://www.python.org)
- [Node.js](https://nodejs.org)
- [Serverless Framework](https://www.serverless.com)

You will need to register as a spotify developer and create an app [here](https://developer.spotify.com)

You will also need to deploy ffmpeg-lambda-layer to your AWS account. You can do that [here](https://serverlessrepo.aws.amazon.com/applications/us-east-1/145266761615/ffmpeg-lambda-layer)

## Environment variables

You will need to create a copy of `.env.sample` in the root directory and rename it to `.env` before updating the values as you want them

- `STREAM_URLS` - comma separated list of radio stream urls
- `SPOTIPY_CLIENT_ID` - the client id from your spotify app
- `SPOTIPY_CLIENT_SECRET` - the client secret from your spotify app
- `FFMPEG_ARN` - the arn from your ffmpeg-lambda-layer deployment

## Build the dependency layers

As the layers are already included in this repo, this only needs to be done if you want to update the package versions

```bash
docker build -f Dockerfile -t reporterlayers:latest .
docker run -dit reporterlayers:latest
docker cp {container_id}:/var/task/recogniselayer.zip .
docker cp {container_id}:/var/task/dotenvlayer.zip .
```

## Deploy to AWS

```bash
sls deploy
```

## Remove the service

```bash
sls remove
```

## Future enhancements

- Remove the dependency on s3 to reduce cost (send data direct to lambda)
- Move the stream url list from env to json file to allow extra metadata (station name etc)
- Add extra access patterns to DynamoDB (artist, show)
- Add visualisation dashboard
