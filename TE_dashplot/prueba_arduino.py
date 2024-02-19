#Recibir arduino
import argparse
import struct
import sys
import time
import traceback
from nrf24 import *
import pigpio
import influxdb_client
from datetime import datetime

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
            if len(payload) == 9:
                values = struct.unpack("<Bff", payload)
                    
                dataid = values[0]
                print(values)
                print(f"DataID: {dataid}")
                print(f"Temperature: {values[1]}")
                print(f"Humidity: {values[2]}")
except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()