import argparse
from datetime import datetime
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Funciona con simple_sender_ino.ino
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# A simple NRF24L receiver that connects to a PIGPIO instance on a hostname and port, default "localhost" and 8888, and
# starts receiving data on the address specified.  Use the companion program "simple-sender.py" to send data to it from
# a different Raspberry Pi.
#
if __name__ == "__main__":

    print("Python NRF24 Simple Receiver Example.")
    
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

                # Resolve protocol number.
                protocol = payload[0] if len(payload) > 0 else -1            

                hex = ':'.join(f'{i:02x}' for i in payload)

                # Show message received as hex.
                print(f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}, count: {count}")

                # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                if len(payload) == 32:
                     values = struct.unpack("<ffffffff", payload)
                     
                     dataid = values[0]

                     if dataid == 0x610 : #IMU REAR
                        print(f'ID: {hex(int(values[0]))}, ax: {round(values[1],2)}, ay: {round(values[2],2)}, az: {round(values[3],2)}, GyroX: {round(values[4],2)}, GyroY: {round(values[5],2)}, GyroZ: {round(values[6],2)}')
                     elif dataid == 0x600 : #MOTOR INVERSOR
                        print(f'ID: {hex(int(values[0]))}, motor_temp: {round(values[1],2)}, igbt_temp: {round(values[2],2)}, invertr_temp: {round(values[3],2)}, n_actual: {round(values[4],2)}, dc_bus_voltage: {round(values[5],2)}, i_actual: {round(values[6],2)}, E: {values[7]}') # E es de relleno, por el tamaño fijo
                     elif dataid == 0x630 : #PEDALS
                        print(f'ID: {hex(int(values[0]))}, throttle: {round(values[1],2)}, brake: {round(values[2],2)}')
                     elif dataid == 0x640 : #ACUMULADOR
                        print(f'ID: {hex(int(values[0]))}, current_sensor: {round(values[1],2)}, cell_min_v: {round(values[2],2)}, cell_max_temp: {round(values[3],2)}')
                     elif dataid == 0x650 : #GPS
                        print(f'ID: {hex(int(values[0]))}, speed: {round(values[1],2)}, lat: {round(values[2],2)}, long: {round(values[3],2)},alt: {round(values[3],2)}')
                     elif dataid == 0x670: #SUSPENSION
                        print(f'ID: {hex(int(values[0]))}, FR: {round(values[1],2)}, FL: {round(values[2],2)}, RR: {round(values[3],2)}, RL: {round(values[4],2)}')
                     elif dataid == 0x660: #INVERTER & MOTOR
                        print(f'ID: {hex(int(values[0]))}, inverter_in: {round(values[1],2)}, inverter_out: {round(values[2],2)}, motor_in: {round(values[3],2)}, motor_out: {round(values[4],2)}')
                     # temperatura frenos_ Definir IDs
                     elif dataid == 0x680: #TEMP Frenos
                        print(f'ID: {hex(int(values[0]))}, TFR: {round(values[1],2)}, TFL: {round(values[2],2)}, TRR: {round(values[3],2)}, TRL: {round(values[4],2)}')
                     
                     else: 
                        print(f'ID: {hex(int(values[0]))}')
                         

            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
