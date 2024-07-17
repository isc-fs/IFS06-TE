import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import datetime
from collections import deque
import pandas as pd
#CSV
csv = '2023-10-22_12-38-47_-_FS-endurance1_2-marco_refcortado.csv'
df = pd.read_csv(csv)
df['time_timestamp'] = pd.to_datetime(df['time'].apply(lambda x: x[:19]))
dc = df[df['measurement']== 'dc_bus_voltage']



# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Crear la disposición de la aplicación
app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            html.H1("Visualización en Tiempo Real con Datos Sacados del csv"),
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Gráfica 1"),
                    dcc.Graph(
                        id='graph1',
                        animate=False,
                        config={'displayModeBar': False},
                        figure={
                            'data': [go.Scatter(
                                x=[],
                                y=[],
                                name='Gráfica 1',
                                mode='lines',
                                line=dict(width=2)
                            )],
                            'layout': go.Layout(
                                xaxis=dict(range=[0, 300]),
                                yaxis=dict(range=[0, 100], automargin=True),
                                template='plotly_dark',
                                yaxis_showgrid=False,
                                legend=dict(orientation='h', x=0, y=1.1),
                                margin=dict(l=0, r=0, t=10, b=0),
                                autosize=True
                            )
                        }
                    ),
                ])
            ]),
        ]),
    ]),
    dcc.Interval(id='interval-component2', interval=60, n_intervals=0),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
], fluid=True)

# Inicialización de los datos
X = deque(maxlen=9480)
Y1, Y2, Y3, Y4 = [deque(maxlen=9480) for _ in range(4)]
now = df["time_timestamp"].iloc[0]
for i in range(9480):
    X.append(now - datetime.timedelta(seconds=9480-i))
    Y1.append(0)
    Y2.append(0)
    Y3.append(0)
    Y4.append(0)
'''
@app.callback(
    Output('interval-component', 'interval'),
    Input('interval-dropdown', 'value')
)
def update_interval(value):
    return value
'''
@app.callback(
    Output('graph1', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('interval-component2', 'interval')]
)
def update_graphs(n, time_frame):
    global X
    global Y1, Y2, Y3, Y4
    
    now = df["time_timestamp"].iloc[n+1]
    X.append(now)
    Y1.append(dc.iloc[n+1]['value'])
    
###
    x_range = [now - datetime.timedelta(seconds=time_frame), now]
###
    data1 = go.Scatter(
        x=list(X),
        y=list(Y1),
        name='Gráfica 1',
        mode='lines',
        line=dict(width=2)
    )      

    figure1 = {
        'data': [data1],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y1), max(Y1)], automargin=True),
            template='plotly_dark',
            yaxis_showgrid=False,
            legend=dict(orientation='h', x=0, y=1.1),
            margin=dict(l=0, r=0, t=10, b=0),
            autosize=True
        )
    }

    return figure1

if __name__ == '__main__':
    app.run_server(debug=True)

'''
    dbc.Card([
        dbc.CardBody([
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
        ])
    ]),
    dbc.Card([
        dbc.CardBody([
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
        ])
    ]),'''