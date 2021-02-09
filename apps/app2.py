import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from datetime import date, datetime

from app import app

df = pd.read_csv("daily_covid_data.csv")

layout_page_2 = html.Div([

        dcc.Graph(id='C19_Map'),
        html.Div([dcc.DatePickerSingle(
            id='date_picker',
            min_date_allowed=datetime.strptime(str(df['date'].min()), '%Y%m%d'),
            max_date_allowed=datetime.strptime(str(df['date'].max()), '%Y%m%d'),
            date=datetime.strptime(str(df['date'].max()), '%Y%m%d')
        ),
        html.Div(id='output-container-date-picker-single')
        ]),
    ])

# Page 2 callbacks
@app.callback(
    Output("C19_Map", "figure"),
    Input('date_picker', 'date')
)
def update_output(date_selected):
    df = pd.read_csv("daily_covid_data.csv")

    if len(date_selected) == 10:
        date_selected = date_selected.replace('-', '')
        date_selected = int(date_selected)
    else:
        date_selected = date_selected[:-9]
        date_selected = date_selected.replace('-', '')
        date_selected = int(date_selected)

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
                      autosize=False,
                      width=1200,
                      height=800,
                      margin=dict(
                          l=50,
                          r=50,
                          b=100,
                          t=100,
                          pad=4),
                      paper_bgcolor="LightSteelBlue",
                      )

    return fig

@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('date_picker', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        if len(date_value) > 10:
            return string_prefix + date_value[:-9]
        else:
            return string_prefix + date_value
