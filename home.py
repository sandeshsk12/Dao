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
pytrends = TrendReq(hl='en-US', tz=360) 




st.set_page_config(page_title="Data Explorer", layout="wide",initial_sidebar_state="collapsed")
st.markdown(f"""
<div style='text-align: center'>
<div class="card text-white bg-danger mb-3" >
  <div class="card-header"> <h2> DAO Dashboard </h2></div>    
    <p class="card-text"></p>
  </div>
  </div>
""", unsafe_allow_html=True)




option = st.selectbox(
    'Which DAO would ypou like to know about ?',
    ('MetricsDAO', 'Biconomy', 'Mobile phone'))

st.write('You selected:', option)

dao_overview, Community, project_metrics, governance = st.tabs(['**DAO overview**','**Community**','**DAO metrics**','**Governance**'])

with dao_overview:
    st.write('DAO overview')
with Community:
  twitter_df=pd.read_csv('twitter_log.csv')
  dao_twitter=twitter_df[twitter_df['Dao Name']=='MetricsDAO'].sort_values(by='Date',ascending=False)
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
  c1.plotly_chart(fig,use_container_width=True)

  fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = round(float(dao_twitter['Following'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter Following",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter['Following'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  c2.plotly_chart(fig,use_container_width=True)

  discord_df=pd.read_csv('discord_log.csv')
  dao_discord=discord_df[discord_df['Dao Name']=='MetricsDAO'].sort_values(by='Date',ascending=False)
  dao_discord.reset_index(inplace=True)
  fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = round(float(dao_discord['Total users'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Discord community",
    delta = {'position': "bottom", 'reference': round(float(dao_discord['Total users'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  c3.plotly_chart(fig,use_container_width=True)

  c1,c2=st.columns(2)
  period=c1.radio(
        label="Select timeframe",
        options=['Daily','Weekly','Monthly'],
        horizontal=True
    )
  dao_twitter['Date']=pd.to_datetime(dao_twitter['Date'])
  st.write(dao_twitter)
  dao_twitter=dao_twitter.resample(period[0], on='Date').mean()

  st.write(dao_twitter)
 
  twitter_trend=px.bar(dao_twitter,x=dao_twitter.index,y='Followers')
  twitter_trend.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(45,45,45,255)',})
  twitter_trend.update_layout(
    title="Twitter followers trend",
    xaxis_title="Date",
    yaxis_title="Followers",
    # legend_title="",
    font=dict(
        color="White"
    ))
  c1.plotly_chart(twitter_trend,use_container_width=True)
    