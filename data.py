import pandas as pd 
import numpy as np
import plotly.express as px 
from datetime import date
today = date.today()
import os
current_directory = os.getcwd()


dao_list=['MetricsDAO','biconomy']




##### Twitter
import tweepy
# twitter_log=pd.DataFrame([],columns=['Date','Dao Name','Followers','Following'],index=None)
twitter_log=pd.read_csv('twitter_log.csv')
auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAEKQiwEAAAAACaGFqOl1LhYAkmTGKqN9%2FrrFNqc%3D47Yh8KbJE0crZ8bUtE7AS7h88iT5gJq9H3cy63zWZqGmf8DwJJ")
api = tweepy.API(auth)
for dao in dao_list:
    user_dict=(api.get_user(screen_name=dao))._json
    twitter_today=pd.DataFrame([[today,user_dict['name'],user_dict['followers_count'],user_dict['friends_count']]],columns=['Date','Dao Name','Followers','Following'])
    twitter_log=pd.concat([twitter_log,twitter_today])
file_path = os.path.join(current_directory, 'twitter_log.csv')
twitter_log=twitter_log[['Date','Dao Name','Followers','Following']]
twitter_log.to_csv(file_path)


###### Discord
import requests
import json
# discord_log=pd.DataFrame([],columns=['Date','Dao Name','Total users','Active users'])
dao_list=['metrics','biconomy']
discord_log=pd.read_csv('discord_log.csv')
for dao in dao_list:
    response_API = requests.get('https://discord.com/api/v9/invites/{}?with_counts=true&with_expiration=true'.format(dao))
#print(response_API.status_code)
    data = response_API.text
    parse_json = pd.read_json(data)

# active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
# print("Active cases in South Andaman:", active_case)
    discord_today=pd.DataFrame([[today,parse_json['guild']['name'],parse_json['approximate_member_count']['id'],parse_json['approximate_presence_count']['id']]],columns=['Date','Dao Name','Total users','Active users'])
    discord_log=pd.concat([discord_log,discord_today])
file_path = os.path.join(current_directory, 'discord_log.csv')
discord_log=discord_log[['Date','Dao Name','Total users','Active users']]
discord_log.to_csv(file_path)




##### Discord contributors
import discum
import pandas as pd 
import re


bot = discum.Client(token="ODg4NDc5MzYxOTQ5MzgwNjU4.GeGlsb.wE24X9vHaUKlvMBbgIwLEe2LMElusiakNOeg6A")

def close_after_fetching(resp, guild_id):
    if bot.gateway.finishedMemberFetching(guild_id):
        lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
        # print(str(lenmembersfetched) + ' members fetched')
        bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
        bot.gateway.close()

def get_members(guild_id, channel_id):
    bot.gateway.fetchMembers(guild_id, channel_id, keep='all', wait=1)
    bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
    bot.gateway.run()
    bot.gateway.resetSession()
    return bot.gateway.session.guild(guild_id).members.items()

def get_roles(guild_id, channel_id):
    bot.gateway.fetchMembers(guild_id, channel_id, keep='all', wait=1)
    bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
    bot.gateway.run()
    bot.gateway.resetSession()
    return bot.gateway.session.guild(guild_id).roles.items()


 
###### members
def make_member_details_dataframe(server_name,server_id,channel_id):
    # 902943676685230100,903338987022876702
    members = get_members(server_id,channel_id )
# f = open('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/res/users_att2_{}.txt'.format('new'), "w")
# for element in members:
#     f.write(str(element[0])+',')
#     for index, role in enumerate(element[1]['roles']):
#         f.write(str(role))
#         # if the current role is not the last one, add a comma after it
#         if index != len(element[1]['roles']) - 1:
#             f.write(',')
#     f.write('\n')
# f.close()

    total_data=[]
    data_row=[]
    for element in members:
        data_row.append(server_name)
        data_row.append((str(element[0])))
        for role in element[1]['roles']:
            data_row.append(role)
        total_data.append(data_row)
        data_row=[]
    member_data=pd.DataFrame(total_data)
    return member_data
###############

############### ROLES

def get_role_details_dataframe(server_name,server_id,channel_id):
    role= get_roles(server_id, channel_id)
    role_data=[]
    role_row=[]

    # f = open('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/res/r.txt', "w")
    for element in role:
        # f.write(str(element[1]['id'])+','+str(element[1]['name'])+'\n')
        role_row.append(server_name)
        role_row.append(str(element[1]['id']))
        # name=str(element[1]['name']).replace(r'[^A-Za-z0-9]', '')
        

        name = element[1]['name']
        name = re.sub(r'[^A-Za-z0-9]', '', name)

        # ).replace(r'[^A-Za-z0-9]', '')
        # print(name)
        role_row.append(name)
        role_data.append(role_row)  
        role_row=[]

    # pd.DataFrame(role_data).to_csv('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/res/mdao_role.csv')
    roles_data=pd.DataFrame(role_data,columns=['Dao','id','role'])
    return roles_data

############


# 'MetricsDao','902943676685230100','903338987022876702'

############ Merging data
def merge_data(server_name,server_id,channel_id):
    member_data=make_member_details_dataframe(server_name,server_id,channel_id)
    roles_data=get_role_details_dataframe(server_name,server_id,channel_id)

    roles_list=roles_data.set_index('id')
    roles_dict=roles_list.to_dict()
    for col in member_data.columns : 
        member_data[col] = member_data[col].str.replace(r'[^A-Za-z0-9]', '')
    #     member_roles[col] = member_roles[col].replace('None', np.NaN)
        member_data[col]=member_data[col].apply(lambda x:roles_dict['role'][x] if x in roles_dict['role'].keys() else x)
    # member_data.to_csv('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/res/mdao_data.csv')
    member_data_with_role=member_data
    return member_data_with_role,roles_data
#############



############# getting counts
def get_counts(server_name,server_id,channel_id,imp_roles):
    member_data_with_role,roles_data=merge_data(server_name,server_id,channel_id)
    role_count=[]
    role_count_row=[]
    for role in roles_data['role']:
        if role in imp_roles:
            value_count = member_data_with_role.eq(role).sum().sum()

            role_count_row.append(role)
            role_count_row.append(value_count)
            role_count.append(role_count_row)
            role_count_row=[]
    role_count_df=pd.DataFrame(role_count)
    # role_count_df.to_csv('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/res/mdao_role_count.csv')
    role_count_df[1]=100*role_count_df[1]/role_count_df[1].sum()
    return role_count_df


dao_params={
    "server_name": ['MetricsDao','Biconomy'],
    "server_id" : ['902943676685230100','692403655474937856'],
    "channel_id" : ['903338987022876702','845957610792157187'],
    "imp_roles" :
    [
        ['Verified','xMETRICMaster','Contributor','Curator','Moderator','Admin','Governor','Connected'], # metrics_dao
        ['Developer','BiconautGenerals','Biconaut']
    ],
}
dao_params=pd.DataFrame(dao_params)
# print(dao_params['server_id'])
print(dao_params)
print(dao_params.iloc[0,1])


for i in range(len(dao_params)):
    res=(get_counts(dao_params.iloc[i,0],dao_params.iloc[i,1],dao_params.iloc[i,2],dao_params.iloc[i,3]))
    res.to_csv('dao_discord_dist/{}_dist.csv'.format(dao_params.iloc[i,0]))




############## 