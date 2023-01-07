import streamlit as st 
import seaborn as sns
import plotly.express as px
from shroomdk import ShroomDK
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
import time
from plotly.subplots import make_subplots
import numpy as np 
from urllib.request import urlopen 
import json
import requests
from PIL import  Image
import plotly.graph_objects as go
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_aggrid import AgGrid
pytrends = TrendReq(hl='en-US', tz=360) 




st.set_page_config(page_title="Data Explorer", layout="wide",initial_sidebar_state="collapsed")

st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center'>
<div class="card text-white bg-danger mb-3" >
  <div class="card-header"> <h2> DAO Dashboard </h2></div>    
    <p class="card-text"></p>
  </div>
  </div>
""", unsafe_allow_html=True)



c1,c2,c3=st.columns(3)
dao_name = c2.selectbox(
    'Which DAO would ypou like to know about ?',
    ('MetricsDAO', 'Biconomy', 'Mobile phone'))

st.write('You selected:', dao_name)

dao_overview, Community, project_metrics, governance = st.tabs(['**DAO overview**','**Community**','**DAO metrics**','**Governance**'])

with dao_overview:
    st.write('DAO overview')
with Community:
  twitter_df=pd.read_csv('twitter_log.csv')
  dao_twitter=twitter_df[twitter_df['Dao Name']==dao_name].sort_values(by='Date',ascending=False)
  dao_twitter.reset_index(inplace=True)
  c1,c2,c3=st.columns(3)
  fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = round(float(dao_twitter['Followers'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter followers",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  c1.plotly_chart(fig,use_container_width=True)

  fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = round(float(dao_twitter['Following'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter Following",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter['Following'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  c2.plotly_chart(fig,use_container_width=True)

  discord_df=pd.read_csv('discord_log.csv')
  dao_discord=discord_df[discord_df['Dao Name']==dao_name].sort_values(by='Date',ascending=False)
  dao_discord.reset_index(inplace=True)
  fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = round(float(dao_discord['Total users'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Discord community",
    delta = {'position': "bottom", 'reference': round(float(dao_discord['Total users'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  c3.plotly_chart(fig,use_container_width=True)

  c1,c2,c3=st.columns(3)
  period=c2.radio(
        label="Select timeframe",
        options=['Daily','Weekly','Monthly'],
        horizontal=True,
        
    )







  c1,c2=st.columns(2)

  dao_twitter['Date']=pd.to_datetime(dao_twitter['Date'])
  dao_twitter=dao_twitter.resample(period[0], on='Date').mean()
  twitter_trend=px.bar(dao_twitter,x=dao_twitter.index,y='Followers',color_discrete_sequence=['#ff6f00'])
  twitter_trend.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  twitter_trend.update_layout(
    title="Twitter followers trend",
    xaxis_title="Date",
    yaxis_title="Followers",
    # legend_title="",
    font=dict(
        color="White"
    ))
  c1.plotly_chart(twitter_trend,use_container_width=True)



  dao_discord['Date']=pd.to_datetime(dao_discord['Date'])
  dao_discord=dao_discord.resample(period[0], on='Date').mean()
  color=['#fa750f','#ebb186']
  discord_trend=px.bar(dao_discord,x=dao_discord.index,y=['Active users','Total users'], color_discrete_sequence=color)
  discord_trend.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  discord_trend.update_layout(
    title="Discord Users trend",
    xaxis_title="Date",
    yaxis_title="Followers",
    font=dict(
        color="White"
    ))
  c2.plotly_chart(discord_trend,use_container_width=True)


  ##################
  discord_dist=pd.read_csv('dao_discord_dist/{}_dist.csv'.format(dao_name))
  # Dao/dao_discord_dist/MetricsDao_dist.csv
  discord_dist.columns=['sl.no','Role','Percent']
  c1,c2=st.columns(2)
  discord_dist_fig = go.Figure(data=[go.Pie(labels=discord_dist['Role'], values=discord_dist['Percent'], pull=[0, 0, 0.2, 0])])
  discord_dist_fig.update_traces(textinfo='label+percent',textposition='inside')
  discord_dist_fig.update_layout(height=600)
  discord_dist_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  discord_dist_fig.update_layout(
    title="Active user distribution",
    font=dict(
        color="White"
    ))
  
  c2.plotly_chart(discord_dist_fig,use_container_width=True)
  # with c1.container():
  #   # st.write("This is inside the container")
  #   # AgGrid(df, height=200) 
  #   grid=AgGrid(discord_dist,fit_columns_on_grid_load=True,columns_auto_size_mode= 'ColumnsAutoSizeMode.NO_AUTOSIZE',height=600)
  #   grid.rowHeight = 100
  #   st.image(grid, use_column_width=True)


  # # c2.image(grid)
  c1.dataframe(discord_dist[['Role','Percent']],use_container_width=True,height=600)
  c11,c12=st.columns(2)
  fig = go.Figure(go.Indicator(
    mode = "number",
    value = round(float(dao_twitter['Followers'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter followers",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  fig.update_layout(height=260, width=600)
  c11.plotly_chart(fig,use_container_width=True)
  fig = go.Figure(go.Indicator(
    mode = "number",
    value = round(float(dao_twitter['Followers'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter followers",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  fig.update_layout(height=260, width=600)
  c12.plotly_chart(fig,use_container_width=True)
  
  


    