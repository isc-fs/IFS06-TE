#!/usr/bin/env python
"""
    Example of (almost) all Elements, that you can use in PySimpleGUI.
    Shows you the basics including:
        Naming convention for keys
        Menubar format
        Right click menu format
        Table format
        Running an async event loop
        Theming your application (requires a window restart)
        Displays the values dictionary entry for each element
        And more!

    Copyright 2021, 2022, 2023 PySimpleGUI
"""

import PySimpleGUI as sg
import requests
from time import time
import csv
import os
import pandas as pd

from influxdb_client import InfluxDBClient
from scratches.list_buckets_functions import buckets_cloud




# Define InfluxDB credentials and URLs
cloud_org = ''
cloud_token = ''
cloud_url = 'https://us-east-1-1.aws.cloud2.influxdata.com'
version = '1.4.2'

def get_buckets():
    try:
        buckets = buckets_cloud(cloud_url, cloud_token, cloud_org)
        # Eliminar 'ISC' y 'RPI' de la lista
        buckets = [bucket for bucket in buckets if bucket not in ['ISC', 'RPI','_monitoring','_tasks',f'version_{version}']]
        print('[LOG] Query bucket list')
    except requests.exceptions.RequestException as e:
        print('[LOG] No internet connection: Error')
        buckets = ['No internet connection']
    except:
        print('[LOG] No internet connection: Unknown error')
        buckets = ['No internet connection']

    return buckets

def make_window(theme):

    buckets = get_buckets()

    sg.theme(theme)
    menu_def = [
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing','More Nothing','Exit']]

    bucket_list = []
    for i, file in enumerate(os.listdir()):
        if file.endswith('.csv'):
            bucket_list.append(file)

    download_layout = [[sg.T('Download bucket as csv', size=(25, 2), key='-DOWNLOAD-')],
               [sg.Image(data=sg.DEFAULT_BASE64_ICON,  k='-IMAGE-')],
               [sg.Listbox(values=buckets, size=(30, 6), key='-LISTD-', enable_events=True,expand_x=True)], 
               [sg.Button('Refresh', key='-REFRESH_DOWNLOAD-')]
               ]

    visualize_layout = [[sg.T('Seleccionar bucket para visualizar', size=(25, 2), key='-VISUALIZE-')],
                        [sg.Listbox(values=bucket_list, size=(30, 6), key='-LISTV-', enable_events=True,expand_x=True)],
                        [sg.Button('Select', key='-SELECT-')],
                        [sg.Button('Back', key='-BACK-')],
                        [sg.Button('Refresh', key='-REFRESH-')]
                        ]

    logging_layout = [[sg.Text("Anything printed will display here!")],
                      [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                      # [sg.Output(size=(60,15), font='Courier 8', expand_x=True, expand_y=True)]
                      ]
    
    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values = sg.theme_list(), 
                      size =(20, 12), 
                      key ='-THEME LISTBOX-',
                      enable_events = True)],
                      [sg.Button("Set Theme")]]
    
    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
                [sg.Text('Telemetry Data Manager', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    layout +=[[sg.TabGroup([[
                               sg.Tab('Download Buckets', download_layout),
                               sg.Tab('Visualize Buckets', visualize_layout),
                               sg.Tab('Theming', theme_layout),
                               sg.Tab('Output', logging_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

               ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Manu Mason', layout,icon='icon.ico', right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window.set_min_size(window.size)
    return window

def main():
    window = make_window(sg.theme())
    is_csv = True
    # This is an Event Loop 
    while True:
        event, values = window.read(timeout=100)
        # print(event)
        # keep an animation running so show things are happening

        if event == '-SELECT-':
            '''
            Este boton solo deberia salir en seleccionar ids
            '''
            selected_bucket = values['-LISTV-']
            print(f'[LOG] Selected buckets {selected_bucket}')

        if event == '-BACK-':
            '''
            Este boton solo deberia salir en seleccionar ids
            '''
            bucket_list = []
            for i, file in enumerate(os.listdir()):
                if file.endswith('.csv'):
                    bucket_list.append(file)
            is_csv = True
            window['-LISTV-'].update(values=bucket_list)

        if event == '-LISTV-':
            
            if is_csv:
                selected_bucket = values['-LISTV-'][0]
                print(f'[LOG] Selected bucket {selected_bucket}')
                df = pd.read_csv(selected_bucket)


                # print all the unique measurements in df
                measurement_list = []
                for i, measurement in enumerate(df['measurement'].unique()):
                    measurement_list.append(measurement)
                measurement_list.append('potencia')

                window['-LISTV-'].update(values=measurement_list)
                window.Element('-LISTV-').widget.config(selectmode= sg.LISTBOX_SELECT_MODE_MULTIPLE)
                is_csv = False
            else:
                pass

        if event == '-LISTD-':
            selected_bucket = values['-LISTD-'][0]

            if selected_bucket == 'No internet connection':
                pass
            else:


                # Disable the Listbox
                window['-LISTD-'].update(disabled=True)


                print("[LOG] User selected bucket: " + str(selected_bucket))
                t0 = time()

                client = InfluxDBClient(url=cloud_url, token=cloud_token)

                query = 'from(bucket: "' + selected_bucket + '") |> range(start: -300d)'

                t0 = time()

                result = client.query_api().query(org=cloud_org, query=query)

                print(f'Done in {time() - t0} seconds')
                # Done in 17.659055471420288 seconds // Using range start: -300d
                # Done in 14.94158148765564 seconds // Using range start: 2023-09-24T16:39:54.572Z & stop
                points = []

                csv_filename = f"{selected_bucket}.csv"
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

                # Enable the Listbox
                window['-LISTD-'].update(disabled=False)


                sg.popup("Downloaded: " + str(selected_bucket) + f'\nDone in {time() - t0} seconds', keep_on_top=True)

        if event == '-REFRESH-':

            if not is_csv:
                print('[LOG] Cant update ids')
            else:
                # Generate the list of csv files
                bucket_list = []
                # print('Showing all .csv files in current directory:')
                print('[LOG] Updating .csv list in current directory')
                for i, file in enumerate(os.listdir()):
                    if file.endswith('.csv'):
                        bucket_list.append(file)

                # Update the Listbox with the new list of csv files
                window['-LISTV-'].update(values=bucket_list)

        if event == '-REFRESH_DOWNLOAD-':
            print('[LOG] Updating bucket list from cloud')
            buckets = get_buckets()
            window['-LISTD-'].update(values=buckets)
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        if event == 'About':
            # print("[LOG] Clicked About!")
            sg.popup('Herramienta de acceso a la telemetria',
                     'Arriba Essspaña',
                     keep_on_top=True)
        
        elif event == "Set Theme":
            # print("[LOG] Clicked Set Theme!")
            theme_chosen = values['-THEME LISTBOX-'][0]
            # print("[LOG] User Chose Theme: " + str(theme_chosen))
            window.close()
            window = make_window(theme_chosen)
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Versions':
            sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)

    window.close()
    exit(0)

if __name__ == '__main__':
    sg.theme('black')
    sg.theme('dark red')
    sg.theme('dark green 7')
    # sg.theme('DefaultNoMoreNagging')



    main()
