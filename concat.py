import json
import urllib.parse
import boto3
from botocore.errorfactory import ClientError
from botocore.config import Config
import os
import subprocess
import time
import math
import shutil
import traceback

print('Loading function')



S3_BUCKET = "mys3bucket"

s3 = boto3.client('s3')

# config=Config(read_timeout=301, retries={'max_attempts': 0})
# lamb = boto3.client('lambda', config=config)



def handler(event, context):
    # event = {
    #     clips_path: "clips/",
    #     render_output: "renders/full_video.mp4",
    #     clips: [
    #         "intro.mp4",
    #         "clip1.mp4",
    #         "clip2.mp4"
    #     ]
    # }

    # print("Received event: " + json.dumps(event, indent=2))

    clips = event['clips']
    clips_path = event['clips_path']
    render_output = event['render_output']
    try:
        with open('/tmp/clips.txt', 'w') as f:
            assert len(clips) > 0
            for clip in clips:
                s3path = f"clips_path{clip}"

                tmppath = f"/tmp/{clip}"

                try:
                    s3.download_file(S3_BUCKET, s3path, tmppath)
                except ClientError:
                    return f"fail: clip {s3path} missing"

                f.write(f"file '{tmppath}'\n")
            
        os.system(f"""./ffmpeg -y -f concat -safe 0 -i /tmp/clips.txt -c copy -movflags +faststart /tmp/out.mp4""")

        s3.upload_file("/tmp/out.mp4", S3_BUCKET, render_output)


        return 'success'
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise e from None


if __name__ == "__main__":
    handler(json.loads(os.environ["RENDER_JSON"]), None)