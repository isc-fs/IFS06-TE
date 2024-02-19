import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True, figure=dict(data=[dict(x=[0], y=[0])], layout=dict(xaxis=dict(range=[0,100]), yaxis=dict(range=[-1,1])))),
    dcc.Interval(
        id='graph-update',
        interval=100,  # in milliseconds
        n_intervals=0
    ),
])

app.clientside_callback(
    """
    function(n_intervals, old_figure) {
        // Genera un nuevo valor de datos
        var newValue = Math.random() * 2 - 1;

        // Agrega el nuevo valor a los datos existentes del gráfico
        var newX = old_figure.data[0].x.concat(old_figure.data[0].x.length);
        var newY = old_figure.data[0].y.concat(newValue);

        // Calcula el rango del eje x para mostrar siempre los últimos 100 puntos de datos
        var xRange = [Math.max(0, newX.length - 100), newX.length];

        // Actualiza el rango del eje x en el layout del gráfico
        var newLayout = JSON.parse(JSON.stringify(old_figure.layout));
        newLayout.xaxis.range = xRange;

        return {data: [{x: newX, y: newY}], layout: newLayout};
    }
    """,
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')],
    [State('live-graph', 'figure')]
)

if __name__ == '__main__':
    app.run_server(debug=True)