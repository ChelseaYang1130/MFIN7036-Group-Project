#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob
import os
import pyarrow.parquet as pq
import plotly.graph_objects as go

import dash
from dash import dcc
import dash_bootstrap_components as dbc

from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from wordcloud import WordCloud


# In[2]:


## heatindex Wallstreetbets_topic
    
products = ['ChatGPT', 'Sora', 'Gemini']
companies = ['NVDA','AMD','Microsoft','Google','OpenAI']
subreddits = ['NVDA', 'OpenAi']


# In[3]:


text_data_ai= pq.read_table('data/bets_ai_search.pq').to_pandas()['cbody'][:1000].str.cat()
text_data_nvda = pq.read_table('data/bets_nvda_search.pq').to_pandas()['cbody'][:1000].str.cat()


# In[4]:


# Sentimen score data 
df = pd.read_parquet("output/data_sample_3w_output.pq") 

topic_data = {
}
for i in subreddits:
    topic_data[i] = list(df[df['subreddit']==i]['Polarity'])


# In[5]:


# Sample stock price data (replace with actual data)
stock_data = pd.read_parquet("output/stock_price.parquet")


# In[6]:


bet_topics = list(set(df[df['subreddit']=="WSB"]['topic']))


# i want to generate a data dashboard with python plotly. the dashboard contains the following elements:
# 1) a timeseries plot with stock prices; 2) word cloud, i need a button to choose the a topic; 3) timeseries of specific topic, i need a button to choose the topic

# In[61]:


SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}


# In[62]:


content_first_row = dbc.Row(
    [html.H4(
    "What did people say the amost about AI topics?", className="bg-primary text-white p-2 mb-2 text-center"
    )])
content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='word-cloud'), md=12
        )
#         ,
#         dbc.Col(
#             dcc.Graph(id='graph_2'), md=4
#         )
    ]
)
header2 = dbc.Row(
    [html.H4(
    "Popularity Index and Stock Price over time", className="bg-primary text-white p-2 mb-2 text-center"
    )]
)


content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='product-polularity-index-timeseries-plot'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='company-polularity-index-timeseries-plot'), md=6,
        )
    ]
)
header3 = dbc.Row(
    [html.H4(
    "Investor Sentiment over time", className="bg-primary text-white p-2 mb-2 text-center"
    )]
)


# In[63]:


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}



# Create the controls card
controls = dbc.Card(
    [
        html.P('Topics for word cloud\n (Public sentiment)', style={'textAlign': 'center'}),
#         html.P('(Public sentiment)', style={'textAlign': 'center'}),
        dbc.Card(
            [
            dbc.Checklist(
                id='WallStreetBets-topic',
                options=[{'label': x, 'value': x} for x in ['NVDA','AI']],
                value=['NVDA'],
#                 inline=True
            )]
        ),
         html.Br(),
        html.P('AI Company', style={'textAlign': 'center'}),
        dbc.Card(
            dbc.Checklist(
                id='company-dropdown',
                options=[{'label': x, 'value': x} for x in companies],
                value=['NVDA'],
#                 inline=True
            )
        ),
        html.Br(),
        html.P('AI Product', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='product-dropdown',  # Unique ID for the AI product dropdown
            options=[{'label': x, 'value': x} for x in products],
            value=['ChatGPT'],  # Default value
            multi=False
        ),
        html.P('Subreddit', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='subreddit-dropdown',  # Unique ID for the subreddit dropdown
            options=[{'label': x, 'value': x} for x in subreddits],
            value=['NVDA'],  # Default value
            multi=False
        )
        
       
    ],
    body=True
)


# In[68]:


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

