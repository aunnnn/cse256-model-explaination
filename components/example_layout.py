import dash_html_components as html
import dash_core_components as dcc
from components.utils import *

import numpy as np
import matplotlib.pyplot as plt

header_text = '''
## CSE 256: Explanation of NLP Classifier
'''

plt.figure(figsize=(3,3))
plt.plot(np.arange(10))
fig = plt.gcf()

graph = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montral'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            },
        },
)

example_layout = Container([
    Markdown(header_text),
    Row([
        MultiColumn(3, [
            html.Div(
                "Test style", className="test-style"
                )
        ]),
        MultiColumn(6, "Hello"),
        MultiColumn(3, "Hello"),
    ]),
    Row([
        MultiColumn(3, [
            TextField(id='hello', value=None, placeholder='wow')
        ]),
        MultiColumn(9, [
            graph
        ])
    ]),
    Row([
        MultiColumn(6, MatplotlibFigure(id='wow', fig=fig, size_in_pixels=(300, 200))),
        MultiColumn(6, MatplotlibFigure(id='wow-2', fig=fig, size_in_pixels=(300, 200))),
    ]),
    TextField(id='testtg', label='My textfield', placeholder='insert sth here'),
    Row([
        MultiColumn(4, Slider('my-slider', min=5, max=20, step=2, value=6, label='My slider')),
        MultiColumn(8, Slider('my-second-slider', min=0, max=20, step=1, value=0, label='My second slider')),
  
    ])
])