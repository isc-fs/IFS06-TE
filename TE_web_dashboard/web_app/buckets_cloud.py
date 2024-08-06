import os
import csv
from influxdb_client import InfluxDBClient
from time import time

CLOUD_ORG = '44b2810a938c40f7'
CLOUD_TOKEN = 'Ncw6Rq19Xt1FXg3JMLS8vqToZT6RON6yRM0JmiBIAx8pZTs5RBth38iPFHu0Wfw6C71sqVEGag_IKcHOx1xyow=='
CLOUD_URL = 'https://us-east-1-1.aws.cloud2.influxdata.com'
CLOUD_URL_BUCKETS = 'https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/buckets'

OSS_ORG = 'b2b03940375e28ac'
OSS_TOKEN = 'sNZJlQsv2KhY28xPDZBmt2HbgGtwU5AE4vUjQsks9WPm3o0g_UreLkxNVgMHNotIqUMHCcgAyN4llUvdXs4QtA=='
OSS_URL = 'http://localhost:8086'


# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(base_dir, 'csv_files')


def csv_buckets():
    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
    return [f.split('.')[0] for f in csv_files]

def buckets_cloud(cloud_url, cloud_token, cloud_org):
    query = 'buckets()'
    cloud_client = InfluxDBClient(url=cloud_url, token=cloud_token, org=cloud_org)
    tables = cloud_client.query_api().query(query, org=cloud_org)
    buckets = []
    for table in tables:
        for record in table.records:
            buckets.append(record.values['name'])

    replaced_buckets = []
    for bucket in buckets:
        bucket_ = bucket.replace(" ", "_").replace(":", "-").replace("|>", "-")
        replaced_buckets.append(bucket_)

    return buckets, replaced_buckets

def download_bucket(selected_bucket, cloud_url, cloud_token, cloud_org):

    # check if the selected bucket contains any of the words in the invalid list
    ignore_buckets = ["test", "ISC", "RPI", "_monitoring", "_tasks", "version_"]

    if any(word in selected_bucket for word in ignore_buckets):
        print(f"Bucket {selected_bucket} is not valid")
        return

    csv_folder = CSV_DIR

    if not os.path.exists(csv_folder):
        csv_folder = os.getcwd()


    client = InfluxDBClient(url=cloud_url, token=cloud_token)

    # Estar atento a range, ya que habria que cambiarlo en algun momento
    query = 'from(bucket: "' + selected_bucket + '") |> range(start: -500d)'

    t0 = time()
    result = client.query_api().query(org=cloud_org, query=query)

    print(result)
    print(f'Done in {time() - t0} seconds')

    points = []

    csv_filename = f"{selected_bucket}.csv"
    csv_filename = csv_filename.replace(" ", "_")
    csv_filename = csv_filename.replace(":", "-")
    csv_filename = csv_filename.replace("|>", "-")

    csv_filename = os.path.join(csv_folder, csv_filename)

    for table in result:
        for record in table.records:
            point = {
                "time": record.get_time(),
                "measurement": record.get_field(), 
                "value": record.get_value()
            }
            points.append(point)

    points = [point for point in points if point['measurement'] != 'data']

    print(len(points))

    if len(points) == 0:
        print(f"No data found for bucket {selected_bucket}")
        return

    with open(f'{csv_filename}', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["time", "measurement", "value"])
        writer.writeheader()
        for point in points:
            writer.writerow(point)

    print(f"File {csv_filename} saved in the current directory")

def compare_and_download_buckets(cloud_url, cloud_token, cloud_org):
    original_cloud_buckets, replaced_cloud_buckets = buckets_cloud(cloud_url, cloud_token, cloud_org)
    local_buckets = csv_buckets()

    # Encontrar los índices de los buckets en la nube que no están en los archivos CSV locales
    missing_indices = [i for i, bucket in enumerate(replaced_cloud_buckets) if bucket not in local_buckets]

    # Descargar los buckets faltantes usando los índices para obtener los nombres originales
    for index in missing_indices:
        download_bucket(original_cloud_buckets[index], cloud_url, cloud_token, cloud_org)


compare_and_download_buckets(CLOUD_URL, CLOUD_TOKEN, CLOUD_ORG)