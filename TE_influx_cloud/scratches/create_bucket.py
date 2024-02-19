import requests

def create_bucket(bucket_name,cloud_url,cloud_token,cloud_org):
   '''
   cloud_url needed is CLOUD_URL_BUCKETS
   '''
   payloadnever = {
    "orgID": cloud_org,
    "name": bucket_name,
    "rp": "myrp",
    "duration":"INF",
    "schemaType": "implicit"
    }
   headers = {'Authorization': f'Token {cloud_token}'}
   r1 = requests.post(cloud_url, headers=headers, json=payloadnever)
   print(r1)