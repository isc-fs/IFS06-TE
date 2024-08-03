from flask import Flask, render_template, request, jsonify
import threading
import time
import random
from datetime import datetime
import csv

app = Flask(__name__)

data_received = False
current_data = []
all_data = []
csv_filename = None
stop_event = threading.Event()
start_saving_event = threading.Event()
lock = threading.Lock()  # Add a lock for thread-safe data access

# Function to generate random data
def generate_random_data():
    global data_received, current_data, all_data, stop_event

    while not stop_event.is_set():
        now = datetime.now()
        data_type = random.choice(["0x610", "0x620", "0x630", "0x640", "0x650", "0x670", "0x660"])
        if data_type in ["0x610", "0x620"]:
            ax, ay, az = [random.uniform(0, 5) for _ in range(3)]
            GyroX, GyroY, GyroZ = [random.uniform(0, 1) for _ in range(3)]
            data = [now, data_type, ax, ay, az, GyroX, GyroY, GyroZ, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        elif data_type == "0x630":
            throttle, brake = [random.randint(0, 100) for _ in range(2)]
            data = [now, data_type, None, None, None, None, None, None, throttle, brake, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        elif data_type == "0x640":
            current_sensor = random.uniform(0, 5)
            cell_min_v = random.uniform(2.5, 4.2)
            cell_max_temp = random.uniform(20, 50)
            data = [now, data_type, None, None, None, None, None, None, None, None, current_sensor, cell_min_v, cell_max_temp, None, None, None, None, None, None, None, None, None, None, None]
        elif data_type == "0x650":
            speed = random.uniform(0, 200)
            lat = random.uniform(-90, 90)
            long = random.uniform(-180, 180)
            alt = random.uniform(0, 1000)
            data = [now, data_type, None, None, None, None, None, None, None, None, None, None, None, speed, lat, long, alt, None, None, None, None, None, None, None]
        elif data_type == "0x670":
            FR, FL, RR, RL = [random.uniform(0, 1) for _ in range(4)]
            data = [now, data_type, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, FR, FL, RR, RL, None, None, None]
        elif data_type == "0x660":
            inverter_in, inverter_out, motor_in, motor_out = [random.uniform(0, 5) for _ in range(4)]
            data = [now, data_type, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, inverter_in, inverter_out, motor_in, motor_out]

        with lock:
            all_data.append(data)
            current_data.append(f"{now:%Y-%m-%d %H:%M:%S.%f}: ID: {data_type}")
            if len(current_data) > 100:
                current_data.pop(0)
            data_received = True
        time.sleep(1)

# Function to save data to CSV
def save_data_to_csv(piloto, circuito):
    global csv_filename, start_saving_event, stop_event

    csv_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{piloto}_{circuito}.csv"

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "ID", "ax", "ay", "az", "GyroX", "GyroY", "GyroZ", "throttle", "brake", "current_sensor", "cell_min_v", "cell_max_temp", "speed", "lat", "long", "alt", "FR", "FL", "RR", "RL", "inverter_in", "inverter_out", "motor_in", "motor_out"])

        while not stop_event.is_set():
            if start_saving_event.is_set():
                with lock:
                    while all_data:
                        writer.writerow(all_data.pop(0))
            time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    global stop_event, start_saving_event

    if request.method == 'POST':
        piloto = request.form['piloto']
        circuito = request.form['circuito']
        start_saving_event.set()
        threading.Thread(target=save_data_to_csv, args=(piloto, circuito)).start()
        return render_template('index.html', data_received=data_received, current_data=current_data, piloto=piloto, circuito=circuito)
    return render_template('index.html', data_received=data_received, current_data=current_data, piloto=None, circuito=None)

@app.route('/check_data', methods=['GET'])
def check_data():
    return jsonify({'data_received': data_received, 'current_data': current_data})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_event
    stop_event.set()
    return jsonify({'message': 'Data generation stopped.'})

if __name__ == '__main__':
    threading.Thread(target=generate_random_data).start()
    app.run(host='0.0.0.0', port=5000)
