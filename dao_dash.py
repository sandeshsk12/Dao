import seaborn as sns
import plotly.express as px
import gspread as gs
import numpy as np
from gspread_dataframe import set_with_dataframe

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
import cred
pytrends = TrendReq(hl='en-US', tz=360) 
import streamlit as st 
import streamlit.components.v1 as components





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

def grey_card(header='',title='',text=''):
    return f"""
    <div class="card text-white bg-secondary mb-" style="margin:1rem;" >
    <div class="card-header">{header}</div>
    <div class="card-body">
    <h3 class="card-title">{title}</h3>
    <p class="card-text">{text}   
    """


gc = gs.service_account(filename='credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1wmVhR3GYJIcAvKR1j_XawVwbTI0Vmi_8K5Bv4vGGHF8/edit?usp=sharing')
ws = sh.worksheet('dao_details')
dao_details = pd.DataFrame(ws.get_all_records())







c1,c2,c3=st.columns((20,40,40))
dao_name_l = c2.selectbox(
    'Which DAO would you like to know about ?',
    dao_details['Name'], key='left',index=2)
dao_name_r = c3.selectbox(
    'Which DAO would you like to know about ?',
    dao_details['Name'], key='right',index=1)

st.write('You selected : {} and {}'.format(dao_name_l,dao_name_r))
st.write(" github link of project : https://github.com/sandeshsk12/Dao")
dao_overview, Community, project_metrics, governance = st.tabs(['**DAO overview**','**Community**','**Tokenomics**','**Governance**'])








with dao_overview:


    name = dao_name_l
    description = dao_details[dao_details['Name']==dao_name_l]['DAO 1-sentence description'].values[0]
    st.markdown(grey_card(title='What Is {}? '.format(name), text=
    """
    What is {} ? <br> {}
    """.format(name, description)
    ), unsafe_allow_html=True)

    
    name = dao_name_r
    description = dao_details[dao_details['Name']==dao_name_r]['DAO 1-sentence description'].values[0]
    st.markdown(grey_card(title='What Is {}? '.format(name), text=
    """
    What is {} ? <br> {}
    """.format(name, description)
    ), unsafe_allow_html=True)

