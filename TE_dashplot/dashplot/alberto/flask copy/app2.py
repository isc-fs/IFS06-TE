from gevent import monkey
monkey.patch_all()
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

# Para compatibilidad con websocckets



'''
Funciona al menos con los datos simulados, abrir http://localhost:5000/
'''

# Clase para simular la llegada de paquetes con distintos dataids de forma uniforme y secuencial
class DataIDIterator:
    def __init__(self, values):
        self.values = values
        self.index = 0

    def get_next(self):
        value = self.values[self.index]
        self.index = (self.index + 1) % len(self.values)
        return value

# Lista de valores
values = [0x600, 0x610, 0x630, 0x640, 0x650, 0x660, 0x670, 0x680]

# Crear instancia del iterador
dataid_iterator = DataIDIterator(values)

#Funcion para simular datos (sin uso de arduino)
def read_data_simulation():

    # Obtener el siguiente valor secuencialmente:
    dataid = dataid_iterator.get_next()

    # Forma para hacerlo aleatoriamente:
    # dataid = random.choice([0x600, 0x610, 0x630, 0x640, 0x650, 0x660, 0x670, 0x680])

    if dataid == 0x610 : #IMU REAR
        values = [random.randint(0, 100) for _ in range(7)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2), round(values[5],2), round(values[6],2))
    elif dataid == 0x600 : #MOTOR INVERSOR
        values = [random.randint(0, 100) for _ in range(8)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2), round(values[5],2), round(values[6],2), values[7])  
    elif dataid == 0x630 : #PEDALS
        values = [random.randint(0, 100) for _ in range(3)]   
        return (dataid, round(values[1],2), round(values[2],2))
    elif dataid == 0x640 : #ACUMULADOR
        values = [random.randint(0, 100) for _ in range(4)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2))
    elif dataid == 0x650 : #GPS
        values = [random.randint(0, 100) for _ in range(5)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
    elif dataid == 0x670: #SUSPENSION
        values = [random.randint(0, 100) for _ in range(5)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
    elif dataid == 0x660: #INVERTER & MOTOR
        values = [random.randint(0, 100) for _ in range(5)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
    # temperatura frenos_ Definir IDs
    elif dataid == 0x680: #TEMP Frenos
        values = [random.randint(0, 100) for _ in range(5)]
        return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
    else: 
        values = [random.randint(0, 100) for _ in range(1)]
        print(f'ID: {hex(int(values[0]))}')
        return (dataid)
    # Return the data as a tuple

#FUNCTION TO INITIALIZE THE NRF24L01 - ONLY TO BE RUN ONCE 
def initialize():
    # Parse command line argument.
    # hostname = 'localhost'
    # port = 8888
    address = [0xE7, 0xE7, 0xE7, 0xE7, 0xE7]
    print('Initializing...')
    # Verify that address is between 3 and 5 characters.
    #if not (2 < len(address) < 6):
    #    print(f'Invalid address {address}. Addresses must be between 3 and 5 ASCII characters.')
    #    sys.exit(1)

    # Connect to pigpiod
    # Initialize the pigpio library
    pi = pigpio.pi()
    if not pi.connected:
        print("Could not connect to pigpio")
        exit()
    print('Connected to pigpio correctly')
    #print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    #pi = pigpio.pi(hostname, port)
    print(f'Initializing nrf24 for address: {address} (length:{len(address)})')

    # Create NRF24 object.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_2MBPS, pa_level=RF24_PA.MIN)
    # Set the RX and TX addresses
    nrf.set_address_bytes(len(address)) 
    
    # Listen on the address specified as parameter
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    return nrf, address

count = 0
#FUNCTION TO READ THE DATA
def read_data(nrf, address):
    try:
        print(f'Receive from {address}')
        if nrf.data_ready():
            pipe = nrf.data_pipe()
            payload = nrf.get_payload()
            print(f"Received data on pipe {pipe}: {payload}")
            data = payload
        '''
        # As long as data is ready for processing, process it.
        if nrf.data_ready():
            # Count message and record time of reception.            
            count += 1
            now = datetime.now()
            print(count)
            # Read pipe and payload for message.
            pipe = nrf.data_pipe()
            payload = nrf.get_payload()
            print(f"Received data on pipe {pipe}: {payload}")

            #print(len(payload))
            #print(payload)

            # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
            # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
            if len(payload) == 32:
                values = struct.unpack("<Ifffffff", payload)
                #print(f'Received payload: {payload.hex()}')  # Debugging print
                # dataid_hex = format(int("".join(map(str, values[:4]))), 'x')  # Join elements and convert to hex
                #print(dataid_hex)
                print(values[0])
                #print(values)
                #print(type(values[0]))
                dataid = values[0]
            
                if dataid == 0x610 : #IMU REAR
                    print(f'ID: {hex(int(values[0]))}, ax: {round(values[1],2)}, ay: {round(values[2],2)}, az: {round(values[3],2)}, GyroX: {round(values[4],2)}, GyroY: {round(values[5],2)}, GyroZ: {round(values[6],2)}')
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2), round(values[5],2), round(values[6],2))
                elif dataid == 0x600 : #MOTOR INVERSOR
                    print(f'ID: {hex(int(values[0]))}, motor_temp: {round(values[1],2)}, igbt_temp: {round(values[2],2)}, inverter_temp: {round(values[3],2)}, n_actual: {round(values[4],2)}, dc_bus_voltage: {round(values[5],2)}, i_actual: {round(values[6],2)}, E: {values[7]}') # E es de relleno, por el tamaño fijo
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2), round(values[5],2), round(values[6],2), values[7])  
                elif dataid == 0x630 : #PEDALS
                    print(f'ID: {hex(int(values[0]))}, throttle: {round(values[1],2)}, brake: {round(values[2],2)}')
                    return (dataid, round(values[1],2), round(values[2],2))
                elif dataid == 0x640 : #ACUMULADOR
                    print(f'ID: {hex(int(values[0]))}, current_sensor: {round(values[1],2)}, cell_min_v: {round(values[2],2)}, cell_max_temp: {round(values[3],2)}')
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2))
                elif dataid == 0x650 : #GPS
                    print(f'ID: {hex(int(values[0]))}, speed: {round(values[1],2)}, lat: {round(values[2],2)}, long: {round(values[3],2)},alt: {round(values[4],2)}')
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
                elif dataid == 0x670: #SUSPENSION
                    print(f'ID: {hex(int(values[0]))}, FR: {round(values[1],2)}, FL: {round(values[2],2)}, RR: {round(values[3],2)}, RL: {round(values[4],2)}')
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
                elif dataid == 0x660: #INVERTER & MOTOR
                    print(f'ID: {hex(int(values[0]))}, inverter_in: {round(values[1],2)}, inverter_out: {round(values[2],2)}, motor_in: {round(values[3],2)}, motor_out: {round(values[4],2)}')
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
                # temperatura frenos_ Definir IDs
                elif dataid == 0x680: #TEMP Frenos
                    print(f'ID: {hex(int(values[0]))}, TFR: {round(values[1],2)}, TFL: {round(values[2],2)}, TRR: {round(values[3],2)}, TRL: {round(values[4],2)}')
                    return (dataid, round(values[1],2), round(values[2],2), round(values[3],2), round(values[4],2))
                else: 
                    print(f'ID: {hex(int(values[0]))}')
                    return (dataid)
                # Return the data as a tuple
           
    '''
    except:
        traceback.print_exc()
        nrf.power_down()
    finally:
        nrf.power_down()
        

    # If no data was ready, return None
    return None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent') 

#!!!!! Uncomment la linea cuando esté la raspberry conectada. 

import time 
import math

def read_loop():

    #nrf, address = initialize() # !! uncomment this line when the raspberry is connected
    #Initialize the pigpio library
    pi = pigpio.pi()

    if not pi.connected:
        print("Could not connect to pigpio")
        exit()

    # Define the CE and IRQ pins
    CE_PIN = 25
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_2MBPS, pa_level=RF24_PA.MIN)
    # Set the RX and TX addresses
    address = [0xE7, 0xE7, 0xE7, 0xE7, 0xE7]
    nrf.set_address_bytes(len(address)) 

    # Configure RX pipes
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

    nrf.show_registers()
    while True:
        #data = read_data_simulation() 
        try: 
            if nrf.data_ready():
                pipe = nrf.data_pipe()
                data = nrf.get_payload()
                print(f"Received data on pipe {pipe}: {data}")

                
                if data is not None:
                    #get element 0 of the tuple data 
                    dataid = data[0]
                    if dataid == 0x610 : #IMU REAR
                        #print(f'ID: {hex(int(data[0]))}, ax: {round(data[1],2)}, ay: {round(data[2],2)}, az: {round(data[3],2)}, GyroX: {round(data[4],2)}, GyroY: {round(data[5],2)}, GyroZ: {round(data[6],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'ax': round(data[1],2), 'ay': round(data[2],2), 'az': round(data[3],2), 'GyroX': round(data[4],2), 'GyroY': round(data[5],2), 'GyroZ': round(data[6],2)})
                    elif dataid == 0x600 : #MOTOR INVERSOR
                        #print(f'ID: {hex(int(data[0]))}, motor_temp: {round(data[1],2)}, igbt_temp: {round(data[2],2)}, inverter_temp: {round(data[3],2)}, n_actual: {round(data[4],2)}, dc_bus_voltage: {round(data[5],2)}, i_actual: {round(data[6],2)}, E: {data[7]}') # E es de relleno, por el tamaño fijo
                        socketio.emit('newdata', {'dataid': dataid, 'motor_temp': round(data[1],2), 'igbt_temp': round(data[2],2), 'inverter_temp': round(data[3],2), 'n_actual': round(data[4],2), 'dc_bus_voltage': round(data[5],2), 'i_actual': round(data[6],2), 'E': data[7]})
                    elif dataid == 0x630 : #PEDALS
                        #print(f'ID: {hex(int(data[0]))}, throttle: {round(data[1],2)}, brake: {round(data[2],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'throttle': round(data[1],2), 'brake': round(data[2],2)})
                    elif dataid == 0x640 : #ACUMULADOR
                        #print(f'ID: {hex(int(data[0]))}, current_sensor: {round(data[1],2)}, cell_min_v: {round(data[2],2)}, cell_max_temp: {round(data[3],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'current_sensor': round(data[1],2), 'cell_min_v': round(data[2],2), 'cell_max_temp': round(data[3],2)})
                    elif dataid == 0x650 : #GPS
                        #print(f'ID: {hex(int(data[0]))}, speed: {round(data[1],2)}, lat: {round(data[2],2)}, long: {round(data[3],2)},alt: {round(data[4],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'speed': round(data[1],2), 'lat': round(data[2],2), 'long': round(data[3],2), 'alt': round(data[4],2)})
                    elif dataid == 0x670: #SUSPENSION
                        #print(f'ID: {hex(int(data[0]))}, FR: {round(data[1],2)}, FL: {round(data[2],2)}, RR: {round(data[3],2)}, RL: {round(data[4],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'FR': round(data[1],2), 'FL': round(data[2],2), 'RR': round(data[3],2), 'RL': round(data[4],2)})
                    elif dataid == 0x660: #INVERTER & MOTOR
                        #print(f'ID: {hex(int(data[0]))}, inverter_in: {round(data[1],2)}, inverter_out: {round(data[2],2)}, motor_in: {round(data[3],2)}, motor_out: {round(data[4],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'inverter_in': round(data[1],2), 'inverter_out': round(data[2],2), 'motor_in': round(data[3],2), 'motor_out': round(data[4],2)})
                    # temperatura frenos_ Definir IDs
                    elif dataid == 0x680: #TEMP Frenos
                        #print(f'ID: {hex(int(data[0]))}, TFR: {round(data[1],2)}, TFL: {round(data[2],2)}, TRR: {round(data[3],2)}, TRL: {round(data[4],2)}')
                        socketio.emit('newdata', {'dataid': dataid, 'TFR': round(data[1],2), 'TFL': round(data[2],2), 'TRR': round(data[3],2), 'TRL': round(data[4],2)})
                    else: 
                        print(f'DATA WITH ID: {hex(int(data[0]))} NOT SENT')
                        return (dataid)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            nrf.power_down()
            pi.stop()

        time.sleep(0.1)

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
    print('Click on http://localhost:5000/')
    try:
        socketio.run(app, port=5000, host='localhost')
    except KeyboardInterrupt:
        print("Exiting...")
