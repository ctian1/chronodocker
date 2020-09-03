# chronodocker

Amazon ECS Task for stitching together video clips using FFMPEG

With the default FFMPEG parameters, the clips must be encoded exactly the same way so that FFMPEG can stitch the clips together as quickly as possible.



## How to use

First, set up this repository as an ECS task in AWS

```python
import boto3, json

ecs = boto3.client('ecs')

clips = {
    clips_path: "clips/",
    render_output: "renders/full_video.mp4",
    clips: [
        "intro.mp4",
        "clip1.mp4",
        "clip2.mp4"
    ]
}

ecs.run_task(
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                '[ subnet ]',
            ],
            'assignPublicIp': 'ENABLED'
        }
    },
    overrides={
        "containerOverrides": [
            {
                "name": "[ ecs task name ]",
                "environment":[
                    {
                        "name": "RENDER_JSON",
                        "value": json.dumps(clips)
                    }
                ]
            }
        ]
    },
    launchType="FARGATE",
    cluster="default",
    taskDefinition="[ ecs task name and version ]"
)
```