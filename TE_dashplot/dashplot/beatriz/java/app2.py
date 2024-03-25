from flask import Flask, render_template
from flask_socketio import SocketIO, emit
#from dashplot.beatriz.java.read_initialize import initialize, read_data, read_data_simulation
import threading

import random 

# Function to read the data 
import argparse
import struct
import sys
import time
import traceback
import nrf24
from nrf24 import *
import pigpio
from datetime import datetime
#Estas funciones deberían estar en un archivo aparte, pero me da error . 

#Esta se inventa datos. 
def read_data_simulation():
    # Simulate temperature and humidity values
    id= 1
    temperature = random.uniform(2.0, 3.0)  # Random float between 20.0 and 30.0
    humidity = random.uniform(3.0, 6.0)  # Random float between 30.0 and 60.0
    pressure = random.uniform(3.0, 6.0)
    dc_bus_voltage = random.uniform(3.0, 6.0)
    i_actual = random.uniform(3.0, 6.0)
    igbt_temp = random.uniform(3.0, 6.0)
    inverter_temp = random.uniform(3.0, 6.0)
    motor_temp = random.uniform(3.0, 6.0)
    n_actual = random.uniform(3.0, 6.0)
    ax = random.uniform(3.0, 6.0)
    ay = random.uniform(3.0, 6.0)
    az = random.uniform(3.0, 6.0)
    brake = random.uniform(3.0, 6.0)
    throttle = random.uniform(3.0, 6.0)
    inverter_temp = random.uniform(3.0, 6.0)
    suspension_fr = random.uniform(3.0, 6.0)
    suspension_fl = random.uniform(3.0, 6.0)
    suspension_rr = random.uniform(3.0, 6.0)
    suspension_rl = random.uniform(3.0, 6.0)



    return id, temperature, humidity, pressure, dc_bus_voltage, i_actual, igbt_temp, inverter_temp, motor_temp, n_actual, ax, ay, az, brake, throttle, inverter_temp, suspension_fr, suspension_fl, suspension_rr, suspension_rl

#FUNCTION TO INITIALIZE THE NRF24L01 - ONLY TO BE RUN ONCE 
def initialize():
    # Parse command line argument.
    hostname = 'localhost'
    port = 8888
    address = '1SNSR'

    # Verify that address is between 3 and 5 characters.
    if not (2 < len(address) < 6):
        print(f'Invalid address {address}. Addresses must be between 3 and 5 ASCII characters.')
        sys.exit(1)

    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    # Create NRF24 object.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    # Listen on the address specified as parameter
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    return nrf, address


#FUNCTION TO READ THE DATA
def read_data(nrf, address):
    try:
        print(f'Receive from {address}')
        count = 0

        # As long as data is ready for processing, process it.
        if nrf.data_ready():
            # Count message and record time of reception.            
            count += 1
            now = datetime.now()

            # Read pipe and payload for message.
            pipe = nrf.data_pipe()
            payload = nrf.get_payload()

            # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
            # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
            if len(payload) == 9:
                values = struct.unpack("<Bff", payload)

                dataid = values[0]
                temperature = values[1]
                humidity = values[2]

                # Return the data as a tuple
                return (dataid, temperature, humidity) #TUPLA

    except:
        traceback.print_exc()
        nrf.power_down()
        

    # If no data was ready, return None
    return None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

#!!!!! Uncomment la linea cuando esté la raspberry conectada. 

import time 
import math

def read_loop():
    #nrf, address = initialize() !! uncomment this line when the raspberry is connected
    while True:
        data = read_data_simulation()#!!!! Aquí debería ir read_data(nrf, address) cuando tengamos la raspberry conectada
        print(data)
        if data is not None:
            #get element 0 of the tuple data 
            dataid = data[0]
            temperature = data[1]
            humidity = data[2]
            pressure = data[3]
            dc_bus_voltage = data[4]
            i_actual = data[5]
            igbt_temp = data[6]
            inverter_temp = data[7]
            motor_temp = data[8]
            n_actual = data[9]
            ax = data[10]
            ay = data[11]
            az = data[12]
            brake = data[13]
            throttle = data[14]
            laquefalta = data[15]
            suspension_FR= data[16]
            suspension_FL = data[17]
            suspension_RR = data[18]
            suspension_RL = data[19]

            #print(type(temperature))
            
            socketio.emit('newdata', {'dataid': dataid, 'temperature': temperature, 'humidity': humidity, 'pressure': pressure, 'dc_bus_voltage': dc_bus_voltage, 'i_actual': i_actual, 'igbt_temp': igbt_temp, 'laquefalta': laquefalta, 'motor_temp': motor_temp, 'n_actual': n_actual, 'ax': ax, 'ay': ay, 'az': az, 'brake': brake, 'throttle': throttle, 'inverter_temp': inverter_temp, 'suspension_FR': suspension_FR, 'suspension_FL': suspension_FL, 'suspension_RR': suspension_RR, 'suspension_RL': suspension_RL})
        time.sleep(2)

#Ruta principal   
@app.route('/')
def index():
    return render_template('index.html')

#Cuando un cliente se conecta, se inicia un hilo que lee los datos del NRF24L01 y los envía a través de socketio
@socketio.on('connect')
def test_connect():
    threading.Thread(target=read_loop).start()

# Inicia el servidor
if __name__ == '__main__':
    socketio.run(app, port=5000, host='localhost')
