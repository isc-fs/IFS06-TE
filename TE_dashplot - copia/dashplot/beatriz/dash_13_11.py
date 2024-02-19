# 13-NOV V.1- Actualiza gráfico a la vez que lee los datos.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
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
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
])

# Define callback to update the plot
# Define callback to update the plot
@app.callback(Output('real-time-plot', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_plot(n):
    # Read all data points up to the current point
    data_points = df.iloc[:n % len(df) + 1]

    # Create a plot using plotly.graph_objects
    fig = go.Figure(data=go.Scatter(x=data_points['time'], y=data_points['value'], mode='lines+markers'))
    fig.update_layout(title='Real-Time Line Chart')    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
