from ast import NotIn
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import requests

import keyboard

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






COM = "COM4"
bucket = "e0e3f2d24fd93e79"

client = InfluxDBClient(url="http://localhost:8086",
                        token="sNZJlQsv2KhY28xPDZBmt2HbgGtwU5AE4vUjQsks9WPm3o0g_UreLkxNVgMHNotIqUMHCcgAyN4llUvdXs4QtA==",
                       org="b2b03940375e28ac")




def writedatatxt(bucketnever,piloto,circuito):

    f = open("C:/Users/fadri/Desktop/Coche/pruebalargo3.txt","r")
    fdata = f.readlines()
    f.close()

    count = 0
    end = False
    while not end:
        for i in fdata:

            if keyboard.is_pressed("right shift"):
            #if keyboard.read_key() == "right shift":
                 print("\nPrograma terminado")
                 end = True
                 break

            count = count + 1
            #print(count)

            write_api = client.write_api(write_options=SYNCHRONOUS)

            #timestamp = datetime.strptime(timestamp, '%H:%M:%S.%f')  No te pone una fecha (o si pero de hace mil años?)
            timest = i.split(" -> ")[0]
            test = datetime.now()
            testtime = str(test.strftime("%Y-%m-%d"))+" "+ timest
            FStime = datetime.strptime(testtime,"%Y-%m-%d %H:%M:%S.%f")

            #int(FStime.timestamp()*1000) esto convierte datetime en timestamp
            FStimets = int(FStime.timestamp())


            dataid = i.split(" -> ")[1].split(",")[0]
            char = i.split(" -> ")[1].split(",")
            num1 = int(char[2])
            num2 = int(char[3].replace("\n",""))


            data = (num1 << 8) + num2
            #data = (data - 10367) / 48.169
            #Esto da error, al introducir decimales en .field()
            #Este calculo se puede hacer directamente en Grafana/Influx

            if dataid == "0x303": # T Aire
                #print("dataid - ",dataid," // data - ",num1,",",num2," // FStime - ",FStime.isoformat())
                data = (data - 10367.0) / 48.169
                #.isoformat convierte el datetime a cierto formato
            elif dataid == "0x301": # T Motor
                data = (data - 9452.4) / 52.33
            elif dataid == "0x302": # T IGBT
                data = (data - 17621.0) / 84.043
            elif dataid == "0x304": # Velocidad Motor
                data = (data*6000) / 32767.0


            #check = ser.readline().decode()
            #check = check.replace(" ","")
            #print(check)

            p = Point(dataid).field("data",data)
            #p = Point("0x1234").field("data",check)

            write_api.write(bucket=bucketnever, record=p)
            write_api.write(bucket=bucket, record=p)

            writerundata(piloto,circuito)

            #mmmm no va / el problema es el .time  // no me queda claro si necesita un formato especial o que
            #Dejando que influx ponga automaticamente el timestamp funciona bien,
            #pero los tiempos dependen de la velocidad a la que se introducen los datos?


            #InfluxDB con solo la hora no es capaz de detectarlo?
            #Añadir a los datos la fecha


            write_api.close()

            #Esto esta para probar, eliminar para ver datos de verdad
            #Con 0.02 se acerca bastante a los tiempos en los .txt
            time.sleep(0.023)


