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
    rxnrf24(0,0,0)
    for key in keys:
        y = [data[timestamp][key] for timestamp in sorted(data.keys())]
        if key in fig.data:
            fig.data[fig.data.index(key)].y = y
        else:
            fig.add_trace(go.Scatter(x=list(sorted(data.keys())), y=y, mode='lines+markers', name=key))

    fig.update_layout(title=title, xaxis_title='Timestamp', yaxis_title='Value', showlegend=True)


# Recibir arduino e ir actualizando variable global data
def rxnrf24(bucketnever,piloto,circuito):
    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8050, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to listen to (3 to 5 ASCII characters)")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address
    print(address)

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
        

    # As long as data is ready for processing, process it.
    
        # Count message and record time of reception.            
        count += 1
        now = datetime.now()
        
        # Read pipe and payload for message.
        pipe = nrf.data_pipe()
        payload = nrf.get_payload()
        # print(payload) para ver que chuta
        

        # Resolve protocol number.
        id = hex(int(payload[0])) if len(payload) > 0 else -1
        #values = struct.unpack("<ffffffff", payload)
                
        #dataid = values[0]
        #print(f"DataID: {dataid}")
        #print(f"Temperature: {values[1]}")
        #print(f"Humidity: {values[2]}")


        hex_msg = ':'.join(f'{i:02x}' for i in payload)
        print(id)

        print(hex_msg)
        print(len(payload))

        # Show message received as hex.
        #print(f"{now:%Y-%m-%d %H:%M:%S.%f}: ID: {pipe}, len: {len(payload)}, bytes: {hex_msg}, count: {count}")
    

        # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
        # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
        now = datetime.now()

        if len(payload) == 9:
            values = struct.unpack("<Bff", payload)
            measurement={}
            measurement["temperature"] = values[1]
            measurement["humidity"] = values[2]
            data[now]=measurement
            dataid = values[0]
            print(values)
            print(f"DataID: {dataid}")
            print(f"Temperature: {values[1]}")
            print(f"Humidity: {values[2]}")
    except:
            traceback.print_exc()
            nrf.power_down()
            pi.stop()



# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True, port=8889)
    
    


