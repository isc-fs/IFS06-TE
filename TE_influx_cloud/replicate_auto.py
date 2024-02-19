from scratches.list_buckets_functions import buckets_cloud,buckets_oss
from scratches.create_bucket import create_bucket
from scratches.influx_replicate_cloud import replicate

from time import time

from dotenv import load_dotenv
# libreria: python-dotenv
import os

import requests

# Load variables from .env file
print('Loading .env variables')
load_dotenv()

cloud_org = os.environ.get('CLOUD_ORG')
cloud_token = os.environ.get('CLOUD_TOKEN')
cloud_url = os.environ.get('CLOUD_URL')
cloud_url_buckets = os.environ.get('CLOUD_URL_BUCKETS')
oss_org = os.environ.get('OSS_ORG')
oss_token = os.environ.get('OSS_TOKEN')
oss_url = os.environ.get('OSS_URL')

print('Loading buckets list from OSS and CLOUD')
bucket_oss = buckets_oss(oss_url,oss_token,oss_org)
print('1')
bucket_cloud = buckets_cloud(cloud_url,cloud_token,cloud_org)

print('2')
oss = [oss_url,oss_token,oss_org]
print('3')
cloud = [cloud_url,cloud_token,cloud_org]


for bucket in bucket_oss:
    if bucket not in bucket_cloud:
        print('Creating bucket...')
        create_bucket(bucket,cloud_url_buckets,cloud_token,cloud_org)
        print(f'Replicating bucket {bucket}')
        t0 = time()
        replicate(bucket,oss,cloud)
        print(f'Done in {time()-t0}')
        # print('Waiting 5 seconds...')
        # time.sleep(5)