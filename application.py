#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd

ma = pd.read_excel('RawData.xlsx', sheet_name = 'MA')
ma['MA'] = [1]*59
ma['BA'] = [0]*59
ba = pd.read_excel('RawData.xlsx', sheet_name = 'BA')
ba['BA'] = [1]*110
ba['MA'] = [0]*110
df = ba.append(ma, ignore_index = True)
df
#FORMER fullinclusive= [1,1,0,1,-1,1,-1,1,-1,1,0,1,-1,-1,1,-1,1,1,1,0,1,-1,1,1,0,1,1,0,-1,1,-1,1,1,1,-1,1,-1,1,1,1]
#NEW (replaces 0's with 1's)
fullinclusive= [1,1,1,1,-1,1,-1,1,-1,1,1,1,-1,-1,1,-1,1,1,1,1,1,-1,1,1,1,1,1,1,-1,1,-1,1,1,1,-1,1,-1,1,1,1]
df = df.fillna(df.mean())
df = df*fullinclusive

df= df.drop(['MA','BA', 'RE'], axis=1) 
questions = pd.read_csv('questions.csv', encoding='latin1')

change = dict(zip(df.columns.sort_values(), questions.Question))
df = df.rename(columns=change)



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import statsmodels.api as sm

app = dash.Dash(name="OUATT")
                
DATA = df

#graphe_test= px.scatter(DATA,x=DATA.x,y=DATA.y)               


def create_figure(column_x, column_y):
    return px.scatter(DATA, x=column_x, y=column_y, trendline='ols')# px.scatter(DATA,x=column_x,y=column_y)
    
app.layout = html.Div([
                       html.Button(" + Graph", id="ajout-graphe", n_clicks=0),
                       html.Div(),
                       html.Div(id='bloc_graphe', children=[]) 
                     ])

@app.callback( Output('bloc_graphe', 'children'),
               [Input('ajout-graphe', 'n_clicks')],
               [State('bloc_graphe', 'children')])

def ajouter_graphe(n_clicks, children):
    
    nouvelle_zone_graphe = html.Div(
        style={'width': '23%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
                  dcc.Graph(
                            id ={'type': 'Graphique',
                                 'index': n_clicks}
                            ),
                  
                  dcc.Dropdown(
                               id={
                                   'type':'Selection_variable_X',
                                   'index': n_clicks
                                   },
                               options=[{'label':i, 'value':i} for i in DATA.columns],
                               value = None
                              ),
                  
                  dcc.Dropdown(
                               id={
                                   'type':'Selection_variable_Y',
                                   'index': n_clicks
                                   },
                               options=[{'label':i, 'value':i} for i in DATA.columns],
                               value = None
                              ), 
                 ])
    children.append(nouvelle_zone_graphe)
    return children
 
@app.callback( Output({'type':'Graphique', 'index':MATCH},'figure'),
               [Input({'type':'Selection_variable_X', 'index':MATCH}, 'value'),
                Input({'type':'Selection_variable_Y', 'index':MATCH}, 'value')]
               
            )
def display_output(column_x,column_y):
            return create_figure(column_x, column_y)
if __name__ == '__main__':
    app.run_server(debug=False, port=8080)


# In[ ]:





# In[ ]:





# In[ ]:




