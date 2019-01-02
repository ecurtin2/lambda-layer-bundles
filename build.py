import os
import subprocess

with open('requirements.txt') as f:
    requirements = f.read()

layer_name = 'pandas-py37'
image = 'layer-py37'
bucket = '<BUCKET_HERE>'

cmd = [
    'docker', 'run', 
    '-e', f'LAYER_NAME={layer_name}',
    '-e', f'REQUIREMENTS={requirements}',
    '-e', f'AWS_ACCESS_KEY_ID={os.environ['AWS_ACCESS_KEY_ID']}',
    '-e', f'AWS_SECRET_ACCESS_KEY={os.environ['AWS_SECRET_ACCESS_KEY']}',
    '-e', f'AWS_DEFAULT_REGION=us-east-1',
    '-e', f'S3_BUCKET={bucket}',
    'layer-py37'
]

subprocess.run(cmd)
