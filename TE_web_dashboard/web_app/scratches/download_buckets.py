import csv
from influxdb_client import InfluxDBClient
from time import time
import os




cloud_org = '44b2810a938c40f7'
cloud_token = 'Ncw6Rq19Xt1FXg3JMLS8vqToZT6RON6yRM0JmiBIAx8pZTs5RBth38iPFHu0Wfw6C71sqVEGag_IKcHOx1xyow=='
cloud_url = 'https://us-east-1-1.aws.cloud2.influxdata.com'


def buckets_cloud(cloud_url,cloud_token,cloud_org):
    query = 'buckets()'

    cloud_client = InfluxDBClient(url=cloud_url, token=cloud_token, org=cloud_org)

    tables = cloud_client.query_api().query(query, org=cloud_org)
    buckets = []
    for table in tables:
        for record in table.records:
            buckets.append(record.values['name'])

    return buckets



def download_data(selected_bucket, cloud_url, cloud_token, cloud_org):

    csv_folder = "csv_files"

    script_directory = os.path.dirname(os.path.abspath(__file__))

    csv_folder = os.path.join(script_directory, csv_folder)

    if not os.path.exists(csv_folder):
        # Create the folder
        os.makedirs(csv_folder)

    csv_filename = f"{selected_bucket}.csv"
    csv_filename = csv_filename.replace(" ", "_")
    csv_filename = csv_filename.replace(":", "-")
    csv_filename = csv_filename.replace("|>", "-")

    csv_filename = os.path.join(csv_folder, csv_filename)

    # check if the selected BUCKET already exists
    if not os.path.exists(csv_filename):
        
        client = InfluxDBClient(url=cloud_url, token=cloud_token)

        # Estar atento a range, ya que habria que cambiarlo en algun momento
        query = 'from(bucket: "' + selected_bucket + '") |> range(start: -500d)'

        t0 = time()
        result = client.query_api().query(org=cloud_org, query=query)

        print(result)
        print(f'Done in {time() - t0} seconds')

        points = []

        for table in result:
            for record in table.records:
                point = {
                    "time": record.get_time(),
                    "measurement": record.get_field(), 
                    "value": record.get_value()
                }
                points.append(point)

        points = [point for point in points if point['measurement'] != 'data']

        with open(f'{csv_filename}', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["time", "measurement", "value"])
            writer.writeheader()
            for point in points:
                writer.writerow(point)

        print(f"File {csv_filename} saved in the current directory")


bucket_list = buckets_cloud(cloud_url,cloud_token,cloud_org)


absolute_file_path = os.path.abspath(__file__)

for bucket in bucket_list:
    # only those with 2023 or 2024 in the name
    if '2023' in bucket or '2024' in bucket:
        download_data(bucket, cloud_url, cloud_token, cloud_org)
        # print(absolute_file_path)