#Adabtive Body Area Sensor Network Monitoring Applications
#Developed by: Humayun Rashid
#Research Group: IoT for HealthCare , Department of Future Technolgoy, University of Turku

#Importing Libraries for Firebase, Dash and PLotly
import datetime
import pyrebase
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly import tools

def firebase_configuration():
    """Function to connect with Firebase and return database"""
    
    config = {
        "apiKey": "AIzaSyC41gi8ur7huhXlEzJZYqN9OmdYE98XvQQ",
        "authDomain": "raahat-demo-project.firebaseapp.com",
        "databaseURL": "https://raahat-demo-project.firebaseio.com",
        "storageBucket": "raahat-demo-project.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def dash_design():
    """Function to generate Dash App"""

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div(
        html.Div([
            html.H6('IoT for HealthCare'),
            html.Div(children='''Project Name: Adaptive Body Area Sensor Network for IoT based HealthCare'''),
            html.Div(children='''Project by: Humayun Rashid'''),
            html.Div(children='''Supervised by: Prof. Pasi Liljeberg'''),
            html.Div(id='live-update-text'),
            dcc.Graph(id='live-update-graph'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
        ])
    )
    return app

#Fetch Firebase Database 
get_firebase_database = firebase_configuration()

#Get dash layout design
get_dash_layout = dash_design()                  

#Callback trigger to run the update_metrics(n) function at an interval repeatedely" 
@get_dash_layout.callback(Output('live-update-text', 'children'),
                          [Input('interval-component', 'n_intervals')])

def update_metrics(n):
    """Live stream of humidity, Temparature, PPG,Atmospheric Pressure and Activity Data"""
    
    get_users_live = get_firebase_database.child("new_user_update").get() #Get live data dicitonary from Google Firebase 
    get_humidity = get_users_live.val()['Humidity'] # Get the value of current humidity
    get_temp =get_users_live.val()['Temp'] # Get the value of current temparature
    get_PPG=get_users_live.val()['PPG']# Get the value of current PPG
    get_prsr=get_users_live.val()['Pressure'] # Get the value of current atmospheric pressure
    get_activity=get_users_live.val()['Activity'] # Get the current activity of the user

    #Define style and return the humidity,temparauture, PPG, Pressure, Activity details.
    style = {'padding-top': '10px','padding-bottom': '20px', 'fontSize': '20px'}
    return[
        html.Span('   Humidity: {0:.2f}'.format(get_humidity), style=style),
        html.Span('   Temp: {0:.2f}'.format(get_temp),style=style),
        html.Span('   PPG: {0:.2f}'.format(get_PPG),style=style),
        html.Span('   Atmospheric Pressure: {0:.2f}'.format(get_prsr), style=style),
        html.Span('   Activity: {0:.2f}'.format(get_activity), style=style)
        ]

#Callback trigger to run the update_graph_live(n) function at an interval repeatedely" 
@get_dash_layout.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    """Function to collect information from Firebase and generate the Plotly Grpah"""
    
    # Data dictionary to store sensor data
    data = {
        'temp_key': [],
        'prsr_key': [],
        'humidity_key': [],
        'ppg_key': [],
        'humidity': [],
        'ppg':[],
        'temp': [],
        'pressure':[],
        'timestamp':[],
        'time_key':[]
        }
    
    #Fetch live PPG data from Google firebase and  update data dictinary 
    all_users_update_ppg = get_firebase_database.child("new_user/PPG").get()
    for user in all_users_update_ppg.each():
        if user.key() not in data['ppg_key']:
            data['ppg_key'].append(user.key())
            data['ppg'].append(user.val())
            
    #Fetch live Pressure data from Google firebase and  update data dictinary  
    all_users_update_pressure = get_firebase_database.child("new_user/Pressure").get()
    for user in all_users_update_pressure.each():
        if user.key() not in data['prsr_key']:
            data['prsr_key'].append(user.key())
            data['pressure'].append(user.val())

    #Fetch live Temparaute data from Google firebase and  update data dictinary  
    all_users_update_temp = get_firebase_database.child("new_user/Temp").get()
    for user in all_users_update_temp.each():
        if user.key() not in data['temp_key']:
            data['temp_key'].append(user.key())
            data['temp'].append(user.val())

    #Fetch live Humidity data from Google firebase and  update data dictinary 
    all_users_update_humidity = get_firebase_database.child("new_user/Humidity").get()
    for user in all_users_update_humidity.each():
        if user.key() not in data['humidity_key']:
            data['humidity_key'].append(user.key())
            data['humidity'].append(user.val())

    #Fetch timestamp data from Google firebase and  update data dictinary    
    all_users_update_time = get_firebase_database.child("new_user/Time").get()
    for user in all_users_update_time.each():
        if user.key() not in data['time_key']:
            data['time_key'].append(user.key())
            data['timestamp'].append(user.val())
            
    # Create the graph with subplots using stored values of Data Dictionary
    fig = plotly.tools.make_subplots(rows=4, cols=1, vertical_spacing=0.10)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 30, 't': 10}
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    
    fig.append_trace({
        'x': data['timestamp'],
        'y': data['humidity'],
        'name': 'Humidity',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1,1)
    
    fig.append_trace({
        'x': data['timestamp'],
        'y': data['temp'],
        'name': 'Temp',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    
    fig.append_trace({
        'x': data['timestamp'],
        'y': data['ppg'],
        'name': 'PPG',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)
    
    fig.append_trace({
        'x': data['timestamp'],
        'y': data['pressure'],
        'name': 'Atmospheric Pressure',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)
    return fig

#Run the Dash App Server
if __name__ == '__main__':
    get_dash_layout.run_server(debug=True)
