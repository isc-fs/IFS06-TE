import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random
import plotly.graph_objs as go
import datetime
from collections import deque

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Crear la disposición de la aplicación
app.layout = html.Div([
    html.Label('Seleccione el intervalo de tiempo:'),
    dcc.Dropdown(
        id='time-frame-dropdown',
        options=[
            {'label': '1 minuto', 'value': 60},
            {'label': '5 minutos', 'value': 300},
            {'label': '15 minutos', 'value': 900},
            {'label': '30 minutos', 'value': 1800},
        ],
        value=60
    ),
    html.Label('Seleccione la frecuencia de actualización:'),
    dcc.Dropdown(
        id='interval-dropdown',
        options=[
            {'label': '0.1 segundos', 'value': 100},
            {'label': '0.5 segundos', 'value': 500},
            {'label': '1 segundo', 'value': 1000},
            {'label': '2 segundos', 'value': 2000},
            {'label': '5 segundos', 'value': 5000},
            {'label': '10 segundos', 'value': 10000}
        ],
        value=1000
    ),
    html.H1("Visualización en Tiempo Real con Datos Aleatorios"),
    html.H3("Gráfica 1"),
    dcc.Graph(id='graph1', animate=True),
    html.H3("Gráfica 2"),
    dcc.Graph(id='graph2', animate=True),
    html.H3("Gráfica 3"),
    dcc.Graph(id='graph3', animate=True),
    html.H3("Gráfica 4"),
    dcc.Graph(id='graph4', animate=True),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
])

# Inicialización de los datos
X = deque(maxlen=300)
Y1, Y2, Y3, Y4 = [deque(maxlen=300) for _ in range(4)]
now = datetime.datetime.now()
for i in range(300):
    X.append(now - datetime.timedelta(seconds=300-i))
    Y1.append(0)
    Y2.append(0)
    Y3.append(0)
    Y4.append(0)

@app.callback(
    Output('interval-component', 'interval'),
    Input('interval-dropdown', 'value')
)
def update_interval(value):
    return value

@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),
     Output('graph4', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('time-frame-dropdown', 'value')]
)
def update_graphs(n, time_frame):
    global X
    global Y1, Y2, Y3, Y4

    now = datetime.datetime.now()
    X.append(now)
    Y1.append(random.uniform(0, 100))
    Y2.append(random.uniform(0, 100))
    Y3.append(random.uniform(0, 100))
    Y4.append(random.uniform(0, 100))

    x_range = [now - datetime.timedelta(seconds=time_frame), now]

    data1 = go.Scatter(
        x=list(X),
        y=list(Y1),
        name='Scatter',
        mode='lines+markers'
    )
    data2 = go.Scatter(
        x=list(X),
        y=list(Y2),
        name='Scatter',
        mode='lines+markers'
    )
    data3 = go.Scatter(
        x=list(X),
        y=list(Y3),
        name='Scatter',
        mode='lines+markers'
    )
    data4 = go.Scatter(
        x=list(X),
        y=list(Y4),
        name='Scatter',
        mode='lines+markers'
    )

    figure1 = {
        'data': [data1],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y1), max(Y1)]),
            template='plotly_dark',  # Set dark theme
            yaxis_showgrid=False  # Turn off y-grid lines
        )
    }
    figure2 = {
        'data': [data2],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y2), max(Y2)]),
            template='plotly_dark',
            yaxis_showgrid=False
        )
    }
    figure3 = {
        'data': [data3],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y3), max(Y3)]),
            template='plotly_dark',
            yaxis_showgrid=False
        )
    }
    figure4 = {
        'data': [data4],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y4), max(Y4)]),
            template='plotly_dark',
            yaxis_showgrid=False
        )
    }

    return figure1, figure2, figure3, figure4

if __name__ == '__main__':
    app.run_server(debug=True)
