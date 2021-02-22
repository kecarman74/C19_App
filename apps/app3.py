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

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

layout_page_3 = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='C19_Map'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='by_state_by_day2'),
    ], style={'display': 'inline-block', 'width': '49%'}),


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
                      width=1100,
                      height=800,
                      margin=dict(
                          l=10,
                          r=10,
                          b=100,
                          t=100,
                          pad=1),
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


@app.callback(
    dash.dependencies.Output('by_state_by_day2', 'fig2'),
    dash.dependencies.Input('C19_Map', 'hoverData'))

def update_plot_2(hoverData):

    #check if we have hoverdata, if not default to oregon
    if (hoverData):
        state = hoverData['points'][0]['location']
    else:
        state = 'OR'

    df2 = df[df['state'] == state]

    fig2 = px.line(df2, x="date", y="positive", title='Cases by date in ' + state)

    fig2.update_layout(title=dict(font=dict(size=28), x=0.5, xanchor='right'),
                      autosize=False,
                      width=500,
                      height=300,
                      margin=dict(
                          l=10,
                          r=10,
                          b=10,
                          t=10,
                          pad=1),
                      paper_bgcolor="LightSteelBlue",
                      )
    fig2.show()

