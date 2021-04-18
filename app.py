import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import cbsodata


# Retrieve data from CBS
def retreive_data_cbs(data):
    df = pd.DataFrame(cbsodata.get_data(data))
    return df


df_price = retreive_data_cbs('83625ENG')

# Create app layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '15%',
    'padding': '20px 10px',
    'background-color': '#ECF0F1'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

# Controls
controls = dbc.FormGroup(
    [
        html.Br(),
        dcc.Markdown("Select first region:"),
        dcc.Dropdown(
            id='dropdown_1',
            options=[
                {'label': regions, 'value': regions} for regions in df_price['Regions'].unique()
            ],
            value='The Netherlands'
        ),
        html.Br(),
        dcc.Markdown("Select second region:"),
        dcc.Dropdown(
            id='dropdown_2',
            options=[
                {'label': regions, 'value': regions} for regions in df_price['Regions'].unique()
            ],
            value='The Netherlands'
        )
    ]
)

sidebar = html.Div(
    [
        html.H4(["Compare house prices in The Netherlands"]),
        html.Br(),
        dcc.Markdown("""
                    Compare Dutch house prices per country region (LD), province (PV) or municipality/city over the 
                    year 1995 until 2020.
                    """),
        dcc.Markdown("""
                        Source: [CBS Open data StatLine](https://opendata.cbs.nl/statline/)
                        """),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        html.Div([
            html.H4(dbc.Badge(id='regions_text', color="primary")),
            dcc.Graph(id='graph_1')
        ]), md=12)
])

content = dbc.Container(html.Div(
    [
        html.Br(),
        html.Br(),
        content_first_row,
    ],
    style=CONTENT_STYLE
))

app.layout = html.Div([sidebar, content])


# Create graph
@app.callback(
    Output('graph_1', 'figure'),
    Output('regions_text', 'children'),
    Input('dropdown_1', 'value'),
    Input('dropdown_2', 'value'))
def update_figure(region_1, region_2):
    filtered_df_graph_1 = df_price[df_price['Regions'].isin([region_1, region_2])]

    fig_1 = px.line(filtered_df_graph_1, x="Periods", y="AveragePurchasePrice_1", color="Regions",
                    line_shape="spline",
                    template="simple_white",
                    labels={"Periods": 'Year', "AveragePurchasePrice_1": 'Average Purchase Price'})

    return fig_1, region_1 + " and " + region_2


if __name__ == '__main__':
    app.run_server(debug=True)
