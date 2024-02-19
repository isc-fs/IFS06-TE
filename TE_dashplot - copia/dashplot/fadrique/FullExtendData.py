import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import datetime

from dash.dependencies import Input, Output, State

# Example data (a time series).
resolution = 10000
t = np.linspace(0, np.pi * 2, resolution)
y = np.sin(t)
print(y)
# make y random float between -1 and 1
#y = np.random.uniform(-1, 1, resolution)

print(y)
x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(resolution)]

# Example app.
figure = dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[min(x), max(x)]), yaxis=dict(range=[-1, 1])))
app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
app.layout = html.Div([
    dcc.Graph(id='graph', figure=dict(figure)), dcc.Interval(id="interval", interval=100),
    dcc.Store(id='offset', data=0), dcc.Store(id='store', data=dict(x=x, y=y, resolution=resolution)),
])
app.clientside_callback(
    """
    function (n_intervals, data, offset) {
        offset = offset % data.x.length;
        const end = Math.min((offset + 40), data.x.length);  // Ajusta este número para cambiar cuántos puntos se agregan en cada intervalo
        return [[{x: [data.x.slice(offset, end)], y: [data.y.slice(offset, end)]}, [0], 500], end]
    }
    """,
    [Output('graph', 'extendData'), Output('offset', 'data')],
    [Input('interval', 'n_intervals')], [State('store', 'data'), State('offset', 'data')]
)

if __name__ == '__main__':
    app.run_server()


# Smooth cient side animation

# https://stackoverflow.com/questions/63589249/plotly-dash-display-real-time-data-in-smooth-animation