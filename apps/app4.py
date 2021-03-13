import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from app import app

df = pd.read_csv("daily_variant_data.csv")

layout_page_4 = html.Div([

    html.Div([
        # Data Category drop down
        dcc.Dropdown(
            id='select_data_type',
            options=[
                {'label': 'B.1.1.7 Variant ', 'value': 'B.1.1.7 Variant '},
                {'label': 'P.1 Variant ', 'value': 'P.1 Variant '},
                {'label': 'B.1.351 Variant ', 'value': 'B.1.351 Variant '}
            ],
            value='B.1.1.7 Variant ',
            style ={'color': 'black'}
        )

    ],
        style={'width': '25%', 'display': 'inline-block'}),

    html.Div(html.P([html.Br()])),

    # C19 variant
    html.Div([
        dcc.Graph(
            id='C19_Map_V'
        )
    ], style={'width': '60%', 'display': 'inline-block'}),

html.Div([
    html.P('Select a variant strain to view a US heat map.'),
    html.P("Hover over a state to view cumulative variant case count.")
])

])

# Page 4 callbacks
@app.callback(
    Output("C19_Map_V", "figure"),
    Input('select_data_type', 'value')
)
def update_output_variant(data_type):
    df = pd.read_csv("daily_variant_data.csv")

    fig = px.choropleth(df,
                        locations="State",
                        color=data_type,
                        hover_name="State",
                        projection='albers usa',
                        title='SARS-CoV-2 ' + data_type + ' Variant Cumulative Cases By State',
                        locationmode="USA-states",
                        hover_data=["B.1.1.7 Variant ", "P.1 Variant ", "B.1.351 Variant "],
                        color_continuous_scale=px.colors.sequential.Plasma)

    fig.update_layout(template='plotly_dark', title=dict(font=dict(size=28), x=0.5, xanchor='center'),
                      autosize=False,
                      width=1100,
                      height=800,
                      margin=dict(
                          l=10,
                          r=10,
                          b=100,
                          t=100,
                          pad=1)
                      )

    return fig
