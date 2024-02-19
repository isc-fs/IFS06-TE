import pandas as pd
import numpy as np

df = pd.read_csv('2023-10-05_13-51-37_-_FS-jarama_accel_2-marco.csv')

# convert al values in df to float except measurements where measurement = 'data'
df['value'] = pd.to_numeric(df['value'], errors='coerce')

values = df[df['measurement'] == 'ax']['value'].values
print(type(values))
print(type(values[0]))


# convert al time values in df to datetime
df['time'] = pd.to_datetime(df['time'], errors='coerce')
time = df['time'].values
print(type(time))
print(type(time[0]))