content = html.Div(
    [
        html.H2('Public and Investor Sentiment in AI Industry', style=TEXT_STYLE),
        html.H3('by Reddit Comment Analysis', style={'textAlign': 'center','color': '#111111'}),
        html.H5('Group FINIX', style={'textAlign': 'center','color': '#111111'}),
        html.Hr(),
        content_first_row,
        content_second_row,
        header2,
        content_third_row,
        header3
#         ,
#         content_fourth_row
    ],
    style=CONTENT_STYLE
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)
app.layout = html.Div([sidebar, content])


# In[69]:


# pip show dash-bootstrap-components
@app.callback(
    Output('word-cloud', 'figure'),
    Input('WallStreetBets-topic', 'value')
)
def update_word_cloud(selected_topic):
    # Generate word cloud
    if selected_topic =="AI":
        wordcloud = WordCloud(background_color = 'white',width=800, height=400).generate(text_data_ai)
    elif selected_topic =="NVDA":
        wordcloud = WordCloud(background_color = 'white',width=800, height=400).generate(text_data_nvda)
    else: 
        wordcloud = WordCloud(background_color = 'white',width=800, height=400).generate(text_data_ai)
    fig = px.imshow(wordcloud, title='Word Cloud')
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='white',  # Change paper background color to white
        plot_bgcolor='white',   # Change plot background color to white
        font=dict(family='Arial', size=12, color='White')
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

# Callback to update topic-specific timeseries plot
@app.callback(
    Output('product-polularity-index-timeseries-plot', 'figure'),
    Input('product-dropdown', 'value')
)
def update_topic_timeseries_plot(selected_product):
    # 创建图表
    grouped = pd.read_parquet('output/HeatOutput/Wallstreetbets_topic/HeatData_bets_{}.parquet'.format(selected_product[0]))
    fig = go.Figure()

    # 添加 heat index 曲线
    fig.add_trace(go.Scatter(x=grouped.index, y=grouped['heat_index'], mode='lines', name='Heat Index', line=dict(color='firebrick')))

    # 添加 Close 曲线
    fig.add_trace(go.Scatter(x=grouped.index, y=grouped['Close'], mode='lines', name='Close', yaxis='y2', line=dict(color='royalblue')))

    # 设置布局
    fig.update_layout(title='AI Product: {}'.format(selected_product[0]),
                      xaxis=dict(title='Time', tickangle=45),
                      yaxis=dict(title='Popularity Index', side='left', showgrid=False, zeroline=False, color='firebrick'),
                      yaxis2=dict(title='Stock Price', side='right', overlaying='y', showgrid=False, zeroline=False, color='royalblue'))

    # 显示图表
    fig.show()
    return fig

# Callback to update topic-specific timeseries plot
@app.callback(
    Output('company-polularity-index-timeseries-plot', 'figure'),
    Input('company-dropdown', 'value')
)
def update_topic_timeseries_plot_company(selected_company):
    # 创建图表
    if selected_company =="OpenAI":
        grouped = pd.read_parquet('output/HeatOutput/Subreddit/HeatData_bets_OpenAi.parquet')
    else:
        grouped = pd.read_parquet('output/HeatOutput/Wallstreetbets_topic/HeatData_bets_{}.parquet'.format(selected_company[0]))
    fig = go.Figure()

    # 添加 heat index 曲线
    fig.add_trace(go.Scatter(x=grouped.index, y=grouped['heat_index'], mode='lines', name='Heat Index', line=dict(color='firebrick')))

    # 添加 Close 曲线
    fig.add_trace(go.Scatter(x=grouped.index, y=grouped['Close'], mode='lines', name='Close', yaxis='y2', line=dict(color='royalblue')))

    # 设置布局
    fig.update_layout(title='AI Company: {}'.format(selected_company[0]),
                      xaxis=dict(title='Time', tickangle=45),
                      yaxis=dict(title='Popularity Index', side='left', showgrid=False, zeroline=False, color='firebrick'),
                      yaxis2=dict(title='Stock Price', side='right', overlaying='y', showgrid=False, zeroline=False, color='royalblue'))

    # 显示图表
    fig.show()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)


# In[ ]:




