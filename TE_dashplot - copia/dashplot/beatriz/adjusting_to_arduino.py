################################################################################################
#PRUEBA DASH-ARDUINO REALTIME (Código sin probar) 23 enero 
################################################################################################

# Ver si se puede recibir datos de arduino y graficarlos en tiempo real
# Función basada en python_realtime.py donde he modificado la función rxnrf24 para que reciba los datos de arduino y los almacene en una variable global data
# Callback para actualizar los gráficos en tiempo real y función auxiliar update_figure para actualizar las figuras de líneas
# Interval component está puesto para update cada 1000ms, si funciona, intentar bajarlo. 
# Probablemente habrá que limpiar un poco las librerías importadas que no se usan

import argparse
import time
from datetime import datetime
import pigpio
from nrf24 import *
import dash 
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

import sys
import time
import traceback

import requests

#import keyboard

import time
from datetime import datetime

#Recibir arduino
import argparse
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *


# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Inicializar la variable global data
data = {}


# Inicializar figuras
temperature_fig = go.Figure()
humidity_fig = go.Figure()

# Layout de la aplicación
app.layout = html.Div([

    #Temperature graph 
    dcc.Graph(id='temperature-graph', figure=temperature_fig),

    #Humidity graph
    dcc.Graph(id='humidity-graph', figure=humidity_fig),

    # Interval component para actualizar los gráficos en tiempo real
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Actualizar cada 1 segundo
        n_intervals=0
    )
])

# Callback para actualizar los gráficos
@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n_intervals):
    # Actualizar figuras existentes
    
    # Actualizar figuras de temperatura y humedad
    update_figure(temperature_fig, 'Temperature', ['temperature'])
    update_figure(humidity_fig, 'Humidity', ['humidity'])

    return temperature_fig, humidity_fig


# Función auxiliar para actualizar una figura de líneas
# Recibe la figura, el título y las keys de los datos a mostrar
# Si la figura ya existe, actualiza los datos
# Si no existe, crea una nueva figura



def update_figure(fig, title, keys):
    for key in keys:
        y = [data[timestamp][key] for timestamp in sorted(data.keys())]
        if key in fig.data:
            fig.data[fig.data.index(key)].y = y
        else:
            fig.add_trace(go.Scatter(x=list(sorted(data.keys())), y=y, mode='lines+markers', name=key))

    fig.update_layout(title=title, xaxis_title='Timestamp', yaxis_title='Value', showlegend=True)


# Recibir arduino e ir actualizando variable global data
def rxnrf24(bucketnever,piloto,circuito):
    #? bucketnever, piloto, circuito? not used in this function

    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to listen to (3 to 5 ASCII characters)")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address

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
    # PLEASE NOTE: PA level is set to MIN, because test sender/receivers are often close to each other, and then MIN works better.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    # Listen on the address specified as parameter
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
    
    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    #write_api = client.write_api(write_options=SYNCHRONOUS)

    # Enter a loop receiving data on the address specified.
    try:
        print(f'Receive from {address}')
        count = 0
        while True:

            # As long as data is ready for processing, process it.
            while nrf.data_ready():
                # Count message and record time of reception.            
                count += 1
                now = datetime.now()
                
                # Read pipe and payload for message.
                pipe = nrf.data_pipe()
                payload = nrf.get_payload()

                protocol = payload[0]

                
                hex_msg = ':'.join(f'{i:02x}' for i in payload)

                if len(payload) == 9 and protocol == 0x01:
                    measurement = {}
                    temperature, humidity = struct.unpack("<ff", payload[1:])
                    measurement["temperature"] = temperature    
                    measurement["humidity"] = humidity

                    data[now] = measurement

                else:
                    print('No ID')

                # Resolve protocol number.
                #id = hex(int(payload[0])) if len(payload) > 0 else -1



                #hex_msg = ':'.join(f'{i:02x}' for i in payload)

                # Show message received as hex.
                #print(f"{now:%Y-%m-%d %H:%M:%S.%f}: ID: {pipe}, len: {len(payload)}, bytes: {hex_msg}, count: {count}")
            

                # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                """ if len(payload) == 32:
                            values = struct.unpack("<ffffffff", payload)
                            dataid = values[0]

                            measurement = {}

                            if dataid == 0x610:  # imu rear 
                                measurement['ax_rear'] = round(values[1], 2)
                                measurement['ay_rear'] = round(values[2], 2)
                                measurement['az_rear'] = round(values[3], 2)
                                measurement['wx_rear'] = round(values[4], 2)
                                measurement['wy_rear'] = round(values[5], 2)
                                measurement['wz_rear'] = round(values[6], 2)

                            elif dataid == 0x620:  # imu front
                                measurement['ax_front'] = round(values[1], 2)
                                measurement['ay_front'] = round(values[2], 2)
                                measurement['az_front'] = round(values[3], 2)
                                measurement['wx_front'] = round(values[4], 2)
                                measurement['wy_front'] = round(values[5], 2)
                                measurement['wz_front'] = round(values[6], 2)
                            
                            elif dataid == 0x600:  # motor inversor
                                measurement['motor_temp'] = round(values[1], 2)
                                measurement['igbt_temp'] = round(values[2], 2)
                                measurement['inverter_temp'] = round(values[3], 2)
                                measurement['n_actual'] = round(values[4], 2)
                                measurement['dc_bus_voltage'] = round(values[5], 2)
                                measurement['i_actual'] = round(values[6], 2)

                            elif dataid == 0x630:  # pedals
                                measurement['throttle'] = round(values[1], 2)
                                measurement['brake'] = round(values[2], 2)
                            
                            elif dataid == 0x640:  # acumulador
                                measurement['current_sensor'] = round(values[1], 2)
                                measurement['cell_min_v'] = round(values[2], 2)
                                measurement['cell_max_temp'] = round(values[3], 2)
                            
                            #elif dataid == 0x650:  # gps
                              #  measurement['speed'] = round(values[1], 2)
                              #  measurement['lat'] = round(values[2], 2)
                              #  measurement['long'] = round(values[3], 2)
                              #  measurement['alt'] = round(values[4], 2)
                            
                            else:
                                print('No ID') """

                            # Update the data with the measurement for the current timestamp
                            #data[now] = measurement
                               
            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()



# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)


