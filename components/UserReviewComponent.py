import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from components.utils import *
from components.base_component import BaseComponent
from analysis import model_analysis, global_vars
from analysis.global_vars import GLOBAL_UI_STYLES
from analysis.model_analysis import FeatureDisplayMode, map_to_new_low_and_high

import numpy as np 

header_md_text = """
## Part 1: User Review
"""

DEFAULT_USER_SENTIMENT_ICON = [
    html.I(className='user icon'),
    html.I(className='comment icon'),
]

display_mode_dropdown_options = [
    ('Prediction Contribution', FeatureDisplayMode.prediction_contribution.value), 
    ('Feature Weight', FeatureDisplayMode.feature_weight.value),
    ('TF-IDF', FeatureDisplayMode.raw_feature_tfidf.value)
]

input_initial_value = 'came in for some good after a long day at work some of the food i wanted wasnt ready and i understand that but the employee bianca refused to tell'

class UserReviewComponent(BaseComponent):
    def render(self, props=None):
        stores = html.Div([
            dcc.Store(id='memory', storage_type='memory'),
        ])
        return Container([
            Grid([
                stores,
                Row([
                    dcc.Markdown(header_md_text),
                ]),
                Row([
                    MultiColumn(2, html.H3([
                        'Input ', 
                        html.Div(DEFAULT_USER_SENTIMENT_ICON, id='user-sentiment-icon', style={'display': 'inline-block'})
                    ])),
                    MultiColumn(8, TextField(id='input-text', value=input_initial_value, placeholder='Type review here', style={
                        'min-width': '200px',
                    })),
                    MultiColumn(6, html.Div(id='prediction-output')),
                ]),
                Row([
                    MultiColumn(2, dcc.Markdown('### Tokens:')),
                    MultiColumn(14, html.Div(None, id="input-text-splitted")),
                ]),
                html.Div(className="ui divider"),
                Row([
                    MultiColumn(2, Row([
                        dcc.Markdown('### Features:'),
                    ])),
                    MultiColumn(14, Row([
                        Row([
                            MultiColumn(5, dcc.Dropdown(
                                id='weight-display-mode',
                                options=[{'label': lb, 'value': value} for lb, value in display_mode_dropdown_options],
                                value=FeatureDisplayMode.prediction_contribution.value,
                                searchable=False,
                                placeholder='Select Feature Display Type',
                            ))
                        ], style={'margin-bottom': '10px'}),
                        html.Div(None, id="sorted-features"),
                        dcc.Graph(
                        id='coef-weight-graph',
                        config={ 
                            'displayModeBar': False,
                            # 'staticPlot': True,
                        }),
                    ])),
                ]),
            ])
        ])

    def register_callbacks(self, app):

        ########################################
        # MEMORY DATA 
        ########################################
        @app.callback(
            Output('memory', 'data'),
            [Input('input-text', component_property='value')],
            [State('memory', 'data')])
        def on_raw_input_text_update(raw_input_text, data):
            # Default data
            data = data or {}

            # existing_text = data.get('preprocessed_input', '')
            new_text = model_analysis.preprocess(raw_input_text)
            data['preprocessed_input'] = new_text
            return data

        # for i in range(100):
        #     tag_id = f'splitted-text-{i}'
        #     @app.callback(
        #         Output(tag_id, 'className'),
        #         [Input(tag_id, 'n_clicks')])
        #     def on_click_tag(n_clicks):
        #         if n_clicks is not None:
        #             if n_clicks % 2 == 1:
        #                 return 'ui red label unseen'
        #             else:
        #                 return 'ui basic label'

        @app.callback(
            Output(component_id='input-text-splitted', component_property='children'),
            [
                Input(component_id='input-text', component_property='value'),
            ],
        )
        def on_enter_input_text(input_text):
            if input_text == '':
                return html.Div('Empty input text.')

            input_text = model_analysis.preprocess(input_text)
            feature_names_set = global_vars.feature_names_set

            splitted_text_tags = []
            tokens = input_text.split()
            for w in (tokens):
                is_unseen = w not in feature_names_set
                new_tag = None
                if is_unseen:
                    html_data = {'data-tooltip': f"'{w}' is not in token list", 'data-position': "top center"}
                    new_tag = html.Div(
                        children=html.Div(w, className='ui basic unseen label'),
                        style={'display': 'inline-block'},
                        **html_data,
                    )
                else:
                    new_tag = html.Div(w, className='ui basic label')

                splitted_text_tags.append(new_tag)

            return html.Div(splitted_text_tags)

        @app.callback(
            [
                Output('coef-weight-graph', 'figure'), 
                Output('sorted-features', 'children'),
                Output('prediction-output', 'children'),
                Output('user-sentiment-icon', 'children'),
            ],
            [
                Input('memory', 'data'),
                Input('weight-display-mode', 'value')
            ]
        )
        def on_enter_input_text_show_weights(data, display_mode):
            preprocessed_input = data['preprocessed_input']

            try:
                display_mode = FeatureDisplayMode(display_mode)
                result = model_analysis.part1_analyze_coefficients(preprocessed_input, display_mode=display_mode)
            except Exception as error:
                print("Error:", error, "with args:", error.args)
                return {}, html.Div(error.args[0]), None, DEFAULT_USER_SENTIMENT_ICON

            figure = result['figure']
            features = result['human_sorted_features']
            values = result['human_sorted_values']
            relative_feature_strengths = result['relative_feature_strengths']

            # DETECTED FEATURES
            feature_tags = []
            for i in range(len(features)):
                f = features[i]
                v = values[i]
                feature_strength = relative_feature_strengths[i]

                className = f'ui {GLOBAL_UI_STYLES.POSITIVE_COLOR_CLASSNAME} label' if v > 0 else f'ui {GLOBAL_UI_STYLES.NEGATIVE_COLOR_CLASSNAME} label'
                html_data = {'data-tooltip': f"{np.round(v, 2)}", 'data-position': "top center"}

                opacity = np.round(feature_strength, 2)
                font_size = np.round(map_to_new_low_and_high(feature_strength, 0, 1, 12, 20), 1)
                tag = html.Div(f, 
                    className=className, 
                    style={
                    'opacity': opacity,
                    'fontSize': font_size,
                    },
                )
                wrapper_div = html.Div(tag, style={
                    'display': 'inline-block', 
                    'margin-right': '1.7px',
                    }, 
                    **html_data)
                feature_tags.append(wrapper_div)

            detected_feature_tags_div = html.Div(feature_tags)
            
            pred_x = result['pred_x']
            prob_x = result['prob_x']


            # USER SENTIMENT ICON
            sentiment_icon_class = 'smile' if pred_x else 'frown'
            user_sentiment_icon = html.I(className=f'{sentiment_icon_class} outline icon')

            # PREDICTION OUTPUT BADGE
            color_class = GLOBAL_UI_STYLES.POSITIVE_COLOR_CLASSNAME if pred_x else GLOBAL_UI_STYLES.NEGATIVE_COLOR_CLASSNAME
            prediction_div_classname = f'ui {color_class} statistic'
            prediction_output_div = html.Div([
                html.Div([
                    f'{np.round(max(prob_x) * 100, 1)}',
                    html.I(className='mini percent icon'),
                    ], className='value'),
                html.Div([
                    'POSITIVE' if pred_x else 'NEGATIVE',
                    user_sentiment_icon,
                    ], className='label'),
            ], 
            className=prediction_div_classname,
            style={
                'display': 'block',
            })
            return figure, detected_feature_tags_div, prediction_output_div, user_sentiment_icon