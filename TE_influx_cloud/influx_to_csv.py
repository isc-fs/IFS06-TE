from tqdm import tqdm
from time import sleep


import csv
from influxdb_client import InfluxDBClient
from time import time

from scratches.list_buckets_functions import buckets_cloud

import plotly.express as px

import pandas as pd

import os

import requests

import sys

import time as t
from colorama import Fore, Back, Style

# cloud_org = os.environ.get('CLOUD_ORG')
cloud_org = ''
cloud_token = ''
cloud_url = 'https://us-east-1-1.aws.cloud2.influxdata.com'
cloud_url_buckets = 'https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/buckets'

version = '1.4.2'
'''
Para que funcione, hay que mantener el formato de los buckets como 'version_1.4.0' y actualizado
con cada nueva version.
'''

try:
    buckets = buckets_cloud(cloud_url, cloud_token, cloud_org)
    # See if any bucket starts with 'version'
    for bucket in buckets:
        if bucket.startswith('version'):
            # If it does, check if it's the same version
            if bucket.split('_')[1] == version:
                print('---------')
                print('*************************')
                print('')
                print('You are using the latest version')
                print(Fore.GREEN + f'Version: {version}'+ Fore.RESET)
                # Make copyright for ISC FS racing team
                print('ISC FS Racing Team')
                print('')
                print('*************************')
                print('---------')
            else:
                print('---------')
                print('*************************')
                print('')
                print('New version available, you can find it at...')
                print('TE Telemetry/TE IFS-06/02 - Software/influx_csv')
                print('')
                print(Fore.RED + 'It is recommended to update to the latest version' + Fore.RESET)
                print('')
                print('*************************')
                print('---------')
            
except requests.exceptions.RequestException as e:
    print('---------')
    print('*************************')
    print('')
    print(Fore.RED + 'Unable to verify version, no internet connection' + Fore.RESET)
    print('')
    print('*************************')
    print('---------')