def writedatatxtsints(bucketnever,bucket,piloto,circuito):

    f = open("pruebaicade.txt","r")
    fdata = f.readlines()
    f.close()
    idlist = []
    count = 0
    end = False
    while not end:
        for i in fdata:


            count = count + 1
            #print(count)

            if i == "empty\n":
                #print(" ")
                pass
            elif i == "nRF24: inicializacion correcta\n":
                #print("nRF24: inicializacion correcta")
                pass
            else:
                test = datetime.now()
                #print(test.strftime("%H:%M:%S.%f"), "-> ",i)

                write_api = client.write_api(write_options=SYNCHRONOUS)


                dataid = i.split(",")[0]
                num1 = int(i.split(",")[2])
                num2 = int(i.split(",")[3])

                if dataid not in idlist:
                    print("new id")
                    idlist.append(dataid)


                data = (num1 << 8) + num2



                if dataid == "0x303": # T Aire
                    #print("dataid - ",dataid," // data - ",num1,",",num2," // FStime - ",FStime.isoformat())
                    data = (data - 10367.0) / 48.169
                    #.isoformat convierte el datetime a cierto formato
                elif dataid == "0x301": # T Motor
                    data = (data - 9452.4) / 52.33
                elif dataid == "0x302": # T IGBT
                    data = (data - 17621.0) / 84.043
                elif dataid == "0x304": # Velocidad Motor
                    data = (data*6000) / 32767.0


                #check = ser.readline().decode()
                #check = check.replace(" ","")
                #print(check)
                print('Point')
                p = Point(dataid).field("data",data)
                #p = Point("0x1234").field("data",check)
                print('bucketnever')
                write_api.write(bucket=bucketnever, record=p)
                print('bucket')
                write_api.write(bucket=bucket, record=p)
                print('writerundata')
                writerundata(bucketnever,bucket,piloto,circuito)

                #mmmm no va / el problema es el .time  // no me queda claro si necesita un formato especial o que
                #Dejando que influx ponga automaticamente el timestamp funciona bien,
                #pero los tiempos dependen de la velocidad a la que se introducen los datos?


                #InfluxDB con solo la hora no es capaz de detectarlo?
                #Añadir a los datos la fecha


                write_api.close()

                #Esto esta para probar, eliminar para ver datos de verdad
                #Con 0.02 se acerca bastante a los tiempos en los .txt
            time.sleep(0.023)


def rxnrf24(bucketnever,piloto,circuito):
    
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

    write_api = client.write_api(write_options=SYNCHRONOUS)

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
                id = hex(int(payload[0])) if len(payload) > 0 else -1



                hex_msg = ':'.join(f'{i:02x}' for i in payload)

                # Show message received as hex.
                # print(f"{now:%Y-%m-%d %H:%M:%S.%f}: ID: {pipe}, len: {len(payload)}, bytes: {hex_msg}, count: {count}")
            

                # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                if len(payload) == 32:
                     values = struct.unpack("<ffffffff", payload)
                     
                     dataid = values[0]

                     if dataid == 0x610 : #IMU REAR
                        print(f'ID: {hex(int(values[0]))}, ax: {round(values[1],2)}, ay: {round(values[2],2)}, az: {round(values[3],2)}, GyroX: {round(values[4],2)}, GyroY: {round(values[5],2)}, GyroZ: {round(values[6],2)}')
                        p = Point("0x610").field("ax",values[1]).field("ay",values[2]).field("az",values[3]).field("wx",values[4]).field("wy",values[5]).field("wz",values[6])
                     elif dataid == 0x620 : #IMU FRONT
                        print(f'ID: {hex(int(values[0]))}, ax: {round(values[1],2)}, ay: {round(values[2],2)}, az: {round(values[3],2)}, GyroX: {round(values[4],2)}, GyroY: {round(values[5],2)}, GyroZ: {round(values[6],2)}, E: {values[7]}')
                        p = Point("0x620").field("ax",values[1]).field("ay",values[2]).field("az",values[3]).field("wx",values[4]).field("wy",values[5]).field("wz",values[6])
                     elif dataid == 0x600 : #MOTOR INVERSOR
                        print(f'ID: {hex(int(values[0]))}, motor_temp: {round(values[1],2)}, igbt_temp: {round(values[2],2)}, invertr_temp: {round(values[3],2)}, n_actual: {round(values[4],2)}, dc_bus_voltage: {round(values[5],2)}, i_actual: {round(values[6],2)}, E: {values[7]}')
                        p = Point("0x600").field("motor_temp",values[1]).field("igbt_temp",values[2]).field("inverter_temp",values[3]).field("n_actual",values[4]).field("dc_bus_voltage",values[5]).field("i_actual",values[6])
                     elif dataid == 0x630 : #PEDALS
                        print(f'ID: {hex(int(values[0]))}, throttle: {round(values[1],2)}, brake: {round(values[2],2)}')
                        p = Point("0x630").field("throttle",values[1]).field("brake",values[2])
                     elif dataid == 0x640 : #ACUMULADOR
                        print(f'ID: {hex(int(values[0]))}, current_sensor: {round(values[1],2)}, cell_min_v: {round(values[2],2)}, cell_max_temp: {round(values[3],2)}')
                        p = Point("0x640").field("current_sensor",values[1]).field("cell_min_v",values[2]).field("cell_max_temp",values[3])
                     elif dataid == 0x650 : #GPS
                        print(f'ID: {hex(int(values[0]))}, speed: {round(values[1],2)}, lat: {round(values[2],2)}, long: {round(values[3],2)},alt: {round(values[3],2)}')
                        p = Point("0x650").field("speed",values[1]).field("lat",values[2]).field("long",values[3]).field("alt",values[3])
                     elif dataid == 0x670:
                        print(f'ID: {hex(int(values[0]))}, FR: {round(values[1],2)}, FL: {round(values[2],2)}, RR: {round(values[3],2)}, RL: {round(values[4],2)}')
                        p = Point("0x670").field("Suspension_FR",values[1]).field("Suspension_FL",values[2]).field("Suspension_RR",values[3]).field("Suspension_RL",values[4])
                     elif dataid == 0x660:
                        print(f'ID: {hex(int(values[0]))}, inverter_in: {round(values[1],2)}, inverter_out: {round(values[2],2)}, motor_in: {round(values[3],2)}, motor_out: {round(values[4],2)}')
                        p = Point("0x660").field("Inverter_inlet",values[1]).field("Inverter_outlet",values[2]).field("Motor_inlet",values[3]).field("Motor_outlet",values[4])
                     else: 
                        print(f'ID: {hex(int(values[0]))}')
                         

                write_api.write(bucket=bucketnever, record=p)
                write_api.write(bucket=bucket, record=p)
                writerundata(bucketnever,bucket,piloto,circuito)


                  
                         

                        
                                   


            # Sleep 100 ms.
            #time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()


