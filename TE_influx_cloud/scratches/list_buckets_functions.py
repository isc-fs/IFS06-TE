from influxdb_client import InfluxDBClient

def buckets_cloud(cloud_url,cloud_token,cloud_org):
    query = 'buckets()'

    cloud_client = InfluxDBClient(url=cloud_url, token=cloud_token, org=cloud_org)

    tables = cloud_client.query_api().query(query, org=cloud_org)
    buckets = []
    for table in tables:
        for record in table.records:
            buckets.append(record.values['name'])

    return buckets

def buckets_oss(oss_url,oss_token,oss_org):

    # Build query with time bounds
    # 2023-09-24 18:37:53
    query = 'buckets()'
    oss_client = InfluxDBClient(url=oss_url, token=oss_token, org=oss_org)

    # Read data from OSS
    result = oss_client.query_api().query(query, org=oss_org)

    # Usar list comprehension mas adelante
    buckets = []
    for table in result:
            for record in table.records:
                buckets.append(record.values['name'])
    return buckets