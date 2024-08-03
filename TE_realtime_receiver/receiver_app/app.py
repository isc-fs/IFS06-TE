from flask import Flask, render_template, request, jsonify
import threading
import time
from datetime import datetime
import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import struct
import sys
import traceback
import pigpio
from nrf24 import *

app = Flask(__name__)

# Mock data to simulate incoming data
mock_data = [
    "2024-07-22 10:00:00.000: ID: 0x610, ax: 1.23, ay: 2.34, az: 3.45, GyroX: 0.12, GyroY: 0.34, GyroZ: 0.56",
    "2024-07-22 10:00:10.000: ID: 0x620, ax: 1.25, ay: 2.36, az: 3.47, GyroX: 0.14, GyroY: 0.36, GyroZ: 0.58",
    "2024-07-22 10:00:20.000: ID: 0x630, throttle: 50, brake: 10",
    "2024-07-22 10:00:30.000: ID: 0x640, current_sensor: 1.5, cell_min_v: 3.7, cell_max_temp: 40",
    "2024-07-22 10:00:40.000: ID: 0x650, speed: 100, lat: 40.7128, long: -74.0060, alt: 10",
    "2024-07-22 10:00:50.000: ID: 0x670, FR: 0.5, FL: 0.6, RR: 0.7, RL: 0.8",
    "2024-07-22 10:01:00.000: ID: 0x660, inverter_in: 1.1, inverter_out: 1.2, motor_in: 1.3, motor_out: 1.4"
]

data_received = False


print('1')
client = InfluxDBClient(url="http://localhost:8086",
                        token="sNZJlQsv2KhY28xPDZBmt2HbgGtwU5AE4vUjQsks9WPm3o0g_UreLkxNVgMHNotIqUMHCcgAyN4llUvdXs4QtA==",
                        org="b2b03940375e28ac")
print('2')

current_data = []

COM = "COM4"
bucket = "e0e3f2d24fd93e79"


def rxnrf24(bucketnever, piloto, circuito):
    global data_received, current_data
    
    # Connect to pigpiod
    pi = pigpio.pi()
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(5)
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, '1SNSR')
    nrf.show_registers()

    write_api = client.write_api(write_options=SYNCHRONOUS)

    try:
        count = 0
        while True:
            while nrf.data_ready():
                count += 1
                now = datetime.now()
                pipe = nrf.data_pipe()
                payload = nrf.get_payload()
                id = hex(int(payload[0])) if len(payload) > 0 else -1
                hex_msg = ':'.join(f'{i:02x}' for i in payload)

                if len(payload) == 32:
                    values = struct.unpack("<ffffffff", payload)
                    dataid = values[0]

                    if dataid == 0x610:
                        p = Point("0x610").field("ax", values[1]).field("ay", values[2]).field("az", values[3]).field("wx", values[4]).field("wy", values[5]).field("wz", values[6])
                    elif dataid == 0x620:
                        p = Point("0x620").field("ax", values[1]).field("ay", values[2]).field("az", values[3]).field("wx", values[4]).field("wy", values[5]).field("wz", values[6])
                    elif dataid == 0x600:
                        p = Point("0x600").field("motor_temp", values[1]).field("igbt_temp", values[2]).field("inverter_temp", values[3]).field("n_actual", values[4]).field("dc_bus_voltage", values[5]).field("i_actual", values[6])
                    elif dataid == 0x630:
                        p = Point("0x630").field("throttle", values[1]).field("brake", values[2])
                    elif dataid == 0x640:
                        p = Point("0x640").field("current_sensor", values[1]).field("cell_min_v", values[2]).field("cell_max_temp", values[3])
                    elif dataid == 0x650:
                        p = Point("0x650").field("speed", values[1]).field("lat", values[2]).field("long", values[3]).field("alt", values[3])
                    elif dataid == 0x670:
                        p = Point("0x670").field("Suspension_FR", values[1]).field("Suspension_FL", values[2]).field("Suspension_RR", values[3]).field("Suspension_RL", values[4])
                    elif dataid == 0x660:
                        p = Point("0x660").field("Inverter_inlet", values[1]).field("Inverter_outlet", values[2]).field("Motor_inlet", values[3]).field("Motor_outlet", values[4])
                    else:
                        p = Point("unknown").field("value", values[0])
                    
                    write_api.write(bucket=bucketnever, record=p)
                    write_api.write(bucket=bucket, record=p)

                    data_received = True
                    current_data.append(f"{now:%Y-%m-%d %H:%M:%S.%f}: ID: {pipe}, len: {len(payload)}, bytes: {hex_msg}, count: {count}")

            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

def writerundata(piloto, circuito):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = Point("piloto").field("data", piloto)
    write_api.write(bucket=bucketnever, record=p)
    write_api.write(bucket=bucket, record=p)
    p = Point("circuito").field("data", circuito)
    write_api.write(bucket=bucketnever, record=p)
    write_api.write(bucket=bucket, record=p)

def createbucket(piloto, circuito):
    headers = {'Authorization': 'Token sNZJlQsv2KhY28xPDZBmt2HbgGtwU5AE4vUjQsks9WPm3o0g_UreLkxNVgMHNotIqUMHCcgAyN4llUvdXs4QtA=='}
    url = "http://localhost:8086/api/v2/buckets"
    payloadnever = {
        "orgID": "b2b03940375e28ac",
        "name": datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " |> FS-" + circuito + "-" + piloto,
        "description": "create a bucket",
        "rp": "myrp",
        "duration": "INF"
    }
    r = requests.post(url, headers=headers, json=payloadnever)
    return r.json()['id']

def monitor_data():
    global data_received
    while True:
        time.sleep(10)
        if data_received:
            print("Data received")
            data_received = False
        else:
            print("No data received")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        piloto = request.form['piloto']
        circuito = request.form['circuito']
        bucketnever = createbucket(piloto, circuito)
        threading.Thread(target=rxnrf24, args=(bucketnever, piloto, circuito)).start()
        return render_template('index.html', data_received=data_received, current_data=current_data, piloto=piloto, circuito=circuito)
    return render_template('index.html', data_received=data_received, current_data=current_data, piloto=None, circuito=None)

@app.route('/check_data', methods=['GET'])
def check_data():
    return jsonify({'data_received': data_received, 'current_data': current_data})

if __name__ == '__main__':
    threading.Thread(target=monitor_data).start()
    app.run(host='0.0.0.0', port=5000)