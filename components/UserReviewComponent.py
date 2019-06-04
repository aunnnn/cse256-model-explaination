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

display_mode_dropdown_options = [
    ('Prediction Contribution', FeatureDisplayMode.prediction_contribution.value), 
    ('Feature Weight', FeatureDisplayMode.feature_weight.value),
    ('TF-IDF', FeatureDisplayMode.raw_feature_tfidf.value)
]

input_initial_value = "Came in for some good after a long day at work. Some of the food I wanted wasn't ready, and I understand that, but the employee Bianca refused to tell"
#'Insert your favorite review here!'

class UserReviewComponent(BaseComponent):
    """
    Part 1: User Review
    """
    def render(self, props=None):
        stores = html.Div([
            dcc.Store(id='text_input', storage_type='memory'),
            dcc.Store(id='sp_data', storage_type='memory'),
        ])
        return Container([
            Grid([
                stores,
                Row([
                    dcc.Markdown(header_md_text),
                ]),
                Row([
                    MultiColumn(2, html.H3('Input:')),
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
                    ])),
                ]),
                Row([
                    MultiColumn(16, dcc.Graph(
                        id='coef-weight-graph',
                        config={ 
                            'displayModeBar': False,
                            # 'staticPlot': True,
                    }))
                ]),
                html.Div(className="ui divider"),
                Row([
                    MultiColumn(2, Row([
                        dcc.Markdown('### Sentiment Prediction:'),
                        html.H4('Show Top-K', id='top-k-slider-label'),
                        dcc.Slider(
                            id='sp-top-k-slider',
                            min=1,
                            max=20,
                            step=1,
                            value=3,
                            marks={
                                1: {'label': '1'},
                                20: {'label': '20'}
                            }
                        )
                    ])),
                    MultiColumn(14, Row([
                        dcc.Graph(
                            id='sentiment-prediction-graph',
                            config={
                                'displayModeBar': False,
                            }
                        ),
                    ])),
                ]),
                html.Div(className="ui divider"),
                
            ])
        ])

    def register_callbacks(self, app):

        ########################################
        # MEMORY DATA 
        ########################################
        @app.callback(
            Output('text_input', 'data'),
            [Input('input-text', component_property='value')],
            [State('text_input', 'data')])
        def on_raw_input_text_update(raw_input_text, data):
            # existing_text = data.get('preprocessed_input', '')
            new_text = model_analysis.preprocess(raw_input_text)
            return new_text

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

        @app.callback(Output('top-k-slider-label', 'children'), [Input('sp-top-k-slider', 'value')])
        def update_top_k_slider_label(top_k_value):
            return f'Show Top-{top_k_value} features'

        @app.callback(
            Output('sentiment-prediction-graph', 'figure'),
            [
                Input('sp_data', 'data'),
                Input('sp-top-k-slider', 'value')
            ]
        )
        def on_sp_data_update(sp_data, top_k_value):
            if sp_data is None:
                return {}
            return model_analysis.part1_create_sentiment_prediction_figure(sp_data, top_k=top_k_value)

        @app.callback(
            [
                Output('coef-weight-graph', 'figure'),
                Output('sorted-features', 'children'),
                Output('prediction-output', 'children'),
                Output('sp_data', 'data'),
            ],
            [
                Input('text_input', 'data'),
                Input('weight-display-mode', 'value')
            ]
        )
        def on_enter_input_text_show_weights(text_input, display_mode):
            preprocessed_input = text_input

            try:
                display_mode = FeatureDisplayMode(display_mode)
                result = model_analysis.part1_analyze_coefficients(preprocessed_input, display_mode=display_mode)
            except Exception as error:
                print("Error:", error, "with args:", error.args)
                return {}, html.Div(error.args[0]), None, None

            figure_fc = result['figure_feature_contribution']
            sp_data = result['sp_data']

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
            sentiment_icon_class = None
            sentiment_label = None
            if prob_x[1] >= 0.7:
                sentiment_icon_class = 'smile' 
                sentiment_label = 'POSITIVE'
            elif prob_x[1] >= 0.4:
                sentiment_icon_class = 'meh'
                sentiment_label = 'MEH'
            else:
                sentiment_icon_class = 'frown'
                sentiment_label = 'NEGATIVE'

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
                    sentiment_label,
                    user_sentiment_icon,
                    ], className='label'),
            ], 
            className=prediction_div_classname,
            style={
                'display': 'block',
            })
            return figure_fc, detected_feature_tags_div, prediction_output_div, sp_data