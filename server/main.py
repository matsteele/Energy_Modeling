# from flask_assets import Bundle, Environment

from flask import Flask, request, render_template, url_for

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime as dt
import plotly.graph_objs as go
from make_features import DFFeatures 

# app = Flask(__name__, static_folder='../static/dist', template_folder='../templates')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# data wrangling
df = pd.read_csv('PD_challange_data_set.csv')

DataFeatures = DFFeatures(df)

def build_weekday_scatter():
    print(DataFeatures.weekday_DF_byTime.head())
    df = DataFeatures.weekday_DF_byTime
    return {
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byDate),
        "y": list(df.just_date),
        "mode": 'markers',
        "z":  list(df.electricity_usage_sum_byDate),
        "marker": dict(
            color='red',
            size=3,
            cauto=True,
            # colorscale=[[0, "rgb(230,245,254)"], [0.4, "rgb(123,171,203)"], [
            #     0.8, "rgb(40,119,174)"], [1, "rgb(37,61,81)"]],
        ),
        "scene": "scene",
        "opacity": .4,
        "scene": "scene"
    }


def build_weekend_scatter():
    df = DataFeatures.weekend_DF_byTime
    return {
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byDate),
        "y": list(df.just_date),
        "mode": 'markers',
        "z":  list(df.electricity_usage_sum_byDate),
        "marker": dict(
            color='blue',
            size=3,
            cauto=True,
            # colorscale=[[0, "rgb(230,245,254)"], [0.4, "rgb(123,171,203)"], [
            #     0.8, "rgb(40,119,174)"], [1, "rgb(37,61,81)"]],
        ),
        "scene": "scene",
        "opacity": .4,
        "scene": "scene"
    }


axis_template = {
    "showbackground": True,
    "backgroundcolor": "#141414",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
}

plot_layout = dict(
    title="electricity usage over time compared to temperature",
    font={"size": 12, "color": "grey"},
    margin=dict(l=0, r=0, b=0, t=0),
    plot_bgcolor="#141414",
    scene=dict(
        aspectmode="manual",
        aspectratio=dict(x=2, y=5, z=1.5),
    )
)

data = [
    build_weekday_scatter(),
    build_weekend_scatter()
]


dash_app.layout = html.Div(children=[
    html.Div([html.H1("ENERGY USAGE OVER TIME ")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),

    html.Div([html.H2("COMPARED TO TEMPERATURE")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph',
        figure=go.Figure(
            data=data,
            layout=plot_layout
        ),
        style={
            'height': '10%',
            'backgroundColor': "grey"
        }
    )
])


if __name__ == "__main__":
    dash_app.run_server(debug=True)


# @app.route("/<int:bars_count>/")
# def chart(bars_count):
#     if bars_count <= 0:
#         bars_count = 1

#     return render_template("chart.html", bars_count=bars_count)


# import dash
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html

# from pandas_datareader import data as web
# from datetime import datetime as dt

# app = dash.Dash('Hello World')

# app.layout = html.Div([
#     dcc.Dropdown(
#         id='my-dropdown',
#         options=[
#             {'label': 'Coke', 'value': 'COKE'},
#             {'label': 'Tesla', 'value': 'TSLA'},
#             {'label': 'Apple', 'value': 'AAPL'}
#         ],
#         value='COKE'
#     ),
#     dcc.Graph(id='my-graph')
# ], style={'width': '500'})

# @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
# def update_graph(selected_dropdown_value):
#     df = web.DataReader(
#         selected_dropdown_value,
#         'google',
#         dt(2017, 1, 1),
#         dt.now()
#     )
#     return {
#         'data': [{
#             'x': df.index,
#             'y': df.Close
#         }],
#         'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
#     }

# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# if __name__ == '__main__':
#     app.run_server()
