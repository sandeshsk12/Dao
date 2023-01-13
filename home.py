import streamlit as st 
import seaborn as sns
import plotly.express as px

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
  fig.update_layout(height=260, width=600)
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
  fig.update_layout(height=260, width=600)
  c2.plotly_chart(fig,use_container_width=True)

  discord_df=pd.read_csv('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/Dao/discord_log.csv')
  dao_discord=discord_df[discord_df['Dao Name']==dao_name].sort_values(by='Date',ascending=False)
  dao_discord.reset_index(inplace=True)
  fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = round(float(dao_discord['Total users'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},s
    title="Discord community",
    delta = {'position': "bottom", 'reference': round(float(dao_discord['Total users'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  fig.update_layout(height=260, width=600)
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


  ##### Dao numbers
  c1,c2=st.columns(2)
  dao_number_df=pd.read_csv('dao_number.csv')
  dao_name
  dao_number_df=dao_number_df[dao_number_df['dao_name']==dao_name]
  fig = go.Figure(go.Indicator(
    mode = "number",
    value = round(float(dao_number_df['number_of_sub_daos']),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Number of Sub DAOs",
    # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  fig.update_layout(height=260, width=600)
  c1.plotly_chart(fig,use_container_width=True)
  fig = go.Figure(go.Indicator(
    mode = "number",
    value = round(float(dao_number_df['Number_of_guilds']),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Number of Guilds",
    # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
  fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
  fig.update_layout(height=260, width=600)
  c2.plotly_chart(fig,use_container_width=True)


  with project_metrics:
    Reach, Retention, Revenue = st.tabs(['**Reach**','**Retention**','**Revenue**'])
  with Reach: 
    st.write('a')
  with Retention :
       ##### Dao numbers
    c1,c2,c3=st.columns(3)
    dao_metrics_period=c2.radio(
        label="Select timeframe",
        options=['Daily','Weekly','Monthly'],
        horizontal=True
        ,key='dao_metrics_period',
        index=1
        
    )
    c1,c2=st.columns(2)
    New_vs_existing_users_df=pd.read_csv('RRR/nve_users.csv')
    New_vs_existing_users_df=New_vs_existing_users_df[New_vs_existing_users_df['dao_name']==dao_name]
    New_vs_existing_users_df['date']=pd.to_datetime(New_vs_existing_users_df['date'])
    New_vs_existing_users_df=New_vs_existing_users_df.resample(dao_metrics_period[0], on='date').mean()
    color=['#fa750f','#ebb186']
    New_vs_existing_users_trend=px.bar(New_vs_existing_users_df,x=New_vs_existing_users_df.index,y=['existing_users','new_users_count'], color_discrete_sequence=color)
    New_vs_existing_users_trend.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    New_vs_existing_users_trend.update_layout(
      title="New vs existing holders",
      xaxis_title="Date",
      yaxis_title="Holders",
      font=dict(
          color="White"
      ))
    c1.plotly_chart(New_vs_existing_users_trend,use_container_width=True)


    stickiness_ratio_df=pd.read_csv('RRR/stickiness_ratio.csv')
    stickiness_ratio_df=stickiness_ratio_df[stickiness_ratio_df['dao_name']==dao_name]
    stickiness_ratio_df.fillna(0,inplace=True)
  
    stickiness_ratio_df['date']=pd.to_datetime(stickiness_ratio_df['date'])
    # stickiness_ratio_df=stickiness_ratio_df.resample(dao_metrics_period[0], on='date').mean()
    color=['#fa750f','#ebb186']
    stickiness_ratio_trend=px.line(stickiness_ratio_df,x=stickiness_ratio_df.index,y=stickiness_ratio_df['stickiness_ratio'], color_discrete_sequence=color)
    stickiness_ratio_trend.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    stickiness_ratio_trend.update_layout(
      title="Stickiness ratio",
      xaxis_title="Date",
      yaxis_title="Ratio",
      font=dict(
          color="White"
      ),
      xaxis=dict(showgrid=False),
      yaxis=dict(showgrid=True))
    c2.plotly_chart(stickiness_ratio_trend,use_container_width=True)

    stickiness_ratio_df=pd.read_csv('RRR/stickiness_ratio.csv')
    stickiness_ratio_df=stickiness_ratio_df[stickiness_ratio_df['dao_name']==dao_name]
    stickiness_ratio_df.fillna(0,inplace=True)
  
    stickiness_ratio_df['date']=pd.to_datetime(stickiness_ratio_df['date'])
    # stickiness_ratio_df=stickiness_ratio_df.resample(dao_metrics_period[0], on='date').mean()
    color=['#fa750f','#ebb186']
    stickiness_ratio_trend=px.line(stickiness_ratio_df,x=stickiness_ratio_df.index,y=stickiness_ratio_df['stickiness_ratio'], color_discrete_sequence=color)
    stickiness_ratio_trend.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    stickiness_ratio_trend.update_layout(
      title="Stickiness ratio",
      xaxis_title="Date",
      yaxis_title="Ratio",
      font=dict(
          color="White"
      ),
      xaxis=dict(showgrid=False),
      yaxis=dict(showgrid=True))
    c2.plotly_chart(stickiness_ratio_trend,use_container_width=True)
    
    



  with governance:
    c1,c2,c3=st.columns(3)
    gov_period=c2.radio(
        label="Select timeframe",
        options=['Daily','Weekly','Monthly'],
        horizontal=True
        ,key='gov_period'
        
    )


    c1,c2=st.columns((70,30))
    proposal_trend=pd.read_csv('governance/voting_prop_trend.csv')
    proposal_trend=proposal_trend[proposal_trend['Name']==dao_name]  
    proposal_trend['date']=pd.to_datetime(proposal_trend['date'])
    
    proposal_trend=proposal_trend.resample(gov_period[0], on='date').sum()
    color=['#fa750f','#ebb186']
    proposal_trend_fig=px.bar(proposal_trend,x=proposal_trend.index,y=proposal_trend['NUMBER_OF_PROPOSALS'], color_discrete_sequence=color)
    proposal_trend_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    proposal_trend_fig.update_layout(
      title="Trend of Proposals",
      xaxis_title="Date",
      yaxis_title="Proposals",
      font=dict(
          color="White"
      ),
      xaxis=dict(showgrid=False),
      yaxis=dict(showgrid=True))
    proposal_trend_fig.update_layout(height=550)
    c1.plotly_chart(proposal_trend_fig,use_container_width=True)


    past_prop=pd.read_csv('governance/total_number_of_proposals_past.csv')
    past_prop=past_prop[past_prop['Name']==dao_name]
    fig = go.Figure(go.Indicator(
      mode = "number",
      value = round(float(past_prop['NUMBER_OF_PROPOSALS']),3),
      # delta=1,
      # number = {'suffix': "%"},
      title="Past proposals",
      # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
      domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)

    ongoin_proposals=pd.read_csv('governance/number_of_ongoing_proposals.csv')
    try: 
      ongoin_proposals=ongoin_proposals[ongoin_proposals['Name']==dao_name]
      fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(ongoin_proposals['NUMBER_OF_PROPOSALS']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Ongoing proposals",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
      fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
      fig.update_layout(height=260, width=600)
      c2.plotly_chart(fig,use_container_width=True)
    except:
      fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(0),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Ongoing proposals",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
      fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
      fig.update_layout(height=260, width=600)
      c2.plotly_chart(fig,use_container_width=True)

    ongoin_proposal_list=pd.read_csv('governance/ongoing_proposals.csv')
    st.subheader('Ongoing proposals')
    try:
      st.dataframe(ongoin_proposal_list[['PROPOSAL_TITLE','PROPOSAL_TEXT','VOTING_START','VOTING_ENDS']])
    except:
      st.subheader('No ongoing proposals')

    c1,c2=st.columns((30,70))
    proposal_trend=pd.read_csv('governance/voting_prop_trend.csv')
    proposal_trend=proposal_trend[proposal_trend['Name']==dao_name]  
    proposal_trend['date']=pd.to_datetime(proposal_trend['date'])
    
    proposal_trend=proposal_trend.resample(gov_period[0], on='date').sum()
    color=['#fa750f','#ebb186']
    proposal_trend_fig=px.bar(proposal_trend,x=proposal_trend.index,y=proposal_trend['NUMBER_OF_VOTERS'], color_discrete_sequence=color)
    proposal_trend_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    proposal_trend_fig.update_layout(
      title="Trend of voters",
      xaxis_title="Date",
      yaxis_title="NUMBER_OF_VOTERS",
      font=dict(
          color="White"
      ),
      xaxis=dict(showgrid=False),
      yaxis=dict(showgrid=True))
    proposal_trend_fig.update_layout(height=350)
    c2.plotly_chart(proposal_trend_fig,use_container_width=True)
    
    
    past_prop=pd.read_csv('governance/average_duration_between_proposals.csv')
    past_prop=past_prop[past_prop['Name']==dao_name]
    fig = go.Figure(go.Indicator(
      mode = "number",
      value = round(float(past_prop['AVERAGE_DURATION_BETWEEN_PROPOSALS']),3),
      # delta=1,
      # number = {'suffix': "%"},
      title="Average duration between proposals",
      number = {'suffix': " Days"},
      # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
      domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=350, width=600)
    c1.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns((30,70))



    proposal_trend_fig=px.line(proposal_trend,x=proposal_trend.index,y=proposal_trend['RATIO'], color_discrete_sequence=color)
    proposal_trend_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    proposal_trend_fig.update_layout(
      title="Voting power per voter",
      xaxis_title="Date",
      yaxis_title="Ratio",
      font=dict(
          color="White"
      ),
      xaxis=dict(showgrid=False),
      yaxis=dict(showgrid=True))
    proposal_trend_fig.update_layout(height=350)
    c2.plotly_chart(proposal_trend_fig,use_container_width=True)

    voting_power_dist=pd.read_csv('governance/voting_power.csv')
    # st.write(voting_power_dist)
    voting_power_dist=voting_power_dist[voting_power_dist['dao_name']==dao_name]
    voting_power_dist_fig=px.violin(voting_power_dist,y='voting_power', color_discrete_sequence=color)
    voting_power_dist_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    voting_power_dist_fig.update_layout(
      title="Voting power distribution",
      # xaxis_title="Date",
      yaxis_title="Ratio",
      font=dict(
          color="White"
      ),
      xaxis=dict(showgrid=False),
      yaxis=dict(showgrid=True))
    voting_power_dist_fig.update_layout(height=720)
    c1.plotly_chart(voting_power_dist_fig,use_container_width=True)
    voting_power_dist=(voting_power_dist.sort_values(by='voting_power',ascending=False))
    voting_power_dist['percentage']=100*voting_power_dist['voting_power']/voting_power_dist['voting_power'].sum()
    # c2.write(voting_power_dist)
    c2.dataframe(voting_power_dist[['voter','voting_power','percentage']].head(5),use_container_width=True,height=450)


  


    
