import plotly.graph_objects as go # or plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,'./assets/']) #__name__, use_pages=True, 
#app._favicon = "./favicon.ico"



fig = go.Figure(go.Scattergeo())

fig.update_geos(projection_type="orthographic")

fig.update_layout(
                height=750, 
                width=900,
                margin={
                        "r":0,
                        "t":0,
                        "l":0,
                        "b":0
                        })

fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
},geo=dict(bgcolor= 'rgba(0,0,0,0)'))

fig.update_geos(
    resolution=110,
    showcoastlines=False, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Green",
    showocean=True, oceancolor="DarkBlue",
    showlakes=False, lakecolor="Blue",
    showcountries=True, countrycolor="White",
    showrivers=False, rivercolor="Blue",

)

storage = html.Div([
    dcc.Store(id="Xpos", storage_type='session'),
    dcc.Store(id="Ypos", storage_type='session'),
    dcc.Store(id="Zpos", storage_type='session')
])

app.layout = html.Div([
    # navbar
    dbc.NavbarSimple( 
        children=[
            dcc.Input(id="X", type="number"),
            dcc.Input(id="Y", type="number"),
            dcc.Input(id="Z", type="number"),
            html.Div(id='coords')
        ],
        brand_href="#",
        color="dark",
        dark=True,
    ),
    # graph
    html.Center(children=[dcc.Graph(figure=fig,id='globe')]), 

    # storage
    storage, 

    # update component
    dcc.Interval(
            id='interval-component',
            interval=1*10, # in milliseconds
            n_intervals=0)
],
style={'backgroundColor': 'black'})

'''
dcc.Input(id="X", type="number"),
            dcc.Input(id="Y", type="number"),
            dcc.Input(id="Z", type="number")
            
dcc.Store(id="Xpos", storage_type='session'),
    dcc.Store(id="Ypos", storage_type='session'),
    dcc.Store(id="Zpos", storage_type='session')'''

@app.callback(
    [Input('interval-component', 'n_intervals'),
    Input('X', 'n_intervals'),
    Input('Y', 'n_intervals'),
    Input('Z', 'n_intervals')],
    [State('Xpos','value'),
    State('Ypos','value'),
    State('Zpos','value')]

    #State("hedge-table-collapse", "is_open")
)
def updateStateVariables(n, iX ,iY, iZ):

    ## get the current inputs

    ## update the memory for the current inputs
    
    ## update the graph's camera coordinates with memory

    input_coords = (iX,iY,iZ)
    print(f'Input: {input_coords}')




if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',debug=False,port=443)
