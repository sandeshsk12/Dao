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
    