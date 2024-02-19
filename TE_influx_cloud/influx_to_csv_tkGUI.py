
'''
Notas:

Funciona sin problema, pero queda por hacer.

- Plotear los datos en la pestaña 'Visualize'
- Boton para seleccionar los datos a plotear
- Dashboard

- Cambiar los botones del sidebar


'''

from tkinter import *
import tkinter.messagebox
import customtkinter

import csv
import os
import pandas as pd
import requests
from time import time
import threading

from influxdb_client import InfluxDBClient
from scratches.list_buckets_functions import buckets_cloud

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



# Define InfluxDB credentials and URLs
cloud_org = ''
cloud_token = ''
cloud_url = 'https://us-east-1-1.aws.cloud2.influxdata.com'
version = '1.4.2'

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



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



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


                # configure window
        self.title("Telemetría")
        self.geometry(f"{1100}x{580}")


        # configure grid layout (1x2)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)


        '''
        
        SIDEBAR
        
        '''


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Telemetria", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event,text='Download data')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event,text='Refresh data')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2.configure(command = lambda: self.update_scrollable_frame(self.search.get(),get_buckets()))
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event,text='Logs')
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))



        '''
        
        TABVIEW

        
        '''


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=450)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Download")
        self.tabview.add("Visualize")
        self.tabview.add("Dashboard")
        self.tabview.tab("Download").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Visualize").grid_columnconfigure(0, weight=1)


        '''
        
        DOWNLOAD TAB
        
        
        '''

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Download"),width=450, label_text="Bucket list")
        self.scrollable_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        buckets = get_buckets()
        self.radio_var = tkinter.IntVar(value=0)
        for i in range(len(buckets)):
            switch = customtkinter.CTkRadioButton(master=self.scrollable_frame,variable=self.radio_var,value=i, text=buckets[i])
            switch.grid(row=i, column=0, padx=20, pady=10, sticky='n')
            # switch.configure(state = 'disabled')
            self.scrollable_frame_switches.append(switch)

        self.search = customtkinter.CTkEntry(master=self.tabview.tab("Download"), width=100)
        self.search.grid(row=0, column=1, padx=40, pady=0)
        # Access the text of the entry with self.search.get()


        self.search_button = customtkinter.CTkButton(master=self.tabview.tab("Download"), text='Search')
        self.search_button.grid(row=0, column=2, padx=20, pady=40)
        self.search_button.configure(command=lambda: print(self.search.get()))
        # update the scrollable frame with items that are smilar to the search entry
        self.search_button.configure(command=lambda: self.update_scrollable_frame(self.search.get(),buckets))


        self.download_btn = customtkinter.CTkButton(master=self.tabview.tab("Download"), text='Download')
        self.download_btn.grid(row=1, column=0, padx=20, pady=40)
        # Execute the download function when the button is pressed and the selected bucket is not 'No internet connection'
        # Use python multithreading to avoid freezing the GUI

        self.download_btn.configure(command=lambda: self.start_download_data(buckets))


        '''
        

        VISUALIZE TAB
        
        
        '''

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Visualize"), text="Pestaña de visualizacion")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.scrollable_frame_v = customtkinter.CTkScrollableFrame(self.tabview.tab("Visualize"),width=450, label_text="Lista de CSV")
        self.scrollable_frame_v.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.scrollable_frame_v.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches_v = []

        
        self.radio_var_v = tkinter.IntVar(value=0)
        bucket_list = []
        count = 0
        for i,file in enumerate(os.listdir()):
            if file.endswith(".csv"):
                switch = customtkinter.CTkRadioButton(master=self.scrollable_frame_v,variable=self.radio_var_v,value=count, text=file)
                switch.grid(row=i, column=0, padx=20, pady=10, sticky='n')
                # switch.configure(state = 'disabled')
                bucket_list.append(file)
                self.scrollable_frame_switches_v.append(switch)
                count += 1

        self.download_btn_v = customtkinter.CTkButton(master=self.tabview.tab("Visualize"), text='Select')
        self.download_btn_v.grid(row=1, column=0, padx=20, pady=40)
        self.download_btn_v.configure(command=lambda: self.show_csv(bucket_list[self.radio_var_v.get()]))
        # self.download_btn_v.configure(command=lambda: self.show_csv(self.radio_var_v.get()))




        '''
        
        Default values
        
        '''


        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")



    '''
    
    Functions
    
    '''


    def update_scrollable_frame(self, search_entry, buckets):
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Download"),width=450, label_text="Bucket list")
        self.scrollable_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        self.radio_var = tkinter.IntVar(value=0)
        for i in range(len(buckets)):
            if search_entry in buckets[i]:
                switch_v = customtkinter.CTkRadioButton(master=self.scrollable_frame,variable=self.radio_var,value=i, text=buckets[i])
                switch_v.grid(row=i, column=0, padx=20, pady=10, sticky='n')
                # switch.configure(state = 'disabled')
                self.scrollable_frame_switches.append(switch_v)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def show_csv(self,selected_csv):

        print(f'[LOG] Selected {selected_csv}')
        df = pd.read_csv(selected_csv)

        # print all the unique measurements in df
        measurement_list = []
        for i, measurement in enumerate(df['measurement'].unique()):
            measurement_list.append(measurement)
        measurement_list.append('potencia')

        self.scrollable_frame_v2 = customtkinter.CTkScrollableFrame(self.tabview.tab("Visualize"),width=450, label_text="Select measurement")
        self.scrollable_frame_v2.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        self.scrollable_frame_v2.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches_v2 = []

        # self.radio_var_v2 = tkinter.IntVar(value=0)
        self.check_vars_v2 = [tkinter.IntVar(value=0) for _ in range(len(measurement_list))]
        for i in range(len(measurement_list)):
            switch = customtkinter.CTkCheckBox(master=self.scrollable_frame_v2,
                                                    variable=self.check_vars_v2[i],
                                                    text=measurement_list[i])
            switch.grid(row=i, column=0, padx=20, pady=10, sticky='n')
            # switch.configure(state = 'disabled')
            self.scrollable_frame_switches_v2.append(switch)
        
        self.download_btn_v2 = customtkinter.CTkButton(master=self.tabview.tab('Visualize'), text='Plot')
        self.download_btn_v2.grid(row=1, column=1, padx=20, pady=40)
        self.download_btn_v2.configure(command=lambda: self.plot_data(measurement_list,df))

        # Update the GUI
        self.scrollable_frame_v2.update_idletasks()

    def plot_data(self,measurement_list,df):

        selected_measurements = [measurement_list[i] for i, var in enumerate(self.check_vars_v2) if var.get() != 0]

        window = Tk()
        window.title('Plotting in Tkinter')
        # window.state('zoomed') 

        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['time'] = pd.to_datetime(df['time'], errors='coerce')

        # check if 'potencia' is in measurement_options
        if 'potencia' in selected_measurements:
            
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

        fig = Figure(figsize = (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111)

        # Para cada opción de medición seleccionada
        print('[LOG] Selected measurements:')
        print(selected_measurements)
        for i in selected_measurements:
            # Filtrar el dataframe por la medición seleccionada
            filtered_df = df[df['measurement'] == i]
            
            # Trazar la medición en el eje
            plot1.plot(filtered_df['time'], filtered_df['value'], label=i)

        # Configurar la leyenda
        plot1.legend()

        canvas = FigureCanvasTkAgg(fig,master = window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,window)
        toolbar.update()
        canvas.get_tk_widget().pack()


    def start_download_data(self,buckets):
        selected_bucket = buckets[self.radio_var.get()]
        # Show a popup that will only close once download is done
        if selected_bucket == 'No internet connection':
            print('[LOG] No internet connection')
        else:
            
            # Start the download in a new thread
            thread = threading.Thread(target=self.download_data, args=(selected_bucket,))
            thread.start()

            
    def download_data(self,selected_bucket):

        # Hide download button
        self.download_btn.grid_remove()

        # Show progressbar
        self.progressbar_1 = customtkinter.CTkProgressBar(self.tabview.tab("Download"))
        self.progressbar_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()

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

        # Hide progressbar
        self.progressbar_1.grid_remove()

        # Show download button
        self.download_btn.grid(row=1, column=0, padx=20, pady=40)


if __name__ == "__main__":
    app = App()
    app.mainloop()
