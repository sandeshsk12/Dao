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

c1,c2,c3=st.columns((20,40,40))
dao_name_l = c2.selectbox(
    'Which DAO would you like to know about ?',
    ('MetricsDAO', 'Biconomy'), key='left',index=0)
dao_name_r = c3.selectbox(
    'Which DAO would you like to know about ?',
    ('MetricsDAO', 'Biconomy'), key='right',index=1)

st.write('You selected : {} and {}'.format(dao_name_l,dao_name_r))
st.write(" github link of project : https://github.com/sandeshsk12/Dao)
dao_overview, Community, project_metrics, governance = st.tabs(['**DAO overview**','**Community**','**Tokenomics**','**Governance**'])








with dao_overview:
    st.markdown(grey_card(title='What Is Biconomy? ',text=
    """
    What is Biconomy?<br>
    Biconomy envisions building the web3 infra that will help onboard the next billion users. The Biconomy DAO invites community members & $BICO \
    token holders to participate via decision making, creating awareness, supporting web3 builders, and discussing new features. Learn more about \
    Biconomy DAO: https://biconomy.notion.site/Welcome-to-Biconomy-DAO-d87669823cb84e98878174b6d10fd65e
    """
    ),unsafe_allow_html=True)
    
    st.markdown(grey_card(title='What Is MetricsDAO? ',text=
    """
    What is MetricsdDao? <br>
    MetricsDAO is the dao for web3 data and analytics. Leveraging hundreds of talented analysts, it enables the creation of on-demand blockchain \
    analytics at scale, with the speed and flexibility this space needs to succeed. Read more: https://docs.metricsdao.xyz/
    """
    ),unsafe_allow_html=True)

with Community:

    ######### Current twitter followers
    c1,c2,c3=st.columns((20,40,40))
    twitter_df=pd.read_csv('twitter_log.csv')
    dao_twitter_l=twitter_df[twitter_df['Dao Name']==dao_name_l].sort_values(by='Date',ascending=False)
    dao_twitter_l.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_twitter_l['Followers'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Twitter followers",
        #delta = {'position': "bottom", 'reference': round(float(dao_twitter_l['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout(height=250, width=600)
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    c2.plotly_chart(fig,use_container_width=True)

    dao_twitter_r=twitter_df[twitter_df['Dao Name']==dao_name_r].sort_values(by='Date',ascending=False)
    dao_twitter_r.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_twitter_r['Followers'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Twitter followers",
        #delta = {'position': "bottom", 'reference': round(float(dao_twitter_l['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout(height=250, width=600)
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    c3.plotly_chart(fig,use_container_width=True)


    fig = go.Figure(go.Indicator(
    mode = "number",
    value = round(float(dao_twitter_l['Following'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter Following",
    #delta = {'position': "bottom", 'reference': round(float(dao_twitter_l['Following'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
    mode = "number",
    value = round(float(dao_twitter_r['Following'][0]),3),
    # delta=1,
    # number = {'suffix': "%"},
    title="Twitter Following",
    #delta = {'position': "bottom", 'reference': round(float(dao_twitter_r['Following'][1]),3)},
    domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c3.plotly_chart(fig,use_container_width=True)

    discord_df=pd.read_csv('discord_log.csv')
    dao_discord_l=discord_df[discord_df['Dao Name']==dao_name_l].sort_values(by='Date',ascending=False)
    dao_discord_l.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_discord_l['Total users'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Discord community",
        #delta = {'position': "bottom", 'reference': round(float(dao_discord_l['Total users'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
    fig.update_layout(height=260, width=600)
    c2.plotly_chart(fig,use_container_width=True)

    discord_df=pd.read_csv('discord_log.csv')
    dao_discord_r=discord_df[discord_df['Dao Name']==dao_name_r].sort_values(by='Date',ascending=False)
    dao_discord_r.reset_index(inplace=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(dao_discord_r['Total users'][0]),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Discord community",
        #delta = {'position': "bottom", 'reference': round(float(dao_discord_r['Total users'][1]),3)},
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
    discord_dist_l=pd.read_csv('dao_discord_dist/{}_dist.csv'.format(dao_name_l))
    # Dao/dao_discord_dist/MetricsDao_dist.csv
    discord_dist_l.columns=['sl.no','Role','Percent']
    
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

    discord_dist_r=pd.read_csv('dao_discord_dist/{}_dist.csv'.format(dao_name_r))
    # Dao/dao_discord_dist/MetricsDao_dist.csv
    discord_dist_r.columns=['sl.no','Role','Percent']
    
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
    dao_number_df=pd.read_csv('dao_details.csv')
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
        st.markdown(grey_card(title='Biconomy tokenization model ',text=
        """
        What is the Biconomy token? <br>
        $BICO is the native work & governance token of the Biconomy multi-chain relayer infrastructure. Its total supply is 1 billion, and 115M of it \
        curculating according to the latest data available as of January 2023. Over 38% of the BICO supply is allocated to community members as rewards and \
        incentives (on a 47-month release schedule), compared to 32% combined to the foundation and team and advisors (on a 3-year vesting schedule). \
        Read more here: https://medium.com/biconomy/bico-token-economics-b33ff71f673d
            """
        ),unsafe_allow_html=True)
        st.markdown(grey_card(title='MetricsDAO tokenization model ',text=
        """
        What is the MetricsDao token? <br>
        xMETRIC is a beta token of MetricsDAO. It does not have any monetary value and not transferrable, and only used as on-chain \
        immutable proof of early participation in the DAO. xMETRIC tokens are not now, and will never be, transferrable, nor do they confer any \
        rights whatsoever to holders of xMETRIC tokens (including but not limited to voting rights; governance rights; or rights to any profits, \
        losses or distributions of any person, organization, DAO or other entity or group). Learn more about xMETRIC: https://docs.metricsdao.xyz/metricsdao/xmetric
        """
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
        New_vs_existing_users_df=pd.read_csv('RRR/nve_users.csv')
        New_vs_existing_users_df_l=New_vs_existing_users_df[New_vs_existing_users_df['dao_name']==dao_name_l]
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



        ######## stickiness ratio
        stickiness_ratio_df=pd.read_csv('RRR/stickiness_ratio.csv')
        stickiness_ratio_df_l=stickiness_ratio_df[stickiness_ratio_df['dao_name']==dao_name_l]
        stickiness_ratio_df_l.fillna(0,inplace=True)
    
        stickiness_ratio_df_l['date']=pd.to_datetime(stickiness_ratio_df_l['date'])
        # stickiness_ratio_df=stickiness_ratio_df.resample(dao_metrics_period[0], on='date').mean()
        color=['#fa750f','#ebb186']
        stickiness_ratio_trend_l=px.line(stickiness_ratio_df_l,x=stickiness_ratio_df_l.index,y=stickiness_ratio_df_l['stickiness_ratio'], color_discrete_sequence=color)
        stickiness_ratio_trend_l.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        stickiness_ratio_trend_l.update_layout(
        title="Stickiness ratio",
        xaxis_title="Date",
        yaxis_title="Ratio",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        c1.plotly_chart(stickiness_ratio_trend_l,use_container_width=True)
                ######## stickiness ratio
        stickiness_ratio_df_r=stickiness_ratio_df[stickiness_ratio_df['dao_name']==dao_name_r]
        stickiness_ratio_df_r.fillna(0,inplace=True)
    
        stickiness_ratio_df_r['date']=pd.to_datetime(stickiness_ratio_df_r['date'])
        # stickiness_ratio_df=stickiness_ratio_df.resample(dao_metrics_period[0], on='date').mean()
        color=['#4287f5','#84aff5'] 
        stickiness_ratio_trend_r=px.line(stickiness_ratio_df_r,x=stickiness_ratio_df_r.index,y=stickiness_ratio_df_r['stickiness_ratio'], color_discrete_sequence=color)
        stickiness_ratio_trend_r.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        stickiness_ratio_trend_r.update_layout(
        title="Stickiness ratio",
        xaxis_title="Date",
        yaxis_title="Ratio",
        font=dict(
            color="White"
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True))
        c2.plotly_chart(stickiness_ratio_trend_r,use_container_width=True)
        
    
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
        st.markdown(grey_card(title='Biconomy governance model ',text=
        """
        Biconomy DAO’s governance process enables proposals around grants, and the distribution of funding for them. Currently only $25k+ grants go \
        through this governance process, while smaller amounts are managed via the Biconomy Rapid Grants Ecosystem. Biconomy DAO governance utilizes the \
        stack including: Discord for preliminary conversations, Discourse forum where BICO token holders can submit Biconomy Grant Proposals with the help of a \
        Biconomy steward, Snapshot for consensus voting based on BICO token holdings (1 BICO = 1 vote), and finally a multisig Treasury wallet for payouts that \
        successfully pass the vote with a quorum\
        (~13% i.e. 15M of circulating supply of BICO). Learn more: https://biconomy.notion.site/Biconomy-DAO-Governance-Voting-Process-ecf64e6e9c53415aa0d79c0f37cf95ae
        """
        ),unsafe_allow_html=True)
        st.markdown(grey_card(title='MetricsDAO governance model ',text=
        """
        MetricsDAO utilizes a Discourse and Snapshot stack for voting, gated by Contributor and Governor badges for the respective season of the DAO. \
        Any DAO member who holds the contributor badge can post a proposal to the forum, which will start a 48 hour period for feedback.After 48 hours, \
        if there is no feedback that would stop the proposal, a poll is posted on Snapshot for all eligible pod contributors to vote on. If it passes, \
        the proposal will move to the Governing Council for ratification. If a DAO member holds the governor badge in addition to the contributor badge, \
        they must also post a proposal on the forum for feedback, but can bypass the Snapshot poll as long as there is no opposition on the forum. \
        These proposals will be sent directly from the forum to the Governance Council to \
        ratify and vote on. Learn more: https://docs.metricsdao.xyz/metricsdao/constitution#article-ii-operations
        """
        ),unsafe_allow_html=True)
        c1,c2=st.columns((70,30))
        proposal_trend=pd.read_csv('governance/proposal_trend.csv')
        proposal_trend_l=proposal_trend[proposal_trend['Name']==dao_name_l]  
        proposal_trend_l['date']=pd.to_datetime(proposal_trend_l['date'])
        
        proposal_trend_l=proposal_trend_l.resample(gov_period[0], on='date').sum()
        color=['#fa750f','#ebb186']
        proposal_trend_fig_l=px.bar(proposal_trend_l,x=proposal_trend_l.index,y=proposal_trend_l['NUMBER_OF_PROPOSALS'], color_discrete_sequence=color)
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


        past_prop=pd.read_csv('governance/total_number_of_proposals_past.csv')
        past_prop_l=past_prop[past_prop['Name']==dao_name_l]
        fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(past_prop_l['NUMBER_OF_PROPOSALS']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Past {} proposals".format(dao_name_l),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        fig.update_layout(height=260, width=600)
        c2.plotly_chart(fig,use_container_width=True)

        ongoin_proposals_l=pd.read_csv('governance/number_of_ongoing_proposals.csv')
        try: 
            ongoin_proposals_l=ongoin_proposals_l[ongoin_proposals_l['Name']==dao_name_l]
            fig = go.Figure(go.Indicator(
                mode = "number",
                value = round(float(ongoin_proposals_l['NUMBER_OF_PROPOSALS']),3),
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

        ongoin_proposal_list=pd.read_csv('governance/ongoing_proposals.csv')
        
        st.subheader('Ongoing {} proposals'.format(dao_name_l))
        try:
            ongoin_proposal_list_l=ongoin_proposal_list[ongoin_proposal_list['Name']==dao_name_l]
            st.dataframe(ongoin_proposals_l[['PROPOSAL_TITLE','PROPOSAL_TEXT','VOTING_START','VOTING_ENDS']])
        except:
            st.subheader('No ongoing proposals')
        
        c1,c2=st.columns((70,30))
        proposal_trend=pd.read_csv('governance/proposal_trend.csv')
        proposal_trend_r=proposal_trend[proposal_trend['Name']==dao_name_r]  
        proposal_trend_r['date']=pd.to_datetime(proposal_trend_r['date'])
        
        proposal_trend_r=proposal_trend_r.resample(gov_period[0], on='date').sum()
        color=['#4287f5','#84aff5'] 
        proposal_trend_fig_r=px.bar(proposal_trend,x=proposal_trend_r.index,y=proposal_trend_r['NUMBER_OF_PROPOSALS'], color_discrete_sequence=color)
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


        past_prop=pd.read_csv('governance/total_number_of_proposals_past.csv')
        past_prop_r=past_prop[past_prop['Name']==dao_name_r]
        fig = go.Figure(go.Indicator(
        mode = "number",
        value = round(float(past_prop_r['NUMBER_OF_PROPOSALS']),3),
        # delta=1,
        # number = {'suffix': "%"},
        title="Past {} proposals".format(dao_name_r),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(25,25,25,255)',})
        fig.update_layout(height=260, width=600)
        c2.plotly_chart(fig,use_container_width=True)

        ongoin_proposals=pd.read_csv('governance/number_of_ongoing_proposals.csv')
        try: 
            ongoin_proposals_r=ongoin_proposals[ongoin_proposals['Name']==dao_name_r]
            fig = go.Figure(go.Indicator(
                mode = "number",
                value = round(float(ongoin_proposals_r['NUMBER_OF_PROPOSALS']),3),
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

        ongoin_proposal_list=pd.read_csv('governance/ongoing_proposals.csv')
        st.subheader('Ongoing {} proposals'.format(dao_name_r))
        try:
            ongoin_proposal_list_r=ongoin_proposal_list[ongoin_proposal_list['Name']==dao_name_r]
            st.dataframe(ongoin_proposal_list_r[['PROPOSAL_TITLE','PROPOSAL_TEXT','VOTING_START','VOTING_ENDS']])
        except:
            st.subheader('No ongoing proposals')
        components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)


        st.title('Voter analysis')

        c1,c2=st.columns((30,70))
        proposal_trend=pd.read_csv('governance/voting_prop_trend.csv')
        proposal_trend_l=proposal_trend[proposal_trend['Name']==dao_name_l]  
        proposal_trend_l['date']=pd.to_datetime(proposal_trend_l['date'])
        
        proposal_trend_l=proposal_trend_l.resample(gov_period[0], on='date').sum()
        color=['#fa750f','#ebb186']
        proposal_trend_fig_l=px.bar(proposal_trend_l,x=proposal_trend_l.index,y=proposal_trend_l['NUMBER_OF_VOTERS'], color_discrete_sequence=color)
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



        voting_power_dist=pd.read_csv('governance/voting_power.csv')
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




        proposal_trend_fig_l=px.line(proposal_trend_l,x=proposal_trend_l.index,y=proposal_trend_l['RATIO'], color_discrete_sequence=color)
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

        
        
        proposal_trend_r=proposal_trend[proposal_trend['Name']==dao_name_r]  
        proposal_trend_r['date']=pd.to_datetime(proposal_trend_r['date'])
        
        proposal_trend_r=proposal_trend_r.resample(gov_period[0], on='date').sum()
        color=['#4287f5','#84aff5'] 
        proposal_trend_fig_r=px.bar(proposal_trend_r,x=proposal_trend_r.index,y=proposal_trend_r['NUMBER_OF_VOTERS'], color_discrete_sequence=color)
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

        voting_power_dist=pd.read_csv('governance/voting_power.csv')
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
        proposal_trend_fig_r=px.line(proposal_trend_r,x=proposal_trend_r.index,y=proposal_trend_r['RATIO'], color_discrete_sequence=color)
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
    