while True:
    err = False
    print('---------')
    print('')
    print(Fore.LIGHTCYAN_EX + 'MENU')
    print('1. Download bucket as csv')
    print('2. Visualize bucket')
    print('3. Exit' + Fore.RESET)
    print('')
    print('---------')
    option = input('Select option: ')



    if option == '1':
        '''
        Dowonload bucket as csv

        1. Get buckets from cloud
        2. Select bucket
        3. Query bucket
        4. Save as csv

        
        '''


        print('---------')
        print('')
        print('Getting buckets from cloud...')


        t0 = time()
        try:
            buckets = buckets_cloud(cloud_url, cloud_token, cloud_org)
            # Eliminar 'ISC' y 'RPI' de la lista
            buckets = [bucket for bucket in buckets if bucket not in ['ISC', 'RPI','_monitoring','_tasks',f'version_{version}']]
        except requests.exceptions.RequestException as e:
            print('---------')
            print('*************************')
            print('')
            print(Fore.RED + 'Unable to access buckets, no internet connection' + Fore.RESET)
            print('')
            print('*************************')
            print('---------')
            err = True
        if err:
            pass
        else:
            for i,bucket in enumerate(buckets):
                print(f"{i+1}. {bucket}")

            print(f'Done in {time() - t0} seconds')
            print('')
            print('')



            bucket_id = input("Enter bucket id: ")

            if not bucket_id.isdigit():
                print('Invalid bucket id, try again (must be a number)')
            elif int(bucket_id) > len(buckets):
                print('Invalid bucket id, try again (check range)')
                
            else:

                bucket = buckets[int(bucket_id)-1]

                client = InfluxDBClient(url=cloud_url, token=cloud_token)

                query = 'from(bucket: "' + bucket + '") |> range(start: -300d)'

                print('Starting query...')
                t0 = time()

                result = client.query_api().query(org=cloud_org, query=query)

                print(f'Done in {time() - t0} seconds')
                # Done in 17.659055471420288 seconds // Using range start: -300d
                # Done in 14.94158148765564 seconds // Using range start: 2023-09-24T16:39:54.572Z & stop
                points = []

                csv_filename = f"{bucket}.csv"
                csv_filename = csv_filename.replace(" ", "_")
                csv_filename = csv_filename.replace(":", "-")
                csv_filename = csv_filename.replace("|>", "-")


                for table in result:
                    for record in table.records:
                        point = {
                            "time": record.get_time(),
                            "measurement": record.get_field(), 
                            "value": record.get_value()
                        }
                        points.append(point)
                # drop all points with measurement 'data' (Esto incluye piloto y circuito)
                points = [point for point in points if point['measurement'] != 'data']

                with open(f'{csv_filename}', 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["time", "measurement", "value"])
                    writer.writeheader()
                    for point in points:
                        writer.writerow(point)
                print(f"File {csv_filename} saved in the current directory")
            print('')
            print('---------')



    elif option == '2':
        '''
        Visualize bucket
        1. Get .csv files in current directory
        2. Select .csv file
        3. Get all measurements in .csv file
        4. Select measurements
        5. Plot measurements

        '''
        err = False


        print('---------')
        print('')
        
        bucket_list = []
        # print all files ending in .csv in current directory
        print('Showing all .csv files in current directory:')


        for i, file in enumerate(os.listdir()):
            if file.endswith('.csv'):
                bucket_list.append(file)
                print(f"{len(bucket_list)}. {file}")


        bucket_option = input("Enter bucket ID: ")
        if not bucket_option.isdigit():
                    print('Invalid bucket id, try again (must be a number)')
        elif int(bucket_option) > len(bucket_list):
            print('Invalid bucket ID, try again (check range)')
        else:
            bucket = bucket_list[int(bucket_option)-1]
            # read .csv file with format: time, measurement, value

            df = pd.read_csv(bucket)


            # print all the unique measurements in df
            measurement_list = []
            for i, measurement in enumerate(df['measurement'].unique()):
                measurement_list.append(measurement)
                print(f"{i+1}. {measurement}")
            measurement_list.append('potencia')
            print(f'{len(measurement_list)}. potencia')



            print('')
            print('Enter measurement id to plot, separated by commas (e.g. 3,4,5)')
            print('')
            measurement_options = input("Enter id: ").split(',')

            for i in measurement_options:
                if not i.isdigit():
                    print('Invalid measurement id, try again (must be a number)')
                    err = True
                elif int(i) > len(measurement_list):
                    print('Invalid measurement id, try again (check id range)')
                    err = True

            
            if not err:
                # convert value column to numeric
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df['time'] = pd.to_datetime(df['time'], errors='coerce')

                # check if 'potencia' is in measurement_options
                if 'potencia' in [measurement_list[int(i)-1] for i in measurement_options]:
                    
                    print('Calculating power...')

                    df1 = df[df['measurement'] == 'dc_bus_voltage']
                    df2 = df[df['measurement'] == 'current_sensor']

                    # Establecer 'time' como el índice para poder alinear las series de tiempo
                    df1.set_index('time', inplace=True)
                    df2.set_index('time', inplace=True)

                    # Eliminar la columna 'measurement'
                    df1 = df1.drop(columns=['measurement'])
                    df2 = df2.drop(columns=['measurement'])
                    
                    # Remuestrear los datos a un intervalo de tiempo diario
                    df1_resampled = df1.resample('S').mean()
                    df2_resampled = df2.resample('S').mean()

                    # Alinear las dos series de tiempo
                    aligned_value1, aligned_value2 = df1_resampled['value'].align(df2_resampled['value'])

                    # Multiplicar las dos series de tiempo
                    result = aligned_value1 * aligned_value2

                    # Crear un nuevo DataFrame para el resultado
                    df_result = pd.DataFrame(result, columns=['value'])
                    df_result['measurement'] = 'potencia'
                    df_result = df_result.dropna()

                    # Cambiar el orden de las columnas
                    df_result = df_result[['measurement', 'value']]

                    # Resetear el índice para poder usar 'time' en la gráfica
                    df_result.reset_index(inplace=True)

                    df = pd.concat([df, df_result])

                fig = px.line(df[df['measurement'].isin([measurement_list[int(i)-1] for i in measurement_options])], x='time', y='value', color='measurement')
                fig.show()

        print('')
        print('---------')

    elif option == 'iscracingteam':
        '''
        
        Ignorar por completo, no mirar, no tocar, no pensar, no respirar, no vivir, no existir, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar, no ser, no estar, no hacer, no pensar, no sentir, no querer, no desear, no amar, no odiar
        
        '''

        # Start fake glitching
        print(Fore.RED + Back.GREEN + 'Descargando claves...')
        for i in tqdm(range(300)):
            sleep(0.01)

        print('Claves descargadas')

        print('Descifrando claves...')
        for i in tqdm(range(100)):
            sleep(0.01)

        print('Claves descifradas')

        print('Iniciando ataque...')
        for i in tqdm(range(400)):
            sleep(0.01)

        # print ataque finalizado with glitched characters
        print('Ataque fina i#ad!')

        import webbrowser
        import random

        # Lista de URLs para abrir
        # https://github.com/ShatteredDisk/rickroll
        urls = ["https://bit.ly/3BlS71b"]


        # Abrir una pestaña aleatoria de Chrome
        for i in range(3):
            webbrowser.open(random.choice(urls))

        print('')
        print('Enhorabuena, has encontrado el huevo de pascua')
        print('')


        import pyautogui
        import time
        import random

        # Obtener el tamaño de la pantalla
        screen_width, screen_height = pyautogui.size()

        start_time = time.time()

        # Mover el ratón aleatoriamente durante 5 segundos
        while time.time() - start_time < 7:
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            pyautogui.moveTo(x, y, duration=0.1)

        sys.exit()


    elif option == '3':

        print(Fore.RED + 'Viv'+ Fore.YELLOW + 'a Espa'+ Fore.RED + 'ña!')
        t.sleep(1)
        sys.exit()



    else:
        print('---------')
        print('')
        print('Invalid option, try again')
        print('')
        print('---------')




