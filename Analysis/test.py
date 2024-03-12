#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Sample data for demonstration (replace with your actual data)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
stock_prices = np.random.rand(len(dates)) * 100
topics = ['Technology', 'Finance', 'Health', 'Environment']
word_cloud_data = {'word': ['apple', 'stock', 'health', 'green', 'finance', 'technology'],
                   'count': [50, 30, 20, 40, 25, 35]}

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Data Dashboard with Plotly"),
    
    # Timeseries plot with stock prices
    dcc.Graph(id='stock-prices',
              figure=px.line(x=dates, y=stock_prices, labels={'x': 'Date', 'y': 'Stock Price'})),
    
    # Word cloud with topic selection
    dcc.Dropdown(id='topic-dropdown',
                 options=[{'label': topic, 'value': topic} for topic in topics],
                 value=topics[0]),
    dcc.Graph(id='word-cloud'),
    
    # Timeseries of specific topic with topic selection
    dcc.Dropdown(id='specific-topic-dropdown',
                 options=[{'label': topic, 'value': topic} for topic in topics],
                 value=topics[0]),
    dcc.Graph(id='specific-topic-timeseries')
])

# Callback to update word cloud based on selected topic
@app.callback(Output('word-cloud', 'figure'),
              [Input('topic-dropdown', 'value')])
def update_word_cloud(selected_topic):
    filtered_data = word_cloud_data[word_cloud_data['word'].str.contains(selected_topic)]
    return ff.create_wordcloud(filtered_data, size=(800, 400))

# Callback to update timeseries of specific topic based on selected topic
@app.callback(Output('specific-topic-timeseries', 'figure'),
              [Input('specific-topic-dropdown', 'value')])
def update_specific_topic_timeseries(selected_topic):
    # Generate sample data for demonstration
    specific_topic_data = np.random.rand(len(dates)) * 50
    return px.line(x=dates, y=specific_topic_data,
                   labels={'x': 'Date', 'y': f'{selected_topic} Score'})

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)


# In[ ]:




