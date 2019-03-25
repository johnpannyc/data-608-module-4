# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go


def readTreeData():
	url = "https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=50000&$select=tree_id,spc_common,boroname,health,steward"
	df = pd.read_json(url)
	df.dropna(inplace=True)
	return df

def readDataFirstData():
    url = "https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5000&$" \
          "select=spc_common,health,count(spc_common),boroname&$group=spc_common,health,boroname"
    df = pd.read_json(url)
    df.dropna(inplace=True)
    return df

def getTable(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), 200))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Assignment 4"
print("Reading Data")
df = readTreeData()
overallDF = readDataFirstData()
print("Done")

species_options = []
species_options.append({'label': str("All"), 'value': "All"})
for spc_common in overallDF['spc_common'].unique():
    species_options.append({'label': str(spc_common), 'value': spc_common})

# Create a Dash layout
app.layout = html.Div([
    html.Div(
        html.H1('Assignment 4', style={'textAlign': 'center', 'color': 'Black'})
    ),
    dcc.Tabs(id="tabs", value='Tab2', style={'width': '90%',
                                             'margin': 'auto',
                                             'textAlign': 'center'
                                             }, children=[
        dcc.Tab(label='Question 1', id='tab1', value='Tab1', children=[
            dcc.Dropdown(id='species-picker-1', style={'width': '95%',
                                                       'margin': 'auto',
                                                       'textAlign': 'center'
                                                       }, options=species_options, value="All", multi=False,
                         placeholder="Select a Species of Tree")
            , html.Div(id='graph-1')
        ]),

        dcc.Tab(label='Question 2', id='tab2', value='Tab2', children=[
			html.Div([html.P('Are stewards having an impact on the health of trees?')],style={'width': '90%',
                                                       'margin': 'auto',
                                                       'textAlign': 'center'
                                                       }),
            html.Div([getTable(df)], style={'width': '90%',
                                                       'margin': 'auto',
                                                       'textAlign': 'center'
                                                       })
        ])
    ])
])


@app.callback(Output('graph-1', 'children'),
              [Input('species-picker-1', 'value')])
def update_figure_1(selected_species):
    graphs = []
    if selected_species == "All":
        filtered_df = overallDF
    else:
        filtered_df = overallDF[overallDF['spc_common'] == selected_species]
    graphs.append(html.Div(dcc.Graph(
        id=selected_species,
        figure={
            'data': [
                {'x': filtered_df[filtered_df['health'] == 'Good'].boroname,
                 'y': filtered_df[filtered_df['health'] == 'Good']['count_spc_common'], 'type': 'bar', 'name': 'Good'},
                {'x': filtered_df[filtered_df['health'] == 'Fair'].boroname,
                 'y': filtered_df[filtered_df['health'] == 'Fair']['count_spc_common'], 'type': 'bar', 'name': 'Fair'},
                {'x': filtered_df[filtered_df['health'] == 'Poor'].boroname,
                 'y': filtered_df[filtered_df['health'] == 'Poor']['count_spc_common'], 'type': 'bar', 'name': 'Poor'},
            ],
            'layout': {
                'title': 'Data Visualization ' + selected_species + ' Tree Species'
            }
        }
    )))
    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)
