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
        
    data = {
        'timestamp1': [],
        'timestamp2': [],
        'timestamp3': [],
        'timestamp4': [],
        'temp':[],
        'ppg-1':[],
        'ppg-2':[],
        'acc':[],
        'used':[]
        }
    
    all_users_update_ppg = get_firebase_database.child("cloud_4").get()
    for elements in all_users_update_ppg.each():
        for a in elements.val().items():
            if a not in data['used']:
                data['used'].append(a)
                if a[0] == "Timestamp_1":
                    for element in a[1]:
                        data['timestamp1'].append(element)
                if a[0] == "Timestamp_2":
                    for element in a[1]:
                        data['timestamp2'].append(element)
                if a[0] == "Timestamp_3":
                    for element in a[1]:
                        data['timestamp3'].append(element)
                if a[0] == "Timestamp_4":
                    for element in a[1]:
                        data['timestamp4'].append(element)
                if a[0] == "PPG-1":
                    for element in a[1]:
                        data['ppg-1'].append(element)
                if a[0] == "PPG-2":
                    for element in a[1]:
                        data['ppg-2'].append(element)
                if a[0] == "Temp":
                    for element in a[1]:
                        data['temp'].append(element)
                if a[0] == "ACC":
                    for element in a[1]:
                        data['acc'].append(element)

# Create the graph with subplots using stored values of Data Dictionary
    fig = plotly.tools.make_subplots(rows=4, cols=1, vertical_spacing=0.10)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 30, 't': 10}
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    
    fig.append_trace({
        'x': data['timestamp1'],
        'y': data['temp'],
        'name': 'Temparature',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1,1)
    
    fig.append_trace({
        'x': data['timestamp2'],
        'y': data['ppg-1'],
        'name': 'PPG-1',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

     fig.append_trace({
        'x': data['timestamp3'],
        'y': data['ppg-2'],
        'name': 'PPG-2',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3,1)
    
    fig.append_trace({
        'x': data['timestamp4'],
        'y': data['acc'],
        'name': 'ACC',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 4, 1)
    return fig

#Run the Dash App Server
if __name__ == '__main__':
    get_dash_layout.run_server(debug=True)
