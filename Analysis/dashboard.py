#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
import glob
import os
import pyarrow.parquet as pq


# In[55]:


df


# In[65]:


df = pd.read_parquet('output/data_sample_3w_output.pq')
df = df.rename(columns={'time':'Date'})
df['Date'] = [x.strftime("%Y-%m-%d") for x in df['Date']]
folder_path = "/Users/chelseayeung/Documents/MFIN7036-Group-Project/Analysis/stock_data"
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

stock_data = []
for csv_file in csv_files:
    stock_df = pd.read_csv(csv_file)[['Date','Close']]
    company_name = csv_file.split("/")[-1].strip(".csv")
    stock_df = stock_df.rename(columns={"Close":company_name+"_stockprice"})
#     stock_df['Date'] = [x.strftime("%Y-%m-%d") for x in df['Date']]

#     stock_df['company'] = csv_file.split("/")[-1].strip(".csv")
#     stock_data.append(stock_df)
    df = df.merge(stock_df,how="left",on="Date")
# stock_price = pd.concat(stock_data)


# In[66]:


df


# In[67]:


table=pq.read_table('data/Chatgpt_sample.pq').to_pandas()
text_data= table['cbody'][:1000].str.cat()


# In[73]:


# Sample stock price data (replace with actual data)
stock_data = stock_price[stock_price['company']=='ORCL']
stock_data = stock_data.rename(columns={'Close':'StockPrice'})
# Sample text data for word cloud (replace with actual text data)
table=pq.read_table('data/Chatgpt_sample.pq').to_pandas()
text_data= table['cbody'][:1000].str.cat()

# Sample topic-specific data (replace with actual data)
topics = list(set(df['subreddit']))

topic_data = {
}
for i in topics:
    topic_data[i] = list(df[df['subreddit']==i]['Polarity'])

stock_data = df[['Date','Polarity','ORCL_stockprice', 'MSFT_stockprice', 'AMD_stockprice',
       'NVDA_stockprice', 'IBM_stockprice', 'GOOG_stockprice']]


# In[72]:





# In[69]:


def update_stock_price_plot(relayoutData):
    # Update stock price plot based on user interaction (if needed)
    fig = px.line(stock_data, x='Date', y='StockPrice', title='Stock Prices Over Time')
    
    # Add a second y-axis for sentiment score
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['SentimentScore'], 
                             mode='lines+markers', name='Sentiment Score', yaxis='y2'))
    
    # Update layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color='black'),
        yaxis=dict(title='Stock Price'),
        yaxis2=dict(title='Sentiment Score', overlaying='y', side='right')
    )
    
    return fig


# In[41]:


import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from wordcloud import WordCloud
import pandas as pd
import numpy as np


# Initialize the Dash app
app = dash.Dash(__name__)

# Define app styles
app.layout = html.Div([
    html.H1("Data Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Timeseries plot with stock prices
    dcc.Graph(
        id='stock-price-plot',
        config={'displayModeBar': False},
        style={'height': '400px'}
    ),
    
    # Word cloud
    html.Div([
        html.H3("Word Cloud", style={'textAlign': 'center'}),
        dcc.Graph(
            id='word-cloud',
            config={'displayModeBar': False},
            style={'height': '300px'}
        )
    ], style={'marginBottom': '20px'}),
    
    # Dropdown for topic selection
    html.Div([
        html.H3("Select Topic", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='topic-dropdown',
            options=[{'label': topic, 'value': topic} for topic in topics],
            value=topics[0],
            style={'width': '50%', 'margin': '0 auto'}
        ),
        dcc.Graph(
            id='topic-timeseries-plot',
            config={'displayModeBar': False},
            style={'height': '300px'}
        )
    ], style={'marginBottom': '20px'})
])

# Callback to update stock price plot
@app.callback(
    Output('stock-price-plot', 'figure'),
    Input('stock-price-plot', 'relayoutData')
)
def update_stock_price_plot(relayoutData):
    # Update stock price plot based on user interaction (if needed)
    fig = px.line(stock_data, x='Date', y='StockPrice', title='Stock Prices Over Time')
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color='black')
    )
    return fig

# Callback to update word cloud
@app.callback(
    Output('word-cloud', 'figure'),
    Input('word-cloud', 'relayoutData')
)
def update_word_cloud(relayoutData):
    # Generate word cloud
    wordcloud = WordCloud(background_color = 'white',width=800, height=400).generate(text_data)
    
    fig = px.imshow(wordcloud, title='Word Cloud')
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',  # Change paper background color to white
        plot_bgcolor='white',   # Change plot background color to white
        font=dict(family='Arial', size=12, color='black')
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

# Callback to update topic-specific timeseries plot
@app.callback(
    Output('topic-timeseries-plot', 'figure'),
    Input('topic-dropdown', 'value')
)
def update_topic_timeseries_plot(selected_topic):
    # Update timeseries plot based on selected topic
    topic_values = topic_data.get(selected_topic, [])
    fig = px.line(x=stock_data['Date'], y=topic_values, title=f"{selected_topic} Timeseries")
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color='black')
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)


# In[ ]:




