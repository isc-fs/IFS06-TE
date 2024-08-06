import os
import base64
from flask import Flask, redirect, url_for, send_from_directory, request, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

from datetime import timedelta
from flask import session

# print the current working directory
print(os.getcwd())

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # Set session lifetime to 30 minutes

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Contraseña correcta
CORRECT_PASSWORD = 'iscracingteam'

# Clase de usuario para Flask-Login
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    user = User()
    user.id = user_id
    return user

# Decorador para verificar la expiración de la sesión
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True
    if not current_user.is_authenticated and request.endpoint != 'login':
        return redirect(url_for('login'))

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
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Contraseña incorrecta'
    return render_template('login.html', error=error)

# Ruta de cierre de sesión
@app.route('/logout')
@login_required
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
CSV_DIR = 'TE_web_dashboard/web_app/csv_files'

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(base_dir, 'csv_files')

# Function to list CSV files
def list_csv_files():
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    return [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]

# Define the title
dash_app.title = 'ISC FS Team'
dash_app._favicon = 'icon.ico'

# Define the layout for the Dash app
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='search-bar-store'),
    html.Div([
        html.Div([
            html.Div([
                html.Img(src='/static/icon.ico', className='circular-icon'),
                html.H2("CSV Files", className="sidebar-title"),
                dcc.Input(id='search-bar', type='text', placeholder='Search CSV...', style={'width': '90%', 'padding': '10px'})
            ], className="sidebar-header"),
            html.Div([
                html.Ul(id='file-list', className="file-list")
            ], className="sidebar-content")
        ], className="sidebar"),
        html.Div(id='page-content', className="content"),
        dcc.Download(id="download-csv"),
    ], className="container", style={'height': '100vh', 'overflowY': 'hidden'})
])

# Callback to update the search-bar-store value when search-bar changes
@dash_app.callback(
    Output('search-bar-store', 'data'),
    [Input('search-bar', 'value')]
)
def update_search_bar_store(search_value):
    return search_value

# Callback to update the file list based on search input
@dash_app.callback(
    Output('file-list', 'children'),
    [Input('search-bar-store', 'data')]
)
def update_file_list(search_value):
    files = list_csv_files()
    if search_value:
        search_terms = search_value.split()
        files = [f for f in files if all(term.lower() in f.lower() for term in search_terms)]
    return [html.Li(html.A(f, href=f'/dashboard/{f}')) for f in files]

# Callback to restore the search bar value from the store
@dash_app.callback(
    Output('search-bar', 'value'),
    [Input('search-bar-store', 'data')]
)
def restore_search_bar_value(stored_value):
    return stored_value

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
@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')], [State('search-bar-store', 'data')])
def display_page(pathname, search_value):
    if pathname and pathname != '/dashboard/':
        file_path = pathname.split('/')[-1]
        if file_path in list_csv_files():
            df = pd.read_csv(os.path.join(CSV_DIR, file_path), parse_dates=[0])

            # Ordenar el DataFrame por la columna 'time'
            df = df.sort_values(by='time')

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

            return html.Div([
                options_menu,
                dcc.Download(id="download-csv"),
                html.Div(graphs, style={'overflowY': 'scroll', 'height': '100vh'})
            ])
    return html.Div('Select a CSV file to view its dashboard.', style={
        'text-align': 'center',
        'margin-top': '20%',
        'font-size': '24px',
        'color': 'white'
    })

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
