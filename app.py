import plotly_express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

#more stuff
import numpy as np
import plotly.graph_objects as go
import pandas as pd

tips = px.data.tips()
col_options = [dict(label=x, value=x) for x in tips.columns]

dimensions = ["State", "Emotion"]
emotions =  ['help', 'medical_emergency', 'health', 'hygiene', 'fear', 'death',
       'negative_emotion', 'sadness', 'nervousness', 'confusion', 'war',
       'fight', 'healing', 'movement', 'leisure', 'fun', 'positive_emotion',
       'optimism', 'sympathy', 'family', 'government', 'modi', 'economics',
       'business', 'occupation']
states = ['Bihar', 'Delhi', 'Telengana', 'Madhya_Pradesh', 'Haryana', 'Uttarakhand',
        'Andhra_Pradesh',  'Maharashtra', 'Orissa', 'Tamil_Nadu', 'West_Bengal', 'Karnataka',
        'Punjab', 'Jammu_and_Kashmir', 'Uttar_Pradesh', 'Gujarat', 'Rajasthan', 'Assam', 'Kerala']
emotions_options = [dict(label=x.replace("_"," "), value=x) for x in emotions]
states_options = [dict(label=x.replace("_"," "), value=x) for x in states]

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div( 
    [
        html.H1("Psychometric Analysis of Twitter in India during COVID-19 Times"),
        html.Div(
            [
                html.P(["State" + ":", dcc.Dropdown(id="State", options=states_options)]),
            ],
            style={"width": "25%", "float": "left","margin-right":"2cm"},
        ),
        html.Div(
                [
                    html.P(["Emotion" + ":", dcc.Dropdown(id="Emotion", options=emotions_options)])
                ],
                style={"width": "25%", "float": "left"},
            ),
        html.Div(
            [html.Div(style={"margin-bottom":"3cm"}),
            dcc.Graph(id="radar", style={"width": "50%", "display": "inline-block"}),
            dcc.Graph(id="line", style={"width": "50%", "display": "inline-block"}),
            dcc.Graph(id="xcorr", style={"width": "50%", "display": "inline-block","align":"center"})]
            
        )
    ],
    style={"margin-left":"100px","margin-right":"100px","margin-top":"50px"}
)


@app.callback([Output("radar", "figure"),Output("line", "figure"),Output("xcorr", "figure")], [Input(d, "value") for d in dimensions])
def make_figure(State, Emotion):
    print(State,Emotion)
    empath_df = pd.read_csv('./India March Tweets.csv')
    empath_fig = px.line_polar(empath_df, r='empath', theta='cats', line_close=True,title='State Wise Empath Analysis')
    emotion_df = pd.read_csv('Andhra.csv')
    if Emotion == None:
        Emotion = "help"
    emotion_fig = px.line(emotion_df, x="date", y=Emotion, title='Time Series of Emotion')
    xcorr_df = pd.read_csv('andhra_xcor.csv')
    xcorr_fig = px.line(xcorr_df, x="lag", y="Andhra_"+Emotion, title='Cross Correlation of Emotion')
    # emotion_fig = go.Figure(data=go.Scatter(x=emotion_df["date"], y=emotion_df[Emotion]))
    return empath_fig,emotion_fig,xcorr_fig

if __name__ == "__main__":
    app.run_server(debug=False,host= '0.0.0.0')
