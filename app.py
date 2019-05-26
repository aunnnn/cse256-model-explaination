import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from components.example_layout import ExampleLayout

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css',
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    '/assets/main.css'
]

# Main app
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    static_folder='assets')

# Root of all views
main_layout = ExampleLayout()

app.layout = main_layout.render()
app.title = 'CSE 256 - Model Explanation'

main_layout.register_callbacks(app)

# Server when deploy* (see `Procfile`)
server = app.server
PORT = 3000

if __name__ == '__main__':
    app.run_server(debug=True, port=PORT)