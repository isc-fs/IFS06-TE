from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "2023-09-24 14:51:40 |> FS-canto_acceleration_2-marco"
org = ""
token = ""

client = InfluxDBClient(url="http://localhost:8086", token=token)

query = f"""
from(bucket: "{bucket}")
  |> range(start: -7d) 
  |> time(v: v, column: "_time")
  |> first()
  |> map(fn: (r) => ({{"earliest": r._time}})) 
  |> yield(name: "earliest")

  |> range(start: -7d)
  |> time(v: v, column: "_time")
  |> last()
  |> map(fn: (r) => ({{"latest": r._time}}))
  |> yield(name: "latest")  
"""
result = client.query_api().query(org=org, query=query)

start = result[0]['earliest'][0]['earliest']
end = result[0]['latest'][0]['latest']

print(f"Time range: {start} to {end}")

