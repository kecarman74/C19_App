import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import date, datetime
from Daily_COVID_Data import GetCovidData
from app import app

new_df = GetCovidData()
df = new_df.covid_df

data_cat_dict = {
    "positive": "Cumulative Positive" ,
    "totalTestResults": "Total Tests",
    "hospitalizedCurrently": "Currently Hospitalized" ,
    "onVentilatorCurrently" :"Currently On Ventilator" ,
    "positiveIncrease": "Daily New Cases",
    "cases_per_100k": "Cases Per 100k Pop",
    "total_pos_rate":"Cumulative Test Positivity"
}

drop_items_k = data_cat_dict.keys()
drop_items_v = data_cat_dict.values()

layout_page_5 = html.Div([

    html.Div([
        # Data Category drop down
        dcc.Dropdown(
            id='select_data_type',
            options=[
                {'label': 'Cumulative Positive', 'value': 'positive'},
                {'label': 'Total Tests', 'value': 'totalTestResults'},
                {'label': 'Currently Hospitalized', 'value': 'hospitalizedCurrently'},
                {'label': 'Currently On Ventilator', 'value': 'onVentilatorCurrently'},
                {'label': 'Daily New Cases', 'value': 'positiveIncrease'},
                {'label': 'Cases Per 100k Pop', 'value': 'cases_per_100k'},
                {'label': 'Cumulative Test Positivity', 'value': 'total_pos_rate'}
            ],
            value='positive'
        )

    ],
        style={'width': '25%', 'display': 'inline-block'}),

    html.Div(html.P([html.Br()])),
    # C19 map and scatter plot
    html.Div([
        dcc.Graph(
            id='C19_Map_A'
        )
    ], style={'width': '60%', 'display': 'inline-block'}),

html.Div([
    html.P('Select a category and date above. The map will display the data for that date.'),
    html.P("Click on a state to chart data by time, hover over other states to compare.")
])

])

@app.callback(
    Output("C19_Map_A", "figure"),
    Input('select_data_type', 'value')
)
def update_output(data_type):

    df = pd.read_csv("daily_covid_data.csv")
    df = df.sort_values('date_obj')

    fig = px.choropleth(df,
                        locations="state",
                        color=data_type,
                        animation_frame="date_obj",
                        hover_name="state",
                        projection='albers usa',
                        title='SARS-CoV-2 ' + data_cat_dict[data_type] + ' By State',
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