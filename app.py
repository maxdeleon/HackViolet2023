import plotly.graph_objects as go # or plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State, ctx

# import plotly.express as px
# df = px.data.gapminder().query("year == 2007")

#,'./assets/'
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) #__name__, use_pages=True, 

fig = go.Figure(go.Scattergeo())

fig.update_geos(projection_type="orthographic")

fig.update_layout(
                height=750, 
                width=900,
                margin={
                        "r":0,
                        "t":5,
                        "l":0,
                        "b":5
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
    showsubunits=True, subunitcolor="Blue"
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
            dcc.Input(id="X", type="number",placeholder=1),
            dcc.Input(id="Y", type="number",placeholder=1),
            dcc.Input(id="Z", type="number",placeholder=1),
            html.Button('up', id='up_btn', n_clicks=0),
            html.Button('down', id='d_btn', n_clicks=0),
            html.Button('left', id='l_btn', n_clicks=0),
            html.Button('right', id='r_btn', n_clicks=0),
            html.Button('zin', id='zin_btn', n_clicks=0),
            html.Button('zout', id='zout_btn', n_clicks=0)

        ],
        brand_href="#",
        color="dark",
        dark=True,
    ),
    # graph
    html.Div(id='camera-data'),
    html.Center(children=[dcc.Graph(figure=fig, id='globe')]), 

    # storage
    #storage, 

    # update component
    dcc.Interval(
            id='interval-component',
            interval=10, # in milliseconds
            n_intervals=0)
    ],
    style={'backgroundColor': 'black',
            'background-image': 'url("./assets/space.png")',
            'background-size': '100%',
            'position': 'fixed',
            'width': '100%',
            'height': '100%'})


@app.callback(
    Output('camera-data', 'children'),
    Input('interval-component', 'n_intervals'),
    Input('globe', 'figure'))
def updateStateVariables(n, layout):
    layout2 = layout['layout']
    current_view = layout2['geo']['projection']
    if current_view.get('scale',None) == None:
        current_view['scale'] = 0.0
    else:
        pass
    return html.Span([str(current_view)],style={"color": "white"})

#### camera control callbacks

'''
html.Button('up', id='up_btn', n_clicks=0),
html.Button('down', id='d_btn', n_clicks=0),
html.Button('left', id='l_btn', n_clicks=0),
html.Button('right', id='r_btn', n_clicks=0),
html.Button('zin', id='zin_btn', n_clicks=0),
html.Button('zout', id='zout_btn', n_clicks=0)
'''
@app.callback(
    Output('globe', 'figure'),
    Input('up_btn','n_clicks'),
    Input('d_btn','n_clicks'),
    Input('l_btn','n_clicks'),
    Input('r_btn','n_clicks'),
    Input('globe', 'figure')
)
def move(n_clicks_up, n_clicks_down, n_clicks_left, n_clicks_right, figure):
    layout = figure['layout']
    current_view = layout['geo']['projection']
    if current_view.get('rotation', None) == None:
        current_view['rotation'] = dict(lon=0, lat=0, roll=0)
    else:
        if 'up_btn' == ctx.triggered_id:
            current_view['rotation']['lat'] += 5
        elif 'd_btn' == ctx.triggered_id:
            current_view['rotation']['lat'] -= 5
        elif 'l_btn' == ctx.triggered_id:
            current_view['rotation']['lon'] -= 5
        elif 'r_btn' == ctx.triggered_id:
            current_view['rotation']['lon'] += 5
        
    return figure




if __name__ == '__main__':
    app.run_server(host= '0.0.0.0', debug=False)
