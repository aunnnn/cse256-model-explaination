import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from enum import Enum
import base64
import pandas as pd
import plotly.graph_objs as go

from analysis import global_vars

from components.UserReviewComponent import UserReviewComponent

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css',
    '/assets/main.css','https://codepen.io/chriddyp/pen/bWLwgP.css',
]

external_scripts = [
    'https://code.jquery.com/jquery-3.4.1.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js',
    '/assets/main.js',
]

#### New classification components
wordle_url = 'https://raw.githubusercontent.com/saideepreddy91/Statistical-NLP/master/wordle_256_final_project.png'

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

GraphOne = dcc.Graph(
        id='life-exp-vs-gdp',
        figure = {
          "data": [
            {
              "values": [0.39606122622995155, 0.39035861598803323, 0.2135801577820151 ],
              "labels": [
                "CRIME",
                "POLITICS",
                "ENTERTAINMENT"
              ],
              "domain": {"column": 0},
              "name": "Prediction Probability",
              "hoverinfo":"label+percent+name",
              "hole": .4,
              "type": "pie"
            },
            {
              "values": [27, 11, 25, 8, 1, 3, 25],
              "labels": [
                "Feature 1",
                "Feature 2",
                "Feature 3",
                "Feature 4",
                "Feature 5",
                "Feature 6",
                "Rest"
              ],
              #"text":["IV"],
              "textposition":"inside",
              "domain": {"column": 1},
              "name": "IV",
              "hoverinfo":"label+percent+name",
              "hole": .4,
              "type": "pie"
            }],
          "layout": {
                "title":"Sample Donut/Pie Chart",
                "grid": {"rows": 1, "columns": 2},
                "annotations": [
                    {
                        "font": {
                            "size": 12
                        },
                        "showarrow": False,
                        "text": "Prediction",
                        "x": 0.21,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 10
                        },
                        "showarrow": False,
                        "text": "Information Value",
                        "x": 0.805,
                        "y": 0.5
                    }
                ]
            }
        }
    )

#### End of News Classification components

class Page(Enum):
    """
    Page and Tab are the same here. Click on a tab will also change the page.
    """
    UserReview = 'review'
    NewsClassification = 'news'

    @property
    def title(self):
        if self == Page.UserReview:
            return '1. User Review'
        elif self == Page.NewsClassification:
            return '2. News Classification'
        else:
            raise ValueError('Invalid value')

    @property
    def content(self):
        if self == Page.UserReview:
            return UserReviewComponent().render()
        elif self == Page.NewsClassification:
            return html.Div([GraphOne, html.Img(src=wordle_url, title='Wordle Plot of the keywords in News Articles ', style={'align-content': 'center'}) ])
        else:
            raise ValueError('Invalid value')


pages = [Page.UserReview, Page.NewsClassification]

# Main app
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    static_folder='assets')

app.config['suppress_callback_exceptions'] = True

global_vars.initialize_global_vars()

# Root of all views
root_layout = html.Div([
    # dcc.Location(id='url', refresh=False),
    dcc.Markdown(
"""
# CSE 256 Statistical NLP: Explanation of Classifier
- Wirawit Rueopas (A53277204)
- Saideep Reddy Pakkeer (A53269319)
""",
        id='app-header-text'
    ),

    dcc.Tabs(id="tabs", value=Page.UserReview.value, children=[
        dcc.Tab(label=page.title, value=page.value) for page in pages        
    ]),

    html.Div(id='page-content'),
])

# Link Tab to URL & Content (page content, url's pathname)
@app.callback(
    Output('page-content', 'children'), 
    [Input('tabs', 'value')]
)
def display_page(tab_value):
    try:
        page = Page(tab_value)
    except ValueError as e:
        # Default page
        page = Page.UserReview
        print("Invalid Page/Tab Encountered:", e, "...Redirect to UserReview")
    return page.content

# Here we try to map url to tab, but result in circular dependency ... So just don't support other url path for now.
# @app.callback(
#     Output('tabs', 'value'),
#     [Input('url', 'pathname')]
# )
# def display_url(pathname):
#     # Default path
#     if pathname == '/':    
#         tab_value = Page.UserReview.value
#     else:
#         pathname = pathname[1:] # exclude '/'
#         tab_value = pathname
#     return tab_value

app.layout = root_layout
app.title = 'CSE 256 - Model Explanation'

# Register all page's callbacks
UserReviewComponent().register_callbacks(app)

# Can only register after render
# main_layout.register_callbacks(app)

# Server when deploy* (see `Procfile`)
server = app.server
PORT = 3000

if __name__ == '__main__':
    app.run_server(debug=True, port=PORT)