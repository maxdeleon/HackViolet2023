import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash()

app.layout = html.Div([
    dcc.Input(id='input-1', type='text', value='initial value'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])

@app.callback(
    Output('output-state', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-1', 'value')]
)
def update_output(n_clicks, input_value):
    callback_context = dash.callback_context
    if callback_context.triggered:
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'submit-button':
            app.callback_context.set_state(input_value=input_value)
    return f'The input value is "{input_value}".'

if __name__ == '__main__':
    app.run_server(debug=True)