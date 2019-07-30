from flask import Flask, request, render_template, url_for

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime as dt
import plotly.graph_objs as go
from make_features import DFFeatures

dash_app = dash.Dash(__name__)

dash_app.title = "PD Challenge"

# data wrangling
df = pd.read_csv('PD_challange_data_set.csv')

DataFeatures = DFFeatures(df)

def build_weekday_scatter():
    # print(DataFeatures.weekday_DF.keys())
    df = DataFeatures.weekday_DF
    return {
        "name": "weekday total daily usage",
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byDate),
        "y": list(df.just_date),
        "mode": 'markers',
        "z":  list(df.electricity_usage_sum_byDate),
        "marker": {
            "size": 3,
            "color": list(-df.pred_diff),
            "colorscale": [[0, "blue"],
                           [0.5, "orange"],
                           [1.0,  "red"]],
            "showscale": True,
            "colorbar": {
                "outlinecolor": "#B8B8B8",
                "title": {
                    "text": "weekday usage<br>above or below<br>expected",
                    "side": "top"
                }
            }
        },
        "scene": "scene",
        "opacity": .9,
        "scene": "scene",
        "customdata": df.just_date,
    }


def build_weekday_predictions():
    df = DataFeatures.weekday_DF
    return {
        "name": "predicted values",
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byDate),
        "y": list(df.just_date),
        "mode": 'lines',
        "z":  list(df.predictions),
        "marker": {
            "color": 'orange',
            "size": 3,
        },
        "scene": "scene",
        "opacity": .5,
        "scene": "scene",
        "customdata": df.just_date,
    }


def build_weekend_scatter():
    df = DataFeatures.weekend_DF
    return {
        "name": "weekend total daily usage",
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byDate),
        "y": list(df.just_date),
        "mode": 'markers',
        "z":  list(df.electricity_usage_sum_byDate),
        "marker": {
            "symbol": "diamond",
            "size": 4,
            "color": list(-df.pred_diff),
            "colorscale": [[0, "blue"],
                           [0.5, "green"],
                           [1.0,  "red"]],
            "showscale": True,
            "colorbar": {
                "xanchor": "right",
                "outlinecolor": "#B8B8B8",
                "title": {
                    "text": "weekend usage<br>above or below<br>expected",
                    "side": "top"
                }
            }
        },
        "scene": "scene",
        "opacity": .4,
        "scene": "scene",
        "customdata": df.just_date,
    }


def build_weekend_predictions():
    df = DataFeatures.weekend_DF
    return {
        "name": "predicted values",
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byDate),
        "y": list(df.just_date),
        "mode": 'lines',
        "z":  list(df.predictions),
        "marker": {
            "color": 'green',
            "size": 3,
        },
        "scene": "scene",
        "opacity": .5,
        "scene": "scene",
        "customdata": df.just_date,
    }


def build_week_scatter():
    df = DataFeatures.base_week_data
    return {
        "name": "weekly average",
        "type": "scatter3d",
        "x": list(df.out_door_temp_mean_byWeek),
        "y": list(df.monday_of_that_week),
        "mode": 'lines',
        "z":  list(df.electricity_usage_mean_byWeek),
        "marker": {
            "color": 'purple',
            "size": 10,
        },
        "scene": "scene",
        "opacity": .9,
        "scene": "scene",
        "customdata": df.monday_of_that_week,
    }


maxTemp = DataFeatures.base_day_data.out_door_temp_mean_byDate.max()
maxUsage = DataFeatures.base_day_data.electricity_usage_sum_byDate.max()
minUsage = DataFeatures.base_day_data.electricity_usage_sum_byDate.min()

main_plot_layout = dict(
    font={"size": 12, "color": "white", "family": "sans-serif"},
    margin=dict(l=0, r=0, b=0, t=0),
    plot_bgcolor="#B8B8B8",
    paper_bgcolor="#B8B8B8",
    hovermode='closest',
    hoverlabel={
        'namelength': 10
    },
    clickmode='event+select',
    legend=dict(x=-.1, y=1.2),
    scene=dict(
        aspectmode="manual",
        aspectratio=dict(x=2, y=5, z=2.5),
        camera=dict(
            up=dict(x=0, y=0, z=.5),
            center=dict(x=-.5, y=.1, z=-1),
            eye=dict(x=4, y=1.75, z=.5)
        ),
        xaxis=dict(
            title="outdoor temp (in F)",
            nticks=6, range=[
                maxTemp*1.2, 0
            ],
            spikecolor="white",
            gridcolor="#D9D9D9",
            showbackground=False
        ),
        yaxis=dict(
            nticks=20, title="",
            spikecolor="white",
            gridcolor="#D9D9D9",
            showbackground=False
        ),
        zaxis=dict(
            title="energy usage (in kW)",
            nticks=7, range=[minUsage*.8,  maxUsage*1.2],
            spikecolor="white",
            gridcolor="#D9D9D9",
            showbackground=False
        )
    ),


)


