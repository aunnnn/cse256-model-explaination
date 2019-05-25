import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

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

if __name__ == '__main__':
    app.run_server(debug=True)