with Community:

    ######### Current twitter followers
    c1,c2,c3=st.columns((20,40,40))
    ws = sh.worksheet('twitter_log')
    twitter_df = pd.DataFrame(ws.get_all_records())
    dao_twitter_l=twitter_df[twitter_df['Dao Name']==dao_name_l].sort_values(by='Date',ascending=False)
    dao_twitter_l.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number + delta",
        value = round(float(dao_twitter_l['Followers'][0])),
        # delta=1,
        # number = {'suffix': "%"},
        title="Twitter followers",
        delta = {'position': "bottom", 'reference': round(float(dao_twitter_l['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout(height=250, width=600)
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    c2.plotly_chart(fig,use_container_width=True)

    dao_twitter_r=twitter_df[twitter_df['Dao Name']==dao_name_r].sort_values(by='Date',ascending=False)
    dao_twitter_r.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number + delta",
        value = round(float(dao_twitter_r['Followers'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Twitter followers",
        delta = {'position': "bottom", 'reference': round(float(dao_twitter_r['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout(height=250, width=600)
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    c3.plotly_chart(fig,use_container_width=True)


    fig = go.Figure(go.Indicator(
    mode = "number + delta",
    value = round(float(dao_twitter_l['Following'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter Following",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter_l['Following'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
    mode = "number + delta",
    value = round(float(dao_twitter_r['Following'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter Following",
    delta = {'position': "bottom", 'reference': round(float(dao_twitter_r['Following'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c3.plotly_chart(fig,use_container_width=True)

    ws = sh.worksheet('discord log')
    discord_df = pd.DataFrame(ws.get_all_records())
    
    dao_discord_l=discord_df[discord_df['Dao Name']==dao_name_l].sort_values(by='Date',ascending=False)
    dao_discord_l.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number + delta",
        value = round(float(dao_discord_l['Total users'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Discord community",
        delta = {'position': "bottom", 'reference': round(float(dao_discord_l['Total users'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)

    dao_discord_r=discord_df[discord_df['Dao Name']==dao_name_r].sort_values(by='Date',ascending=False)
    dao_discord_r.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number + delta",
        value = round(float(dao_discord_r['Total users'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Discord community",
        delta = {'position': "bottom", 'reference': round(float(dao_discord_r['Total users'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c3.plotly_chart(fig,use_container_width=True)
    components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)


    c1,c2,c3=st.columns(3)
    period=c2.radio(
            label="Select timeframe",
            options=['Daily','Weekly','Monthly'],
            horizontal=True,
            
        )

    c1,c2=st.columns(2)



    dao_twitter_l['Date']=pd.to_datetime(dao_twitter_l['Date'])
    dao_twitter_l=dao_twitter_l.resample(period[0], on='Date').mean()
    twitter_trend_l=px.bar(dao_twitter_l,x=dao_twitter_l.index,y='Followers',color_discrete_sequence=['#ff6f00'])
    twitter_trend_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    twitter_trend_l.update_layout(
        title="{} Twitter followers trend".format(dao_name_l),
        xaxis_title="Date",
        yaxis_title="Followers",
        # legend_title="",
        font=dict(
            color="White"
        ))
    c1.plotly_chart(twitter_trend_l,use_container_width=True)

    dao_twitter_r['Date']=pd.to_datetime(dao_twitter_r['Date'])
    dao_twitter_r=dao_twitter_r.resample(period[0], on='Date').mean()
    twitter_trend_r=px.bar(dao_twitter_r,x=dao_twitter_r.index,y='Followers',color_discrete_sequence=['#4287f5'])
    twitter_trend_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    twitter_trend_r.update_layout(
        title="{} Twitter followers trend".format(dao_name_r),
        xaxis_title="Date",
        yaxis_title="Followers",
        # legend_title="",
        font=dict(
            color="White"
        ))
    c2.plotly_chart(twitter_trend_r,use_container_width=True)

    ######## Discord users 
    dao_discord_l['Date']=pd.to_datetime(dao_discord_l['Date'])
    dao_discord_l=dao_discord_l.resample(period[0], on='Date').mean()
    color=['#fa750f','#ebb186']
    dao_discord_l=px.bar(dao_discord_l,x=dao_discord_l.index,y=['Active users','Total users'], color_discrete_sequence=color)
    dao_discord_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    dao_discord_l.update_layout(
        title="{} Discord Users trend".format(dao_name_l),
        xaxis_title="Date",
        yaxis_title="Followers",
        font=dict(
            color="White"
        ))
    c1.plotly_chart(dao_discord_l,use_container_width=True)
    dao_discord_r['Date']=pd.to_datetime(dao_discord_r['Date'])
    dao_discord_r=dao_discord_r.resample(period[0], on='Date').mean()
    color=['#4287f5','#84aff5']
    dao_discord_r=px.bar(dao_discord_r,x=dao_discord_r.index,y=['Active users','Total users'], color_discrete_sequence=color)
    dao_discord_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    dao_discord_r.update_layout(
        title="{} Discord Users trend".format(dao_name_r),
        xaxis_title="Date",
        yaxis_title="Followers",
        font=dict(
            color="White"
        ))
    c2.plotly_chart(dao_discord_r,use_container_width=True)




    ######### discord users dist 
    c1,c2=st.columns(2)
      ##################
    ws = sh.worksheet('Discord dist')
    discord_dist = pd.DataFrame(ws.get_all_records())

    # discord_dist_l=pd.read_csv('dao_discord_dist/{}_dist.csv'.format(dao_name_l))
    # Dao/dao_discord_dist/MetricsDao_dist.csv
    discord_dist_l=discord_dist[discord_dist['dao_name']==dao_name_l]
    discord_dist_l.columns=['Role','Percent','dao_name','date']
    
    discord_dist_l_fig = go.Figure(data=[go.Pie(labels=discord_dist_l['Role'], values=discord_dist_l['Percent'], pull=[0, 0, 0.2, 0])])
    discord_dist_l_fig.update_traces(textinfo='label+percent',textposition='inside')
    discord_dist_l_fig.update_layout(height=600)
    discord_dist_l_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    discord_dist_l_fig.update_layout(
        title="Active user distribution of {}".format(dao_name_l),
        font=dict(
            color="White"
        ))
    
    c1.plotly_chart(discord_dist_l_fig,use_container_width=True)

    discord_dist_r=discord_dist[discord_dist['dao_name']==dao_name_r]
    # Dao/dao_discord_dist/MetricsDao_dist.csv
    discord_dist_r.columns=['Role','Percent','dao_name','date']
    
    discord_dist_r_fig = go.Figure(data=[go.Pie(labels=discord_dist_r['Role'], values=discord_dist_r['Percent'], pull=[0, 0, 0.2, 0])])
    discord_dist_r_fig.update_traces(textinfo='label+percent',textposition='inside')
    discord_dist_r_fig.update_layout(height=600)
    discord_dist_r_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    discord_dist_r_fig.update_layout(
        title="Active user distribution of {}".format(dao_name_r),
        font=dict(
            color="White"
        ))
    
    c2.plotly_chart(discord_dist_r_fig,use_container_width=True)

    components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)

        ##### Dao numbers
    c1,c2=st.columns(2)
    dao_number_df=dao_details.copy()
    # dao_name
    dao_number_df_l=dao_number_df[dao_number_df['Name']==dao_name_l]
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_number_df_l['number_of_sub_daos']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Number of Sub DAOs in {}".format(dao_name_l),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c1.plotly_chart(fig,use_container_width=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_number_df_l['Number_of_guilds']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Number of Guilds in {}".format(dao_name_l),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c1.plotly_chart(fig,use_container_width=True)


    # dao_name
    dao_number_df_r=dao_number_df[dao_number_df['Name']==dao_name_r]
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_number_df_r['number_of_sub_daos']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Number of Sub DAOs in {}".format(dao_name_r),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_number_df_r['Number_of_guilds']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Number of Guilds in {}".format(dao_name_r),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)


    with project_metrics:
      #hardcoded for now, will be made to change dynamically in next version.


        name = dao_name_l
        description = dao_details[dao_details['Name']==dao_name_l]['Tokenization model'].values[0]
        st.markdown(grey_card(title='{} tokenization model '.format(name),text=
        """What is the {} token? <br> {}
        """.format(name,description)
        ),unsafe_allow_html=True)
        name = dao_name_r
        description = dao_details[dao_details['Name']==dao_name_r]['Tokenization model'].values[0]
        st.markdown(grey_card(title='{} tokenization model '.format(name),text=
        """What is the {} token? <br> {}""".format(name,description)
        ),unsafe_allow_html=True)
        #Reach, Retention, Revenue = st.tabs(['**Reach**','**Retention**','**Revenue**'])
    #with Reach: 
        #st.write('a')
    #with Retention :
       ##### Dao numbers
        c1,c2,c3=st.columns(3)
        dao_metrics_period=c2.radio(
        label="Select timeframe",
        options=['Daily','Weekly','Monthly'],
        horizontal=True
        ,key='dao_metrics_period'
        ,index=1
        )

        c1,c2=st.columns(2)
        ws = sh.worksheet('nve_users')
        New_vs_existing_users_df = pd.DataFrame(ws.get_all_records())
        # New_vs_existing_users_df=pd.read_csv('Dao/RRR/nve_users.csv')

        New_vs_existing_users_df_l=New_vs_existing_users_df[New_vs_existing_users_df['dao_name']==dao_name_l]
        New_vs_existing_users_df_l.dropna(inplace=True)
        New_vs_existing_users_df_l['date']=pd.to_datetime(New_vs_existing_users_df_l['date'])
        New_vs_existing_users_df_l=New_vs_existing_users_df_l.resample(dao_metrics_period[0], on='date').mean()
        color=['#fa750f','#ebb186']
        New_vs_existing_users_trend_l=px.bar(New_vs_existing_users_df_l,x=New_vs_existing_users_df_l.index,y=['existing_users','new_users_count'], color_discrete_sequence=color)
        New_vs_existing_users_trend_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        New_vs_existing_users_trend_l.update_layout(
        title="New vs existing {} token holders".format(dao_name_l),
        xaxis_title="Date",
        yaxis_title="Holders",
        font=dict(
            color="White"
        ))
        c1.plotly_chart(New_vs_existing_users_trend_l,use_container_width=True)

        New_vs_existing_users_df_r=New_vs_existing_users_df[New_vs_existing_users_df['dao_name']==dao_name_r]
        New_vs_existing_users_df_r['date']=pd.to_datetime(New_vs_existing_users_df_r['date'])
        New_vs_existing_users_df_r=New_vs_existing_users_df_r.resample(dao_metrics_period[0], on='date').mean()
        color=['#4287f5','#84aff5'] 
        New_vs_existing_users_trend_r=px.bar(New_vs_existing_users_df_r,x=New_vs_existing_users_df_r.index,y=['existing_users','new_users_count'], color_discrete_sequence=color)
        New_vs_existing_users_trend_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        New_vs_existing_users_trend_r.update_layout(
        title="New vs existing {} token holders".format(dao_name_r),
        xaxis_title="Date",
        yaxis_title="Holders",
        font=dict(
            color="White"
        ))
        c2.plotly_chart(New_vs_existing_users_trend_r,use_container_width=True)



        # ######## stickiness ratio
        # # stickiness_ratio_df=pd.read_csv('RRR/stickiness_ratio.csv')
        # ws = sh.worksheet('stickiness_ratio')
        # stickiness_ratio_df = pd.DataFrame(ws.get_all_records())
        # stickiness_ratio_df_l=stickiness_ratio_df[stickiness_ratio_df['dao_name']==dao_name_l]
        # stickiness_ratio_df_l.fillna(0,inplace=True)
    
        # stickiness_ratio_df_l['date']=pd.to_datetime(stickiness_ratio_df_l['date'])
        # # stickiness_ratio_df=stickiness_ratio_df.resample(dao_metrics_period[0], on='date').mean()
        # color=['#fa750f','#ebb186']
        # st.write(stickiness_ratio_df_l)
        # stickiness_ratio_trend_l=px.line(stickiness_ratio_df_l,x=stickiness_ratio_df_l['date'],y=stickiness_ratio_df_l['stickiness_ratio'], color_discrete_sequence=color,range_y=[0,1])
        # stickiness_ratio_trend_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        # stickiness_ratio_trend_l.update_layout(
        # title="Stickiness percentage",
        # xaxis_title="Date",
        # yaxis_title="percentage",
        # font=dict(
        #     color="White"
        # ),
        # xaxis=dict(showgrid=False),
        # yaxis=dict(showgrid=True))
        # c1.plotly_chart(stickiness_ratio_trend_l,use_container_width=True)
        #         ######## stickiness ratio
        # stickiness_ratio_df_r=stickiness_ratio_df[stickiness_ratio_df['dao_name']==dao_name_r]
        # stickiness_ratio_df_r.fillna(0,inplace=True)
    
        # stickiness_ratio_df_r['date']=pd.to_datetime(stickiness_ratio_df_r['date'])
        # # stickiness_ratio_df=stickiness_ratio_df.resample(dao_metrics_period[0], on='date').mean()
        # color=['#4287f5','#84aff5'] 
        # stickiness_ratio_trend_r=px.line(stickiness_ratio_df_r,x=stickiness_ratio_df_r['date'],y=stickiness_ratio_df_r['stickiness_ratio'], color_discrete_sequence=color,range_y=[0,1])
        # stickiness_ratio_trend_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        # stickiness_ratio_trend_r.update_layout(
        # title="Stickiness percentage",
        # xaxis_title="Date",
        # yaxis_title="percentage",
        # font=dict(
        #     color="White"
        # ),
        # xaxis=dict(showgrid=False),
        # yaxis=dict(showgrid=True))
        # c2.plotly_chart(stickiness_ratio_trend_r,use_container_width=True)
        
    
    with governance:
        
        c1,c2,c3=st.columns(3)
        gov_period=c2.radio(
            label="Select timeframe",
            options=['Daily','Weekly','Monthly'],
            horizontal=True
            ,key='gov_period',
            index=1            
        )


    ######### proposals
        name_l = dao_name_l
        gov_model_text_l = dao_details[dao_details['Name']==dao_name_l]['Governance model in practice'].values[0]
        st.markdown(grey_card(title='{} governance model '.format(name_l),text=
        """
        {}
        """.format(gov_model_text_l)
        ),unsafe_allow_html=True)
        name_r = dao_name_r
        gov_model_text_r = dao_details[dao_details['Name']==dao_name_r]['Governance model in practice'].values[0]
        st.markdown(grey_card(title='{} governance model '.format(name_r),text=
        """
        {}
        """.format(gov_model_text_r)
        ),unsafe_allow_html=True)
        c1,c2=st.columns((70,30))

        ws = sh.worksheet('proposal_trend')
        proposal_trend = pd.DataFrame(ws.get_all_records())
        proposal_trend_l=proposal_trend[proposal_trend['dao_name']==dao_name_l]  
        proposal_trend_l['date']=pd.to_datetime(proposal_trend_l['date'])
        proposal_trend_l=proposal_trend_l.resample(gov_period[0], on='date').sum()
        color=['#fa750f','#ebb186']
        proposal_trend_fig_l=px.bar(proposal_trend_l,x=proposal_trend_l.index,y=proposal_trend_l['number_of_proposals'], color_discrete_sequence=color)
        proposal_trend_fig_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        proposal_trend_fig_l.update_layout(
        title="Trend of {} Proposals".format(dao_name_l),
        xaxis_title="Date",
        yaxis_title="Proposals",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        proposal_trend_fig_l.update_layout(height=550)
        c1.plotly_chart(proposal_trend_fig_l,use_container_width=True)


        ws = sh.worksheet('total_number_of_proposals_past')
        past_prop = pd.DataFrame(ws.get_all_records())
        past_prop_l=past_prop[past_prop['dao_name']==dao_name_l]
        fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(past_prop_l['number_of_proposals']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Past {} proposals".format(dao_name_l),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        fig.update_layout(height=260, width=600)
        c2.plotly_chart(fig,use_container_width=True)

        ws = sh.worksheet('number_of_ongoing_proposals')
        ongoin_proposals_l = pd.DataFrame(ws.get_all_records())
        
        try: 
            ongoin_proposals_l=ongoin_proposals_l[ongoin_proposals_l['dao_name']==dao_name_l]
            fig = go.Figure(go.Indicator(
                mode = "number",
                value = round(float(ongoin_proposals_l['number_of_proposals']),3),
                # delta=1,
                # number = {'suffix': "%"},
                title="Ongoing {} proposals".format(dao_name_l),
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
                title="Ongoing {} proposals".format(dao_name_l),
                # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
                domain = {'x': [0, 1], 'y': [0, 1]}))
            fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
            fig.update_layout(height=260, width=600)
            c2.plotly_chart(fig,use_container_width=True)

        ws = sh.worksheet('ongoing_proposals')
        ongoin_proposal_list = pd.DataFrame(ws.get_all_records())
                # ongoin_proposal_list=pd.read_csv('governance/ongoing_proposals.csv')
        
        st.subheader('Ongoing {} proposals'.format(dao_name_l))
        try:
            
            ongoin_proposal_list_l=ongoin_proposal_list[ongoin_proposal_list['dao_name']==dao_name_l]            
            st.dataframe(ongoin_proposal_list_l[['proposal_title','proposal_text','voting_start','voting_ends']])
        except:
            st.subheader('No ongoing proposals')
        
        c1,c2=st.columns((70,30))
        ws = sh.worksheet('proposal_trend')
        proposal_trend = pd.DataFrame(ws.get_all_records())
        # proposal_trend=pd.read_csv('governance/proposal_trend.csv')
        proposal_trend_r=proposal_trend[proposal_trend['dao_name']==dao_name_r]  
        proposal_trend_r['date']=pd.to_datetime(proposal_trend_r['date'])
        
        proposal_trend_r=proposal_trend_r.resample(gov_period[0], on='date').sum()
        color=['#4287f5','#84aff5'] 
        proposal_trend_fig_r=px.bar(proposal_trend,x=proposal_trend_r.index,y=proposal_trend_r['number_of_proposals'], color_discrete_sequence=color)
        proposal_trend_fig_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        proposal_trend_fig_r.update_layout(
        title="Trend of {} Proposals".format(dao_name_r),
        xaxis_title="Date",
        yaxis_title="Proposals",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        proposal_trend_fig_r.update_layout(height=550)
        c1.plotly_chart(proposal_trend_fig_r,use_container_width=True)


        # past_prop=pd.read_csv('governance/total_number_of_proposals_past.csv')
        past_prop_r=past_prop[past_prop['dao_name']==dao_name_r]
        fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(past_prop_r['number_of_proposals']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Past {} proposals".format(dao_name_r),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        fig.update_layout(height=260, width=600)
        c2.plotly_chart(fig,use_container_width=True)

        ws = sh.worksheet('number_of_ongoing_proposals')
        ongoin_proposals = pd.DataFrame(ws.get_all_records())        
        # ongoin_proposals=pd.read_csv('governance/number_of_ongoing_proposals.csv')
        try: 
            ongoin_proposals_r=ongoin_proposals[ongoin_proposals['dao_name']==dao_name_r]
            fig = go.Figure(go.Indicator(
                mode = "number",
                value = round(float(ongoin_proposals_r['number_of_proposals']),3),
                # delta=1,
                # number = {'suffix': "%"},
                title="Ongoing {} proposals".format(dao_name_r),
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
                title="Ongoing {} proposals".format(dao_name_r),
                # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
                domain = {'x': [0, 1], 'y': [0, 1]}))
            fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
            fig.update_layout(height=260, width=600)
            c2.plotly_chart(fig,use_container_width=True)

        ws = sh.worksheet('ongoing_proposals')
        ongoin_proposal_list = pd.DataFrame(ws.get_all_records())         
        # ongoin_proposal_list=pd.read_csv('governance/ongoing_proposals.csv')
        st.subheader('Ongoing {} proposals'.format(dao_name_r))
        try:
            ongoin_proposal_list_r=ongoin_proposal_list[ongoin_proposal_list['dao_name']==dao_name_r]            
            st.dataframe(ongoin_proposal_list_r[['proposal_title','proposal_text','voting_start','voting_ends']])
        except:
            st.subheader('No ongoing proposals')
        components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)


        st.title('Voter analysis')

        c1,c2=st.columns((30,70))
        ws = sh.worksheet('voting_prop_trend')
        proposal_trend = pd.DataFrame(ws.get_all_records())        
        # proposal_trend=pd.read_csv('governance/voting_prop_trend.csv')
        proposal_trend_l=proposal_trend[proposal_trend['dao_name']==dao_name_l]  
        proposal_trend_l['date']=pd.to_datetime(proposal_trend_l['date'])
        
        proposal_trend_l=proposal_trend_l.resample(gov_period[0], on='date').sum()
        color=['#fa750f','#ebb186']
        proposal_trend_fig_l=px.bar(proposal_trend_l,x=proposal_trend_l.index,y=proposal_trend_l['number_of_voters'], color_discrete_sequence=color)
        proposal_trend_fig_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        proposal_trend_fig_l.update_layout(
        title="Trend of {} voters".format(dao_name_l),
        xaxis_title="Date",
        yaxis_title="NUMBER_OF_VOTERS",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        proposal_trend_fig_l.update_layout(height=350)
        c2.plotly_chart(proposal_trend_fig_l,use_container_width=True)


        ws = sh.worksheet('voting_power')
        voting_power_dist = pd.DataFrame(ws.get_all_records())   
        # voting_power_dist=pd.read_csv('governance/voting_power.csv')
        # st.write(voting_power_dist)
        voting_power_dist_l=voting_power_dist[voting_power_dist['dao_name']==dao_name_l]
        voting_power_dist_fig_l=px.violin(voting_power_dist_l,y='voting_power', color_discrete_sequence=color)
        voting_power_dist_fig_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        voting_power_dist_fig_l.update_layout(
        title="Voting power distribution ({})".format(dao_name_l),
        # xaxis_title="Date",
        yaxis_title="Ratio",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        voting_power_dist_fig_l.update_layout(height=720)
        c1.plotly_chart(voting_power_dist_fig_l,use_container_width=True)




        proposal_trend_fig_l=px.line(proposal_trend_l,x=proposal_trend_l.index,y=proposal_trend_l['ratio'], color_discrete_sequence=color)
        proposal_trend_fig_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        proposal_trend_fig_l.update_layout(
        title="Voting power per voter ({})".format(dao_name_l),
        xaxis_title="Date",
        yaxis_title="Ratio",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        proposal_trend_fig_l.update_layout(height=350)
        c2.plotly_chart(proposal_trend_fig_l,use_container_width=True)

        
        
        proposal_trend_r=proposal_trend[proposal_trend['dao_name']==dao_name_r]  
        proposal_trend_r['date']=pd.to_datetime(proposal_trend_r['date'])
        
        proposal_trend_r=proposal_trend_r.resample(gov_period[0], on='date').sum()
        color=['#4287f5','#84aff5'] 
        proposal_trend_fig_r=px.bar(proposal_trend_r,x=proposal_trend_r.index,y=proposal_trend_r['number_of_voters'], color_discrete_sequence=color)
        proposal_trend_fig_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        proposal_trend_fig_r.update_layout(
        title="Trend of {} voters".format(dao_name_r),
        xaxis_title="Date",
        yaxis_title="NUMBER_OF_VOTERS",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        proposal_trend_fig_r.update_layout(height=350)
        c2.plotly_chart(proposal_trend_fig_r,use_container_width=True)

        ws = sh.worksheet('voting_power')
        voting_power_dist = pd.DataFrame(ws.get_all_records())   
        # voting_power_dist=pd.read_csv('governance/voting_power.csv')
        # st.write(voting_power_dist)
        voting_power_dist_r=voting_power_dist[voting_power_dist['dao_name']==dao_name_r]
        color=['#4287f5','#84aff5'] 
        voting_power_dist_fig_r=px.violin(voting_power_dist_r,y='voting_power', color_discrete_sequence=color)
        voting_power_dist_fig_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        voting_power_dist_fig_r.update_layout(
        title="Voting power distribution ({})".format(dao_name_r),
        # xaxis_title="Date",
        yaxis_title="Ratio",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        voting_power_dist_fig_r.update_layout(height=720)
        c1.plotly_chart(voting_power_dist_fig_r,use_container_width=True)
        color=['#4287f5','#84aff5'] 
        proposal_trend_fig_r=px.line(proposal_trend_r,x=proposal_trend_r.index,y=proposal_trend_r['ratio'], color_discrete_sequence=color)
        proposal_trend_fig_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        proposal_trend_fig_r.update_layout(
        title="Voting power per voter ({})".format(dao_name_r),
        xaxis_title="Date",
        yaxis_title="Ratio",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        proposal_trend_fig_r.update_layout(height=350)
        c2.plotly_chart(proposal_trend_fig_r,use_container_width=True)
    








