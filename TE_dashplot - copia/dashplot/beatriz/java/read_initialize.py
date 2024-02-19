# Function to read the data (UNSUSED porque no me funcionaban los directorios.)
import argparse
import struct
import sys
import time
import traceback
import nrf24
from nrf24 import *
import pigpio
from datetime import datetime



#FUNCTION TO INITIALIZE THE NRF24L01 - ONLY TO BE RUN ONCE 
def initialize():
    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
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
                return (dataid, temperature, humidity)

    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

    # If no data was ready, return None
    return None

import random 

def read_data_simulation():
    # Simulate temperature and humidity values
    id= 1
    temperature = random.uniform(20.0, 30.0)  # Random float between 20.0 and 30.0
    humidity = random.uniform(30.0, 60.0)  # Random float between 30.0 and 60.0

    return {
        'id': id,
        'temperature': temperature,
        'humidity': humidity
    }