# 13-NOV V.2- Existen 2 intervalos: 
# intervalo para actualizar los gráficos
# intervalo para leer datos cada x milisegundos desde el csv 
# se ha creado un csv simulando datos de suspensión

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load your CSV file
df = pd.read_csv('suspension_test1_rl.csv')
df['time'] = pd.to_datetime(df['time'])

# Initialize Dash app
app = dash.Dash(__name__)

# Set up layout
app.layout = html.Div([
    dcc.Graph(id='real-time-plot'),
    dcc.Interval(
        id='data-interval',
        interval=2000,  # milliseconds (read data every 5 seconds)
        n_intervals=0
    ),
    dcc.Interval(
        id='update-interval',
        interval=1000,  # in milliseconds (update plot every 1 second)
        n_intervals=0
    )
])

# Define callback to update the plot
@app.callback(Output('real-time-plot', 'figure'),
              [Input('data-interval', 'n_intervals'),
               Input('update-interval', 'n_intervals')])
def update_plot(data_n, update_n):
    # Read all data points up to the current point
    data_points = df.iloc[:data_n % len(df) + 1]

    # Create a plot using plotly.graph_objects
    fig = go.Figure(data=go.Scatter(x=data_points['time'], y=data_points['value'], mode='lines+markers'))
    fig.update_layout(title='Real-Time Line Chart')    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
