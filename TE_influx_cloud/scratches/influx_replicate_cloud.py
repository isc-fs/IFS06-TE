import datetime
from influxdb_client import InfluxDBClient, Point 
import requests

# Helper function to replicate data between time range
def replicate(bucket,oss,cloud):
  '''
  oss: list with required oss variables
      oss = [oss_url,oss_token,oss_org]

  cloud: list with required cloud variables
      cloud = [cloud_url,cloud_token,cloud_org]
  '''
  # Build query with time bounds
  query = f'from(bucket:"{bucket}")' \
          f'|> range(start: -365d)'
          
  
  # Create client connections
  oss_client = InfluxDBClient(url=oss[0], token=oss[1], org=oss[2])
  cloud_client = InfluxDBClient(url=cloud[0], token=cloud[1], org=cloud[2])

  # Read data from OSS
  tables = oss_client.query_api().query(query, org=oss[2])


  write_api = cloud_client.write_api()
  # write_options=WriteOptions(use_timestamp=True)
  # Usando SYNCHRONOUS va de uno en uno (estamos 2 dias aqui)

  # Write data to Cloud
  for table in tables:
      for record in table.records:
          ts = int(record.values["_time"].timestamp() * 1e9)
          # Convertimos a formato timestamp
          point = [Point(record.get_measurement()).field(record.get_field(), record.get_value()).time(ts)]


          write_api.write(bucket=bucket,
                          record=point,
                          content_encoding="identity",
                          content_type="text/plain; charset=utf-8",)
          # if record.get_measurement() == '0x600':
            # print(f'Write id {record.get_measurement()} with data {record.get_field()} - {record.get_value()} at {record.values["_time"]}')

  write_api.close()
  # print(f"Replicated data from {bucket} range 30days")


def query_oss(oss_bucket,oss_url,oss_token,oss_org):
  '''
  Usado como pruebas para los queries, nada mas
  '''

     # Build query with time bounds
     # 2023-09-24 18:37:53
  query = 'buckets()'

  query_2 = f'from(bucket:"{oss_bucket}")' \
          f'|> range(start: -30d)'
  
  oss_client = InfluxDBClient(url=oss_url, token=oss_token, org=oss_org)

  # Read data from OSS
  result = oss_client.query_api().query(query, org=oss_org)

  # Usar list comprehension mas adelante
  for table in result:
        for record in table.records:
           print(record.values['name'])
           # print(record.values['_time'])
           #print(f'as timestamp {int(record.values["_time"].timestamp() * 1e9)}')
           # print(record.values)