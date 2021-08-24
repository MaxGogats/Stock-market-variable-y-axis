import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html

from pandas_datareader import data as web 
from datetime import datetime as dt

app = dash.Dash('Hello World',
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div(children = [
    html.H4(children='Stock Market Tracker with Variable Y-axis'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],  
        value='COKE'
    ),

    dcc.Dropdown(
        id='currency-dropdown',
        options=[
            {'label': 'Bitcoin', 'value': 'BTC-USD'},
            {'label': 'Ethereum', 'value': 'ETH-USD'},
            {'label': 'US Dollars', 'value': 'USD'},
            {'label': 'Gold', 'value': 'GOLD'},
        ],
        value='USD'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})

# need to retrieve data for selected stock and the price of selected currency
# convert price of stock to reflect the price of selected currency and display

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')], [Input('currency-dropdown', 'value')])
def update_graph(selected_dropdown_value, selected_currency_value):
    df = web.DataReader(
        selected_dropdown_value,
        'yahoo',
        dt(2017, 1, 1), 
        dt.now()
    )   
    
    non_USD_currency_data = web.DataReader(
        selected_currency_value,
        'yahoo', 
        dt(2017, 1, 1), 
        dt.now()
    )

    if selected_currency_value == 'USD':
        return {
        'data': [{
            'x': df.index, # represents the time 
            'y': df.Close  # closing price data
        }], 
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    } 
    
    else : 
        converted_prices = []
        for usd_price, new_currency_price in zip(df.Close, non_USD_currency_data.Close):
            converted_prices.append(usd_price / new_currency_price) 
        
        return {
        'data': [{
            'x': df.index, # represents the time 
            'y': converted_prices  # closing price data
        }], 
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }
            

        
 

if __name__ == '__main__':
    app.run_server()