import os
import base64
from flask import Flask, redirect, url_for, send_from_directory, request, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

app = Flask(__name__)
app.secret_key = 'super secret key'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Contraseña correcta
CORRECT_PASSWORD = '33'

# Clase de usuario para Flask-Login
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    user = User()
    user.id = user_id
    return user

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if password == CORRECT_PASSWORD:
            user = User()
            user.id = 'user'  # ID estático, ya que no estamos manejando múltiples usuarios
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            error = 'Contraseña incorrecta'
    return render_template('login.html', error=error)

# Ruta de cierre de sesión
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Proteger la ruta de Dash con Flask-Login
@app.before_request
def before_request():
    if not current_user.is_authenticated and request.path.startswith('/dashboard'):
        return redirect(url_for('login'))

# Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')
CSV_DIR = 'csv_files'


# Function to list CSV files
def list_csv_files():
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    return [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]

# Define the layout for the Dash app
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.H2("CSV Files", className="sidebar-title"),
            dcc.Input(id='search-bar', type='text', placeholder='Search CSV...', style={'width': '90%', 'padding': '10px'}),
            html.Ul(id='file-list', className="file-list")

        ], className="sidebar"),
        html.Div(id='page-content', className="content"),
        dcc.Download(id="download-csv"),
    ], className="container", style={'height': '100vh', 'overflowY': 'hidden'})
])

# Callback to update the file list dynamically
@dash_app.callback(Output('file-list', 'children'), [Input('url', 'pathname'), Input('search-bar', 'value')])
def update_file_list(pathname, search_value):
    csv_files = list_csv_files()
    if search_value:
        # Filtra los archivos que contienen el texto de búsqueda (case-insensitive)
        filtered_files = [file for file in csv_files if search_value.lower() in file.lower()]
    else:
        filtered_files = csv_files
    return [html.Li(dcc.Link(file, href=f'/dashboard/{file}')) for file in filtered_files]

# Callback para manejar la descarga del archivo CSV
@dash_app.callback(
    Output("download-csv", "data"),
    [Input("option-1", "n_clicks")],
    [State('url', 'pathname')]
)
def download_csv(n_clicks, pathname):
    if n_clicks is None or pathname == '/dashboard/':
        return dash.no_update
    else:
        file_path = pathname.split('/')[-1]
        if file_path in list_csv_files():

            with open(os.path.join(CSV_DIR, file_path), 'r') as file:
                content = file.read()
            # content_encoded = base64.b64encode(content.encode()).decode()
                

            # Inicia la descarga retornando el path del archivo
            return dict(content=content, filename=file_path)

# Callback to display the CSV file content and download link
@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname and pathname != '/dashboard/':
        file_path = pathname.split('/')[-1]
        if file_path in list_csv_files():
            df = pd.read_csv(os.path.join(CSV_DIR, file_path), parse_dates=[0])
            graphs = []
            for unique_id in df['measurement'].unique():
                filtered_df = df[df['measurement'] == unique_id]
                graph = dcc.Graph(
                    id=f'graph-{unique_id}',
                    figure={
                        'data': [
                            {'x': filtered_df['time'], 'y': filtered_df['value'], 'type': 'line', 'name': unique_id}
                        ],
                        'layout': {
                            'title': unique_id
                        }
                    }
                )
                graphs.append(graph)

            options_menu = html.Div([
                html.Button("Download CSV", id="option-1"),
                html.Button("Option 2", id="option-2"),
            ], className="options-menu")

            return html.Div([options_menu,dcc.Download(id="download-csv"), html.Div(graphs, style={'overflowY': 'scroll', 'height': '100vh'})])
    return html.Div('Select a CSV file to view its dashboard.', style={
                    'text-align': 'center', 
                    'margin-top': '20%', 
                    'font-size': '24px'})

@app.route('/download/<path:filename>')
def download_file(filename):
    """Serve a file from the filesystem."""
    return send_from_directory(CSV_DIR, filename, as_attachment=True)

# Rutas de Flask
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    return dash_app.index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)