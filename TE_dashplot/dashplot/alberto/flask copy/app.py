import pigpio
from nrf24 import *
import time
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import struct

# Inicializa la biblioteca pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio")
    exit()

# Define los pines CE e IRQ
CE_PIN = 25

# Inicializa el módulo NRF24
nrf = NRF24(pi, ce=CE_PIN, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_2MBPS, pa_level=RF24_PA.MIN)

# Establece las direcciones RX y TX
address = [0xE7, 0xE7, 0xE7, 0xE7, 0xE7]
nrf.set_address_bytes(len(address))

# Configura las tuberías RX
nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

nrf.show_registers()
def emit_data(values):
    data = values
    dataid = data[0]
    if dataid == 0x610 : #IMU REAR
        print(f'ID: {hex(int(data[0]))}, ax: {round(data[1],2)}, ay: {round(data[2],2)}, az: {round(data[3],2)}, GyroX: {round(data[4],2)}, GyroY: {round(data[5],2)}, GyroZ: {round(data[6],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'ax': round(data[1],2), 'ay': round(data[2],2), 'az': round(data[3],2), 'GyroX': round(data[4],2), 'GyroY': round(data[5],2), 'GyroZ': round(data[6],2)})
    elif dataid == 0x600 : #MOTOR INVERSOR
        print(f'ID: {hex(int(data[0]))}, motor_temp: {round(data[1],2)}, igbt_temp: {round(data[2],2)}, inverter_temp: {round(data[3],2)}, n_actual: {round(data[4],2)}, dc_bus_voltage: {round(data[5],2)}, i_actual: {round(data[6],2)}, E: {data[7]}') # E es de relleno, por el tamaño fijo
        socketio.emit('newdata', {'dataid': dataid, 'motor_temp': round(data[1],2), 'igbt_temp': round(data[2],2), 'inverter_temp': round(data[3],2), 'n_actual': round(data[4],2), 'dc_bus_voltage': round(data[5],2), 'i_actual': round(data[6],2), 'E': data[7]})
    elif dataid == 0x630 : #PEDALS
        print(f'ID: {hex(int(data[0]))}, throttle: {round(data[1],2)}, brake: {round(data[2],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'throttle': round(data[1],2), 'brake': round(data[2],2)})
    elif dataid == 0x640 : #ACUMULADOR
        print(f'ID: {hex(int(data[0]))}, current_sensor: {round(data[1],2)}, cell_min_v: {round(data[2],2)}, cell_max_temp: {round(data[3],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'current_sensor': round(data[1],2), 'cell_min_v': round(data[2],2), 'cell_max_temp': round(data[3],2)})
    elif dataid == 0x650 : #GPS
        print(f'ID: {hex(int(data[0]))}, speed: {round(data[1],2)}, lat: {round(data[2],2)}, long: {round(data[3],2)},alt: {round(data[4],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'speed': round(data[1],2), 'lat': round(data[2],2), 'long': round(data[3],2), 'alt': round(data[4],2)})
    elif dataid == 0x670: #SUSPENSION
        print(f'ID: {hex(int(data[0]))}, FR: {round(data[1],2)}, FL: {round(data[2],2)}, RR: {round(data[3],2)}, RL: {round(data[4],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'FR': round(data[1],2), 'FL': round(data[2],2), 'RR': round(data[3],2), 'RL': round(data[4],2)})
    elif dataid == 0x660: #INVERTER & MOTOR
        print(f'ID: {hex(int(data[0]))}, inverter_in: {round(data[1],2)}, inverter_out: {round(data[2],2)}, motor_in: {round(data[3],2)}, motor_out: {round(data[4],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'inverter_in': round(data[1],2), 'inverter_out': round(data[2],2), 'motor_in': round(data[3],2), 'motor_out': round(data[4],2)})
    # temperatura frenos_ Definir IDs
    elif dataid == 0x680: #TEMP Frenos
        print(f'ID: {hex(int(data[0]))}, TFR: {round(data[1],2)}, TFL: {round(data[2],2)}, TRR: {round(data[3],2)}, TRL: {round(data[4],2)}')
        socketio.emit('newdata', {'dataid': dataid, 'TFR': round(data[1],2), 'TFL': round(data[2],2), 'TRR': round(data[3],2), 'TRL': round(data[4],2)})
    else: 
        print(f'DATA WITH ID: {hex(int(data[0]))} NOT SENT')
        #return (dataid)
    # Return the data as a tuple

# Función para recibir datos
def receive_data():
    if nrf.data_ready():
        pipe = nrf.data_pipe()
        payload = nrf.get_payload()
        #print(f"Datos recibidos en la tubería {pipe}: {payload}")
        return payload
    return None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Ruta principal   
@app.route('/')
def index():
    return render_template('index.html')

# Función para leer los datos del NRF24L01 y enviarlos a través de socketio
def read_loop():
    print("Receptor NRF24 de Raspberry Pi está en línea.")
    print(f'Recibiendo de {address}')
    try:
        while True:
            data = receive_data()
            if data:
                values = struct.unpack('8f', data)
                #print(values)
                emit_data(values)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Saliendo...")
    finally:
        nrf.power_down()
        pi.stop()

# Cuando un cliente se conecta, se inicia un hilo que lee los datos del NRF24L01 y los envía a través de socketio
@socketio.on('connect')
def test_connect():
    threading.Thread(target=read_loop).start()

# Inicia el servidor
if __name__ == '__main__':
    print('Ve a http://localhost:5000/')
    try:
        socketio.run(app, port=5000, host='0.0.0.0')
    except KeyboardInterrupt:
        print("Saliendo...")
