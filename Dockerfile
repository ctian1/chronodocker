# FROM jrottenberg/ffmpeg
FROM python:3.8-slim-buster

# RUN apt-get update && \
#     apt-get install python3.7-dev -y && \
#     apt-get clean

# RUN python3 -m pip install pip

RUN pip install awscli boto3 

WORKDIR /tmp/workdir

COPY concat.py /tmp/workdir
COPY ffmpeg /tmp/workdir

# ENTRYPOINT ffmpeg -i ${INPUT_VIDEO_FILE_URL} -ss ${POSITION_TIME_DURATION} -vframes 1 -vcodec png -an -y ${OUTPUT_THUMBS_FILE_NAME} && ./copy_thumbs.sh
ENTRYPOINT python3 concat.py