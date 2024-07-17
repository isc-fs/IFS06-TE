from scratches.list_buckets_functions import buckets_cloud,buckets_oss
from scratches.create_bucket import create_bucket
from scratches.influx_replicate_cloud import replicate

from time import time

from dotenv import load_dotenv
# libreria: python-dotenv
import os

import requests



'''
Code will only work on rasberry pi with influxdd installed


Onboarding script to replicate data from OSS to Cloud
    Minimal changes from replicate_auto.py
    - Removed print statements
    - Will only replicate when wifi conectivity is available
    - Assume when conection to wifi, car has stopped running (REVISAR)
            Se podria conectar sin querer a wifi y replicar datos que estan llegando aun

Probably should run script on start of onboard device, check for wifi connection and replicate data every X minutes



variables en .env (meter de nuevo si se cambia de maquina)

Sacas los buckets de OSS y de CLOUD y comparas

Funcion clave para replicar: replicate(bucket,oss,cloud) en influx_replicate_cloud.py

'''


def verificar_conexion_internet(url="http://www.google.com", timeout=5):
    '''
    Self explanatory...
    '''
    try:
        # Make a GET request and check if the status code is 200
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        # If there is a connection error, assume there is no internet
        return False


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



while True:
    time.sleep(60)
    # Check if wifi is connected
    if verificar_conexion_internet():
        print('Loading buckets list from OSS and CLOUD')
        bucket_oss = buckets_oss(oss_url,oss_token,oss_org)
        bucket_cloud = buckets_cloud(cloud_url,cloud_token,cloud_org)

        oss = [oss_url,oss_token,oss_org]
        cloud = [cloud_url,cloud_token,cloud_org]


        for bucket in bucket_oss:
            if bucket not in bucket_cloud:
                print('Creating bucket...')
                create_bucket(bucket,cloud_url_buckets,cloud_token,cloud_org)
                print(f'Replicating bucket {bucket}')
                t0 = time()
                replicate(bucket,oss,cloud)
                print(f'Done in {time()-t0}')
    else:
        print('Wifi not connected')


