import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from enum import Enum

from analysis import global_vars

from components.UserReviewComponent import UserReviewComponent

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css',
    '/assets/main.css',
]

external_scripts = [
    'https://code.jquery.com/jquery-3.4.1.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js',
    '/assets/main.js',
]

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
            return html.Div('News classification page')
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
# CSE 256: Explanation of Classifier
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