# how to import plotly
import plotly.express as px

import pandas as pd

import os

csv_filename = '2023-10-05_13-57-50_-_FS-jarama_accel_5-marco.csv'

# read .csv file with format: time, measurement, value
df = pd.read_csv(f'CSV/{csv_filename}')
print(df.head())

# print all the unique measurements in df
print(df['measurement'].unique())


# print all files ending in .csv in current directory
for file in os.listdir():
     if file.endswith('.py'):
            print(file)



measurement_list = input("Enter measurement: ").split(',')
print(measurement_list)

# plot data in df using 'throttle' and 'brake' measurements using plotly
fig = px.line(df[df['measurement'].isin(['ax', 'ay','az'])], x='time', y='value', color='measurement')
fig.show()
