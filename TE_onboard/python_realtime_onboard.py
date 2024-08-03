'''
Receive data through CAN bus and send it to InfluxDB


'''

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


from datetime import datetime

import requests


import can

# Instalar librerias necesarias para recibir por CAN bus (python-can??)
# configurar interfaz CAN bus
    # sudo ip link set can0 up type can bitrate 500000 (e.g)



client = InfluxDBClient(url="http://localhost:8086",
                        token="sNZJlQsv2KhY28xPDZBmt2HbgGtwU5AE4vUjQsks9WPm3o0g_UreLkxNVgMHNotIqUMHCcgAyN4llUvdXs4QtA==",
                       org="b2b03940375e28ac")


def recibir_datos_can():
    '''

    Mantener esto como ejemplo para recibir datos por CAN bus
    No se usa la funcion
    
    '''


    # Crear un bus CAN usando la configuración específica
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    # Bucle para recibir mensajes
    while True:
        mensaje = bus.recv()  # Recibir un mensaje
        if mensaje is not None:
            print(f"ID: {mensaje.arbitration_id}, Datos: {mensaje.data}")



def rxnrf24(bucketnever):
    
    '''
    
    Add method to receive data from CAN bus and send it to InfluxDB

    Done?? Would have to check if it works
    
    '''

    # Crear un bus CAN usando la configuración específica
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Enter a loop receiving data on the address specified.
    try:

        while True:

                mensaje = bus.recv()  # Recibir un mensaje
                if mensaje is not None:
                    print(f"ID: {mensaje.arbitration_id}, Datos: {mensaje.data}")
                    dataid = mensaje.arbitration_id
                    values = mensaje.data
               

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
                # writerundata(bucketnever,bucket) # REMOVE¿?

    except Exception as e:
        print('Error:', e)



def createbucket():
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
    "name": time+" |> FS- local",
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

    bucketnever = createbucket()
    bucket = "296f7f6218c651a2"
    print(f"Bucket created with ID - {bucketnever} | {bucket}")

    #writedatatxtsints(bucketnever,bucket,piloto,circuito)

    rxnrf24(bucketnever)

    # print("\nPress PLAY to start RSHIFT to end")

    #para Flux, si quieres seleccionr un bucket por ID en vez del nombre -> from bucketID...