def writerundata(bucketnever,bucket,piloto,circuito):
    write_api = client.write_api(write_options=SYNCHRONOUS)


    p = Point("piloto").field("data",piloto)
    write_api.write(bucket=bucketnever, record=p)
    write_api.write(bucket=bucket, record=p)


    p = Point("circuito").field("data",circuito)
    write_api.write(bucket=bucketnever, record=p)
    write_api.write(bucket=bucket, record=p)


def rundata():


    piloto = input("Introducir el nombre del piloto: ")
    circuito = input("Introducir el nombre del circuito: ")

    return piloto,circuito



def createbucket(piloto,circuito):
    headers = {'Authorization': 'Token sNZJlQsv2KhY28xPDZBmt2HbgGtwU5AE4vUjQsks9WPm3o0g_UreLkxNVgMHNotIqUMHCcgAyN4llUvdXs4QtA=='}
    url = "http://localhost:8086/api/v2/buckets"
    payloadtemp = {
    "orgID": "b2b03940375e28ac",
    "name": "ISC",
    "description": "create a bucket",
    "rp": "myrp",
    "retentionRules":[
    {
    "type": "expire",
    "everySeconds": 86400
    }
    ]
    }

    test = datetime.now()
    time = test.strftime("%Y-%m-%d %H:%M:%S")
    print(time)

    payloadnever = {
    "orgID": "b2b03940375e28ac",
    "name": time+" |> FS-"+circuito+"-"+piloto,
    "description": "create a bucket",
    "rp": "myrp",
    "duration":"INF"
    }

    # "type": "expire","everySeconds": 86400 // es 1 dia
    #Para crear un rp que no se borre quitas retentionRules y pones "duration": "INF"
    #No se puede crear un bucket con el mismo nombre que uno ya existente

    r1 = requests.post(url, headers=headers, json=payloadnever)
    r2 = requests.post(url, headers=headers, json=payloadtemp)
    #print(r.text.split(",")[0].split(":")[1].replace('"',"").replace(" ",""))
    #print(r.text)
    return r1.text.split(",")[0].split(":")[1].replace('"',"").replace(" ","")
    #r.text.split(",")[0].split(":")[1].replace('"',"").replace(" ","") de aqui sacas el id del bucket creado


END = False


print("FS Real Time Raspberry")

#print("\nPress PLAY to start RSHIFT to end")
while not END:

    #print(keyboard.read_key())
    #if keyboard.read_key() == "play/pause media":

    print("Programa inicializado\n")

    piloto,circuito = rundata()

    bucketnever = createbucket(piloto,circuito)
    bucket = "296f7f6218c651a2"
    print(f"Bucket created with ID - {bucketnever} | {bucket}")

    #writedatatxtsints(bucketnever,bucket,piloto,circuito)

    rxnrf24(bucketnever,piloto,circuito)

    print("\nPress PLAY to start RSHIFT to end")

    #para Flux, si quieres seleccionr un bucket por ID en vez del nombre -> from bucketID...
