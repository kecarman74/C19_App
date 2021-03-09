import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from Daily_COVID_Data import GetCovidData

from app import app, server
from apps import app2, app4, app5


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return app2.layout_page_2
    elif pathname == '/animate':
        return app5.layout_page_5
    elif pathname == '/variant':
        return app4.layout_page_4
    else:
        return '404-Oops, these are not the pages you are looking for'

if __name__ == '__main__':
    new_data = GetCovidData()
    app.run_server(debug=True)