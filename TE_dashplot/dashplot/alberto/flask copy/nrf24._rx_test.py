import pigpio
from nrf24 import *
import time

# Initialize the pigpio library
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio")
    exit()

# Define the CE and IRQ pins
CE_PIN = 25


# Initialize the NRF24 module

nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_2MBPS, pa_level=RF24_PA.MIN)# MIN

# Set the RX and TX addresses
address = [0xE7, 0xE7, 0xE7, 0xE7, 0xE7]
nrf.set_address_bytes(len(address)) 

# Configure RX pipes
nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)

nrf.show_registers()

# Function to receive data
def receive_data():
    if nrf.data_ready():
        pipe = nrf.data_pipe()
        payload = nrf.get_payload()
        print(f"Received data on pipe {pipe}: {payload}")

try:
    print("Raspberry Pi NRF24 Receiver is online.")
    print(f'Receive from {address}')
    while True:
        receive_data()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    nrf.power_down()
    pi.stop()
