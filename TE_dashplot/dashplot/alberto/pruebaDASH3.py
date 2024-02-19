import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random
import plotly.graph_objs as go
import datetime
from collections import deque


# Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Visualización en Tiempo Real con Datos Aleatorios"),
    html.H3("Gráfica 1"),
    dcc.Graph(id='graph1', animate = True),
    html.H3("Gráfica 2"),
    dcc.Graph(id='graph2', animate = True),
    html.H3("Gráfica 3"),
    dcc.Graph(id='graph3', animate = True),
    html.H3("Gráfica 4"),
    dcc.Graph(id='graph4', animate = True),
    dcc.Interval(
        id='graph-update',
        interval=1000,  # Actualiza cada 1000 milisegundos 
        n_intervals=0
    )
])

# Inicialización de los datos
X = deque(maxlen=20)
Y1, Y2, Y3, Y4 = [deque(maxlen=20) for _ in range(4)]
X.append(0)
Y1.append(0)
Y2.append(0)
Y3.append(0)
Y4.append(0)

@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),
     Output('graph4', 'figure')],
    Input('graph-update', 'n_intervals')
)
def update_graphs(n):
    global X
    global Y1, Y2, Y3, Y4


    X.append(X[-1] + 1)
    Y1.append(random.uniform(0, 100))
    Y2.append(random.uniform(0, 100))
    Y3.append(random.uniform(0, 100))
    Y4.append(random.uniform(0, 100))

    # Gráficas
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

    figure1 = {'data': [data1], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y1), max(Y1)]))}
    figure2 = {'data': [data2], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y2), max(Y2)]))}
    figure3 = {'data': [data3], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y3), max(Y3)]))}
    figure4 = {'data': [data4], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y4), max(Y4)]))}

    return figure1, figure2, figure3, figure4

if __name__ == '__main__':
    app.run_server(debug=True)
