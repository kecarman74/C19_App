import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go

from app import app

df = pd.read_csv("daily_covid_data.csv")

layout_page_2 = html.Div([
        html.Div([
        dcc.Graph(id='C19_Map')
        ]),

        html.Div([html.Br()]),

        html.Div([dcc.Slider(
            id='date_slider',
            min=df['date'].min(),
            max=df['date'].max(),
            value=df['date'].max(),
            step=1
        )])
    ])

# Page 2 callbacks
@app.callback(
    [Output(component_id='C19_Map', component_property='figure')],
    [Input(component_id='date_slider', component_property='value')]
)
def update_output(date_selected, df=df):
    df = pd.read_csv("daily_covid_data.csv")
    print(date_selected)
    df.drop(df[df['date'] != date_selected].index, inplace=True)

    fig = px.choropleth(df,
                        locations="state",
                        color="positive",
                        hover_name="state",
                        projection='albers usa',
                        title='SARS-CoV-2 Data By State',
                        locationmode="USA-states",
                        color_continuous_scale=px.colors.sequential.Plasma)

    fig.update_layout(title=dict(font=dict(size=28), x=0.5, xanchor='center'),
                      margin=dict(l=60, r=60, t=50, b=50))

    fig.show()

    return fig
