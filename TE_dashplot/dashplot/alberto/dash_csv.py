import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import random
import plotly.graph_objs as go
import datetime
from collections import deque

csv = 'alberto\2023-10-22_12-38-47_-_FS-endurance1_2-marco.csv'
df = pd.read_csv(csv)
df['time_timestamp'] = pd.to_datetime(df['time'].apply(lambda x: x[:19]))

dc = df[df['measurement']== 'dc_bus_voltage']

di = df[df['measurement']== 'i_actual']

digbt = df[df['measurement']== 'igbt_temp']

dinv = df[df['measurement']== 'inverter_temp']


# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Crear la disposición de la aplicación
app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            html.H1("Visualización en Tiempo Real con Datos del csv:" + csv),
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Voltaje bus DC"),
                    dcc.Graph(
                        id='graph1',
                        animate=True,
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
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Intesidad"),
                    dcc.Graph(
                        id='graph2',
                        animate=True,
                        config={'displayModeBar': False},
                        figure={
                            'data': [go.Scatter(
                                x=[],
                                y=[],
                                name='Gráfica 2',
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
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Temperatura igbt"),
                    dcc.Graph(
                        id='graph3',
                        animate=True,
                        config={'displayModeBar': False},
                        figure={
                            'data': [go.Scatter(
                                x=[],
                                y=[],
                                name='Grafica 3',
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
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Temperatura del inversor"),
                    dcc.Graph(
                        id='graph4',
                        animate=True,
                        config={'displayModeBar': False},
                        figure={
                            'data': [go.Scatter(
                                x=[],
                                y=[],
                                name='Grafica 4',
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
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
], fluid=True)

# Inicialización de los datos
X = deque(maxlen=9580)
Y1, Y2, Y3, Y4 = [deque(maxlen=9580) for _ in range(4)]
now = df["time_timestamp"].iloc[0]
for i in range(9580):
    X.append(now - datetime.timedelta(seconds=9580-i))
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
    [Input('interval-component', 'n_intervals')]
)

def update_graphs(n, time_frame):
    global X
    global Y1, Y2, Y3, Y4

    now = df["time_timestamp"].iloc[n+1]
    X.append(now)
    Y1.append(dc.iloc[n+1]['value'])
    Y2.append(di.iloc[n+1]['value'])
    Y3.append(digbt.iloc[n+1]['value'])
    Y4.append(dinv.iloc[n+1]['value'])

    x_range = [now - datetime.timedelta(seconds=time_frame), now]

    data1 = go.Scatter(
        x=list(X),
        y=list(Y1),
        name='Gráfica 1',
        mode='lines',
        line=dict(width=2)
    )
    data2 = go.Scatter(
        x=list(X),
        y=list(Y2),
        name='Gráfica 2',
        mode='lines',
        line=dict(width=2)
    )
    data3 = go.Scatter(
        x=list(X),
        y=list(Y3),
        name='Gráfica 3',
        mode='lines',
        line=dict(width=2)
    )
    data4 = go.Scatter(
        x=list(X),
        y=list(Y4),
        name='Gráfica 4',
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
    figure2 = {
        'data': [data2],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y2), max(Y2)], automargin=True),
            template='plotly_dark',
            yaxis_showgrid=False,
            legend=dict(orientation='h', x=0, y=1.1),
            margin=dict(l=0, r=0, t=10, b=0),
            autosize=True
        )
    }
    figure3 = {
        'data': [data3],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y3), max(Y3)], automargin=True),
            template='plotly_dark',
            yaxis_showgrid=False,
            legend=dict(orientation='h', x=0, y=1.1),
            margin=dict(l=0, r=0, t=10, b=0),
            autosize=True
        )
    }
    figure4 = {
        'data': [data4],
        'layout': go.Layout(
            xaxis=dict(range=x_range),
            yaxis=dict(range=[min(Y4), max(Y4)], automargin=True),
            template='plotly_dark',
            yaxis_showgrid=False,
            legend=dict(orientation='h', x=0, y=1.1),
            margin=dict(l=0, r=0, t=10, b=0),
            autosize=True
        )
    }

    return figure1, figure2, figure3, figure4

if __name__ == '__main__':
    app.run_server(debug=True)

