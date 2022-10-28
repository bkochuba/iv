from dash import Dash, dcc, html, Output ,Input
from dataProvider import dteData_app
from datetime import datetime
import plotly.express as px


#this was the default sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
#app = Dash(__name__)

app.title = "0 DTE Options Data | SpotGamma "

server = app.server

df = dteData_app()
strikelist = df.current_strike.to_list()
ivListCurrent = df.current_smvVol.to_list()
ivListHist = df.hist_smvVol.to_list()
callVolumeList = df.current_callVolume.to_list()
putVolumeList = df.current_putVolume.to_list()
theTime = datetime.now().strftime("%Y/%m/%d %H:%m")
print(theTime)

app.layout = html.Div(

         children = [
             html.H2(children = 'SPX 0 DTE Metrics: ' +str(theTime),),
             html.P(
            children="Skew & Volume for 0 DTE",
            ),
    dcc.Graph(
        figure = {
            "data": [

                    {"x": df['current_strike'], "y": df['current_smvVol'], "type": "lines", "name":"0 DTE IV", "template":"plotly_dark"},
                    {"x": df['current_strike'], "y": df['hist_smvVol'], "type": "lines", "name":"0 DTE IV yesterday", "template":"plotly_dark"},

            ],
            "layout": {"title": "0DTE IV"},
        },

    ),
        dcc.Graph(
            figure={
                "data": [
                    {"x": df['current_strike'],"y": df['current_callVolume'],"type": "bar", "name":"0DTE Call Volume", "color":"blue", "template":"plotly_dark"},
                    {"x": df['current_strike'], "y": df['current_putVolume'], "type": "bar", "name": "0DTE Put Volume", "template":"plotly_dark"},

                ],
                "layout": {"title": "0DTE Volume"},
            },

        ),
        dcc.Interval(
         id='interval-component',
         interval=1 * 300000,  # in milliseconds
         n_intervals=0
        )

    ]
)




if __name__ == '__main__':
    app.run_server(debug=True)


