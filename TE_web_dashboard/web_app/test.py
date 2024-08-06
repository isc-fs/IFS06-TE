import os

print(os.getcwd())

print('CSV files:', [f for f in os.listdir('TE_web_dashboard/web_app/csv_files') if f.endswith('.csv')])


# from the csv example1.csv extract all the unique measurement id (time,measurement,values)
import pandas as pd

df = pd.read_csv('TE_web_dashboard/web_app/csv_files/example1.csv')

print(df['measurement'].unique())

# check time column is parsed as datetime
print(df.dtypes)

# convert time column to datetime
df['time'] = pd.to_datetime(df['time'])

print(df.dtypes)