main_chart_data = [
    build_weekday_scatter(),
    build_weekend_scatter(),
    build_week_scatter(),
    build_weekday_predictions(),
    build_weekend_predictions()
]


dash_app.layout = html.Div(
    className='row background',
    style={"max-width": "100%", "font-size": "1.5rem", "font-family": "sans-serif",
           "padding": "0px 0px", 'backgroundColor': "#B8B8B8", "margin": 0},
    children=[
        html.Div([html.H2("ENERGY USAGE OVER TIME")],
                 style={'backgroundColor': "grey", 'height': '10%', "color": "white", 'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),

        html.Div(
            className='row background',
            style={'backgroundColor': "#B8B8B8"},
            children=[
                html.Div(
                    [
                        dcc.Graph(
                            className='ten columns offset-by-one',
                            id='main-graph',
                            figure=go.Figure(
                                data=main_chart_data,
                                layout=main_plot_layout
                            ),
                            config={"displaylogo": False},
                            hoverData={'points': [{'x': 70.32895833395834, 'y': '2018-04-13T00:00:00', 'z': 67944.64000000001,
                                                   'curveNumber': 0, 'pointNumber': 436, 'customdata': '2018-04-13T00:00:00'}]}
                        )
                    ]
                ),

            ]
        ),
        html.Div([html.H4(" usage every half hour (in kW) for date : - "), html.H4(id='dateforsubgraph', )],
                 style={'backgroundColor': "grey", 'height': '5%', "color": "white",
                        'display': 'flex', 'justifyContent': "center",
                        'text-align': "center", "padding-bottom": "10", "padding-top": "10"},
                 className="row"
                 ),

        html.Div(
            style={'background-color': "#B8B8B8", "width": "100%"},
            children=[
                dcc.Graph(
                    style={'backgroundColor': "#B8B8B8", "width": "100%"},
                    className='ten columns',
                    id='sub-graph',
                    config={
                        'displayModeBar': False
                    }
                )
            ]),

    ])


def update_subgraph(hoverData):
    date_hovered = hoverData['points'][0]['customdata'][:10]

    specific_day_data = DataFeatures.base_time_data[DataFeatures.base_time_data['just_date']
                                                    == date_hovered]

    maxUsage = DataFeatures.base_time_data.electricity_usage.max()

    sub_plot_layout = dict(
        font={"size": 8, "color": "white"},
        margin=dict(l=0, r=0, b=0, t=0),
        plot_bgcolor="#B8B8B8",
        paper_bgcolor="#B8B8B8",
        height=150,
        hoverlabel=dict(
            bordercolor='white'
        ),
        yaxis=dict(
            range=[
                maxUsage*1.1, 0
            ],
        ),
    )

    sub_chart_energy_data = {
        "name": "",
        "type": "bar",
        "x": list(specific_day_data.just_time),
        "y": list(specific_day_data.electricity_usage),
        "text": list(specific_day_data.just_time),
        "marker": {
            'color': list(specific_day_data.out_door_temp),
            'colorscale': [[0.0, "rgb(20, 20, 20)"],
                           [0.5,  '#801D16'],
                           [1.0,  '#FF392B']],
            "cauto": False,
            "cmin": 35,
            "showscale": True,
            "colorbar": {
                "outlinecolor": "#B8B8B8",
                "title": {
                    "text": "farenheit",
                    "side": "top"
                }
            }
        },
        "hovertext": list(specific_day_data.out_door_temp),
        "hovertemplate": '<b>%{x}</b>  ' + '<br>%{y} kW <br>' + '%{hovertext} F',
        "textposition": "inside",
        "textfont": {
            "color": "white"
        },
        "insidetextfont": {
            "color": "white"
        },
        "insidetextanchor": "start",
        "cliponaxis": "true",
    }

    return {
        'data': [sub_chart_energy_data],
        'layout': sub_plot_layout
    }, date_hovered


@dash_app.callback([Output('sub-graph', 'figure'), Output('dateforsubgraph', 'children')],
                   [Input('main-graph', 'hoverData')])
def update_subgraph_onHover(inputData):
    output1, output2 = update_subgraph(inputData)
    return output1, output2

if __name__ == "__main__":
    dash_app.run_server(debug=True)
