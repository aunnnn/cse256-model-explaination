import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.example_layout import example_layout

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css',
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    '/static/main.css'
]

# Main app
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    static_folder='static')

# Root of all views
app.layout = example_layout
app.title = 'CSE256 - model explanation'

# Server when deploy* (view Procfile)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)