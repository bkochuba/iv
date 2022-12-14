from dash import Dash, dcc, html, Output ,Input
from dataProvider import dteData_app
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


#this was the default sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
#app = Dash(__name__)

app.title = "0 DTE Options Data | SpotGamma "

server = app.server

app.layout = html.Div(

         children = [
             html.P(id='live-update-text',
                      style={'font-size': '10px'}),
             html.H2(children = 'SPX 0 DTE Metrics ',),
             html.P(
            children="Skew & Volume for 0 DTE",
            ),
        dcc.Dropdown(
                id='my-dropdown',
                options=[
                    {'label': '1%', 'value': '.01'},
                    {'label': '2%', 'value': '.02'},
                    {'label': '3%', 'value': '.03'}
                ],
                value='.01',
            style=dict(
                width='40%',
                display='table-cell',
            ),

            ),
        dcc.Graph(id='skewGraph'),
        dcc.Graph(id='volumeGraph'),
        dcc.Graph(id='oiGraph'),
        dcc.Interval(
         id='interval-component',
         interval=1 * 600000,  # in milliseconds
         n_intervals=0
        ),

    ]
)

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_date(n):
      return [html.P('Last updated ' +str(datetime.now()))]

@app.callback(Output('skewGraph', 'figure'),[Input('my-dropdown','value')])
def update_skew_graph(selected_dropdown_value):
    df = dteData_app(selected_dropdown_value)
        # strikelist = df.current_strike.to_list()
        # ivListCurrent = df.current_smvVol.to_list()
        # ivListHist = df.hist_smvVol.to_list()
        # callVolumeList = df.current_callVolume.to_list()
        # putVolumeList = df.current_putVolume.to_list()
    return{
        'data': [{
            'x': df.current_strike,
            'y': df.current_smvVol
        }],
    }

@app.callback(Output('volumeGraph', 'figure'),[Input('my-dropdown','value')])
def update_volume_graph(selected_dropdown_value):
    df = dteData_app(selected_dropdown_value)
    barchart = go.Figure(data=[
        go.Bar(name="Call Volume", x= df.current_strike.to_list(), y=df.current_callVolume.to_list()),
        go.Bar(name="Put Volume", x=df.current_strike.to_list(), y=df.current_putVolume.to_list()),

    ])
    return barchart

@app.callback(Output('oiGraph', 'figure'),[Input('my-dropdown','value')])
def update_volume_graph(selected_dropdown_value):
    df = dteData_app(selected_dropdown_value)
    barchart = go.Figure(data=[
        go.Bar(name="Call OI", x= df.current_strike.to_list(), y=df.current_callOpenInterest.to_list()),
        go.Bar(name="Put OI", x=df.current_strike.to_list(), y=df.current_putOpenInterest.to_list()),

    ])
    return barchart


if __name__ == '__main__':
    app.run_server(debug=True)

