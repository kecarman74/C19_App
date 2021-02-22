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

layout_page_2 = html.Div([

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

    # date picker
    html.Div([dcc.DatePickerSingle(
        id='date_picker',
        min_date_allowed=datetime.strptime(str(df['date'].min()), '%Y%m%d'),
        max_date_allowed=datetime.strptime(str(df['date'].max()), '%Y%m%d'),
        date=datetime.strptime(str(df['date'].max()), '%Y%m%d')
    ),
        html.Div(id='output-container-date-picker-single')
    ]),

    # C19 map and scatter plot
    html.Div([
        dcc.Graph(
            id='C19_Map'
        )
    ], style={'width': '60%', 'display': 'inline-block'}),

    # click and hover graphs
    html.Div([
        dcc.Graph(id='by_state_by_day'),
        dcc.Graph(id='by_state_by_day2'),
    ], style={'display': 'inline-block', 'width': '40%', 'height': '20%'}),

html.Div([
    html.P('Select a category and date above. The map will display the data for that date.'),
    html.P("Click on a state to chart data by time, hover over other states to compare.")
])

])



# Page 2 callbacks
@app.callback(
    Output("C19_Map", "figure"),
    [Input('date_picker', 'date'),
    Input('select_data_type', 'value')]
)
def update_output(date_selected, data_type):
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
                        color=data_type,
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
    Output('by_state_by_day2', 'figure'),
    [Input('C19_Map', 'clickData'),
     Input('C19_Map', 'hoverData'),
     Input('select_data_type', 'value')])
def update_bottom_plot(clickData, hoverData, data_type):
    # check if we have clickData, if not default to oregon
    if (hoverData):
        state1 = hoverData['points'][0]['location']
    else:
        state1 = 'OR'

    if (clickData):
        state2 = clickData['points'][0]['location']
    else:
        state2 = 'CA'

    state = [state1, state2]

    df2 = df[df.state.isin(state)]

    pd.options.mode.chained_assignment = None  # default='warn'

    fig = px.line(df2, x="date_obj", y='positiveIncrease', color='state',
                  hover_data={"date": True,
                              "date_obj": False,
                              "positive": True,
                              "totalTestResults": True},
                  title='Daily New Cases by Date in ' + state1 + " & " + state2)
    fig.update_xaxes(
        title="Date",
        dtick="M1",
        tickformat="%b\n%Y")

    fig.update_layout(hovermode='x unified')

    fig.update_layout(title=dict(font=dict(size=28), x=0.5, y=0.9, xanchor='center', yanchor='top'),
                      autosize=False,
                      width=700,
                      height=400,
                      margin=dict(
                          l=0,
                          r=10,
                          b=10,
                          t=100,
                          pad=1),
                      paper_bgcolor="LightSteelBlue",
                      )
    return fig


@app.callback(
        Output('by_state_by_day', 'figure'),
        [Input('select_data_type', 'value'),
        Input('C19_Map', 'clickData'),
        Input('C19_Map', 'hoverData'),
])
def update_top_plot(data_type='positive', clickData='OR', hoverData='CA'):
    # check if we have clickData, if not default to oregon
    if (hoverData):
        state1 = hoverData['points'][0]['location']
    else:
        state1 = 'OR'

    if (clickData):
        state2 = clickData['points'][0]['location']
    else:
        state2 = 'CA'

    state = [state1, state2]

    df2 = df[df.state.isin(state)]
    pd.options.mode.chained_assignment = None  # default='warn'

    fig = px.line(df2, x="date_obj", y=data_type, color='state',
                  hover_data={"date": True,
                              "date_obj": False},
                  title='Map Data by Date in ' + state1 + ' & ' + state2)
    fig.update_xaxes(
        title="Date",
        dtick="M1",
        tickformat="%b\n%Y")

    fig.update_layout(hovermode='x unified')

    fig.update_layout(title=dict(font=dict(size=28), x=0.5, y=0.9, xanchor='center', yanchor='top'),
                      autosize=False,
                      width=700,
                      height=400,
                      margin=dict(
                          l=0,
                          r=10,
                          b=10,
                          t=100,
                          pad=1),
                      paper_bgcolor="LightSteelBlue",
                      )
    return fig
