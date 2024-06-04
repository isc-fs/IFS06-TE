# 13-NOV V.2- Existen 2 intervalos: 
# intervalo para actualizar los gráficos
# intervalo para leer datos cada x milisegundos desde el csv 
# se ha creado un csv simulando datos de suspensión

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import datetime
from collections import deque
import pandas as pd

#Función para crear un componente grafica 
def grafica(nombre, n):
    card = dbc.Card([
        dbc.CardBody([
            html.H3(nombre),
            dcc.Graph(
                id=f'real-time-plot{n}',
                animate=False,
                config={'displayModeBar': False},
                figure={
                    'data': [go.Scatter(
                        x=[],
                        y=[],
                        name=f'Gráfica {n}',
                        mode='lines',
                        line=dict(width=2)
                    )],
                    'layout': go.Layout(
                        xaxis=dict(range=[0, 300]),
                        yaxis=dict(range=[0, 100],
                                   automargin=True,
                                   tickangle=-45),
                        template='plotly_dark',
                        yaxis_showgrid=False,
                        legend=dict(orientation='h', x=0, y=1.1),
                        margin=dict(l=0, r=0, t=10, b=0),
                        autosize=True
                    )
                }
            ),
        ],style={'background': 'rgba(40,40,40,1)'})  # fondo del CardBody transparente
    ], style={'background': 'rgba(40,40,40,1)'})  # fondo del Card transparente
    return card





# Lectura y división del CSV
csv = 'dashplot/alberto/2023-10-22_12-38-47_-_FS-endurance1_2-marco.csv'
df = pd.read_csv(csv)
df['time_timestamp'] = pd.to_datetime(df['time'].apply(lambda x: x[:19]))
dc = df[df['measurement']== 'dc_bus_voltage']
di = df[df['measurement']== 'i_actual']
digbt =df[df['measurement']== 'igbt_temp']
dinv =df[df['measurement']== 'inverter_temp']
dmotor = df[df['measurement']== 'motor_temp']
dna = df[df['measurement']== 'n_actual']
dax =df[df['measurement']== 'ax']
day =df[df['measurement']== 'ay']
daz = df[df['measurement']== 'az']
db = df[df['measurement']== 'brake']
dth =df[df['measurement']== 'throttle']
dcs =df[df['measurement']== 'current_sensor']
dsfr = df[df['measurement']== 'Suspension_FR']
dsfl = df[df['measurement']== 'Suspension_FL']
dsrr =df[df['measurement']== 'Suspension_RR']
dsrl =df[df['measurement']== 'Suspension_RL']
 
# Inicialización de la app DASH
app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.SLATE])

# Layout
app.layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            html.H1("Visualización en Tiempo Real con Datos Sacados del csv: "+ csv),
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('DC_BUS_VOLTAGE','1')
        ]),
        dbc.Col([
            grafica('I_ACTUAL','2')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('IGBT_TEMP','3')
        ]),
        dbc.Col([
            grafica('INVERTER_TEMP','4')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('MOTOR_TEMP','5')
        ]),
        dbc.Col([
            grafica('N_ACTUAL','6')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('AX','7')
        ]),
        dbc.Col([
            grafica('AY','8')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('AZ','9')
        ]),
        dbc.Col([
            grafica('BRAKE','10')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('THROTTLE','11')
        ]),
        dbc.Col([
            grafica('CURRENT_SENSOR','12')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('SUSPENSION_FR','13')
        ]),
        dbc.Col([
            grafica('SUSPENSION_FL','14')
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            grafica('SUSPENSION_RR','15')
        ]),
        dbc.Col([
            grafica('SUSPENSION_RL','16')
        ]),
        
    ]),
    
    dcc.Interval(
        id='data-interval',
        interval=300,  
        n_intervals=0
    ),
    dcc.Interval(
        id='update-interval',
        interval=300,
        n_intervals=0
    )
], fluid=True)

# Callback
@app.callback([Output('real-time-plot1', 'figure'),
               Output('real-time-plot2', 'figure'),
               Output('real-time-plot3', 'figure'),
               Output('real-time-plot4', 'figure'),
               Output('real-time-plot5', 'figure'),
               Output('real-time-plot6', 'figure'),
               Output('real-time-plot7', 'figure'),
               Output('real-time-plot8', 'figure'),
               Output('real-time-plot9', 'figure'),
               Output('real-time-plot10', 'figure'),
               Output('real-time-plot11', 'figure'),
               Output('real-time-plot12', 'figure'),
               Output('real-time-plot13', 'figure'),
               Output('real-time-plot14', 'figure'),
               Output('real-time-plot15', 'figure'),
               Output('real-time-plot16', 'figure')],
              [Input('data-interval', 'n_intervals'),
               Input('update-interval', 'n_intervals')])
def update_plot(data_n, update_n):

    #Función para crear la actualización de las gráficas, coge todo los valores hasta dicho momento de actualización 
    def figura(dataframe, mode):
        data_points = dataframe.iloc[:data_n % len(dataframe) + 1]
        fig = go.Figure(data=go.Scatter(
            x=data_points['time'], 
            y=data_points['value'], 
            mode=mode,
            hovertemplate='Hora: %{x|%H:%M:%S}<br>Valor: %{y}<extra></extra>'))
        fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # fondo de la gráfica rojo
        paper_bgcolor='rgba(0,0,0,0)',  # fondo del papel rojo
        #yaxis_showgrid=False,
        xaxis_showgrid=False,
        # x axis labels angle
        xaxis_tickangle=-45,
        template='plotly_dark',
        transition={'duration': 300, 'easing': 'cubic-in-out'},  # transición más suave
    )

        return fig

    fig1 =  figura(dc, 'lines') 
    fig2 =  figura(di, 'lines')
    fig3 =  figura(digbt, 'lines')
    fig4 =  figura(dinv, 'lines')
    fig5 =  figura(dmotor, 'lines')
    fig6 =  figura(dna, 'lines')
    fig7 =  figura(dax, 'lines')
    fig8 =  figura(day, 'lines')
    fig9 =  figura(daz, 'lines')
    fig10 = figura(db, 'lines')
    fig11 = figura(dth, 'lines')
    fig12 = figura(dcs, 'lines')
    fig13 = figura(dsfr, 'lines')
    fig14 = figura(dsfl, 'lines')
    fig15 = figura(dsrr, 'lines')
    fig16 = figura(dsrl, 'lines')
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14, fig15, fig16

if __name__ == '__main__':
    app.run_server(debug=True)