'''

Fadrique Alvarez De Toledo Abaitua
fadriquealvarezdetoledoabaitua@gmail.com
web.fadriqueserver.com

'''


'''
if 'dc_bus_voltage' and 'current_sensor' in [measurement_list[int(i)-1] for i in measurement_options]:
                # print('Calculating power...')
                try:
                    df1 = df[df['measurement'] == 'dc_bus_voltage']
                    df2 = df[df['measurement'] == 'current_sensor']

                    # Convert to numeric values
                    df1['dc_bus_voltage'] = pd.to_numeric(df1['measurement'], errors='coerce')
                    df2['current_sensor'] = pd.to_numeric(df2['measurement'], errors='coerce')

                    # Ensure the index is a DateTimeIndex
                    df1.index = pd.to_datetime(df1.index)
                    df2.index = pd.to_datetime(df2.index)


                    # Resample to a common time interval (e.g., 1 minute)
                    try:
                        df1_resampled = df1['time'].resample('1T').mean()
                        df2_resampled = df2['time'].resample('1T').mean()
                    except Exception as e:
                        # print(f"Error resampling dataframes: {e}")
                        pass
                        
                    # Reset the index
                    #print('Resetting index')
                    df1_resampled.reset_index(inplace=True)
                    df2_resampled.reset_index(inplace=True)

                    # Merge the two dataframes
                    if not err:
                        # print('Merging dataframes')
                        merged_df = pd.merge(df1_resampled, df2_resampled, left_index=True, right_index=True)
                    # print(merged_df.head())

                    merged_df['potencia'] = merged_df['dc_bus_voltage'] * merged_df['current_sensor']
                except Exception as e:
                    # print(e)
                    pass


En un script de Python, encontré yo,
un bloque de código lleno de desorden y error.
Intenta calcular potencia, mas no puede volar,
en un mar de excepciones, se queda sin navegar.

"dc_bus_voltage" y "current_sensor" son su afán,
pero en el camino, se pierde sin plan.
Intenta convertir, resamplear y fundir,
pero en su confusión, no logra ni seguir.

Las excepciones lo abrazan, lo ocultan del sol,
en un manto de errores, se ahoga en su error.
Intenta, persiste, pero no puede avanzar,
en un laberinto de problemas, se queda sin hallar.

Mas no todo está perdido, siempre hay una salida,
un camino hacia el orden, una nueva vida.
Con paciencia y cuidado, se puede refactorizar,
y de esta basura de código, algo limpio crear.

Así que no te desesperes, sigue adelante sin temor,
con cada corrección, llegarás a tu mejor versión.
Y cuando el código funcione, con gracia y esplendor,
celebrarás el triunfo de tu valiente labor.
'''
