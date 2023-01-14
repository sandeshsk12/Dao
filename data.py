import pandas as pd 
import numpy as np
import plotly.express as px 
from datetime import date
today = date.today()
import os
from shroomdk import ShroomDK

sdk = ShroomDK("00dba474-bd21-4d4d-a9b9-c5eaa08aac33")
current_directory = os.getcwd()
dao_details=pd.read_csv('dao_details.csv')
print(dao_details.columns)
dao_list=dao_details['Name']





##### Twitter
import tweepy
# twitter_log=pd.DataFrame([],columns=['Date','Dao Name','Followers','Following'],index=None)
twitter_log=pd.read_csv('twitter_log.csv')
auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAEKQiwEAAAAACaGFqOl1LhYAkmTGKqN9%2FrrFNqc%3D47Yh8KbJE0crZ8bUtE7AS7h88iT5gJq9H3cy63zWZqGmf8DwJJ")
api = tweepy.API(auth)
# print(dao_list)
for dao in dao_list:
    print(dao_details['Name'])
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


bot = discum.Client(token="MzkwNDkzMjU1MTY4Njg4MTI4.G4Kv2i.qegt36LwQEMdqGN1_e7jNAL2LYsR6jrwg7Jxbw")

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
    "server_name": ['MetricsDAO','Biconomy'],
    "server_id" : ['902943676685230100','692403655474937856'],
    "channel_id" : ['903338987022876702','845957610792157187'],
    "imp_roles" :
    [
        ['Verified','xMETRICMaster','Contributor','Curator','Moderator','Admin','Governor','Connected'], # metrics_dao
        ['Developer','BiconautGenerals','Biconaut']
    ],
}
dao_params=pd.DataFrame(dao_params)
# dao_params=pd.read_csv('dao_details.csv')
# print(dao_params['server_id'])
print(dao_params)
print(dao_params.iloc[0,1])


for i in range(len(dao_params)):
    res=(get_counts(dao_params.iloc[i,0],dao_params.iloc[i,1],dao_params.iloc[i,2],dao_params.iloc[i,3]))
    res.to_csv('dao_discord_dist/{}_dist.csv'.format(dao_params.iloc[i,0]))




############## 

############## number of sub dao and guilds 
#  Manually dao_list
# sub_dao_details={
#     "dao_name": ['MetricsDAO','Biconomy'],
#     "number_of_sub_daos" : ['0','0'],
#     "Number_of_guilds" : ['7','0']
# }
# pd.DataFrame(sub_dao_details).to_csv('dao_number.csv')






# ########## New vs existing users

# dao_name='MetricsDao'
# token_address='0x15848C9672e99be386807b9101f83A16EB017bb5'
# nve_users = f"""
# with user_cohorts as (
#     SELECT  FROM_ADDRESS as address
#             , min(block_timestamp::date) as cohortDate
#     FROM ethereum.core.fact_transactions
#     Where 1=1 
#   		AND TO_ADDRESS = lower('0x9C8fF314C9Bc7F6e59A9d9225Fb22946427eDC03')
#         AND STATUS = 'SUCCESS'
#     GROUP BY address
# ),
#      new_users as (
#     SELECT  cohortDate as date, count(distinct address) as new_users_count
#     FROM user_cohorts uc
#     GROUP BY date
# ),
#      all_users as (
#     SELECT block_timestamp::date as date
#         ,count(distinct FROM_ADDRESS) as total_players
  
#     FROM ethereum.core.fact_transactions
#     Where 1=1 
#   		AND TO_ADDRESS = lower('{{token_address}}')
#         AND STATUS = 'SUCCESS'
#  GROUP BY date
# )
#     SELECT  au.date
#          , nu.new_users_count
#          , au.total_players - nu.new_users_count AS Existing_Users
#          , (nu.new_users_count/au.total_players)*100 as New_User_Percentage
#     FROM all_users au
#     LEFT JOIN new_users nu
#         ON au.date = nu.date;

# """
# query_result_set = sdk.query(nve_users)
# res=(pd.DataFrame(query_result_set.records))
# res.to_csv('RRR/{}_nve_users.csv'.format(dao_name))


############# project overview
import pandas as pd 
import numpy as np
import plotly.express as px 
from datetime import date
today = date.today()
import os
from shroomdk import ShroomDK

sdk = ShroomDK("00dba474-bd21-4d4d-a9b9-c5eaa08aac33")
current_directory = os.getcwd()


dao_list=dao_details['Name'].to_list()
dao_details=pd.read_csv('dao_details.csv')










###### Cohort analysis
print('starting sql')
cohort_analysis_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    nve_users = f"""
    with user_cohorts as (
        SELECT  {dao_details_row['user'].values[0]} as address
                , min(date_trunc('month', block_timestamp)) as cohortMonth
        FROM {dao_details_row['Table'].values[0]}
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
            -- AND STATUS = 'SUCCESS'
            -- AND date_trunc('month', block_timestamp) > CURRENT_DATE() - interval '5 month'
            AND block_timestamp >  '2021-10-12'
        GROUP BY address
    ),
    following_months as (
        SELECT  {dao_details_row['user'].values[0]} as addresss
                , datediff('month', uc.cohortMonth, date_trunc('month', block_timestamp))  as month_number
        FROM {dao_details_row['Table'].values[0]}
        LEFT JOIN user_cohorts uc ON address = uc.address
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
            -- AND STATUS = 'SUCCESS'
            -- AND date_trunc('month', block_timestamp) > CURRENT_DATE() - interval '5 month'
            AND block_timestamp >  '2021-10-12'
        GROUP BY addresss, month_number
    ),
    cohort_size as (
        SELECT  uc.cohortMonth as cohortMonth
                , count(distinct address) as num_users
        FROM user_cohorts uc
        GROUP BY cohortMonth
        ORDER BY cohortMonth
    ),
    retention_table as (
        SELECT  c.cohortMonth as cohortMonth
                , o.month_number as month_number
                , count(distinct c.address) as num_users
            
        FROM following_months o
        LEFT JOIN user_cohorts c ON o.addresss = c.address
        GROUP BY cohortMonth, month_number
    )
    SELECT  '{dao_details_row['Name'].values[0]}' as dao_name, 
            r.cohortMonth
            , s.num_users as new_users
            , r.month_number
            , r.num_users / s.num_users as retention
    FROM retention_table r
    LEFT JOIN cohort_size s 
        ON r.cohortMonth = s.cohortMonth
    WHERE r.month_number != 0
    AND r.cohortMonth >   '2022-10-12'
    ORDER BY r.cohortMonth, r.month_number


    """
    query_result_set = sdk.query(nve_users)
    res=(pd.DataFrame(query_result_set.records))
    cohort_analysis_df=pd.concat([cohort_analysis_df,res],axis=0)
    print('finished')

cohort_analysis_df.to_csv('RRR/cohort_users.csv')

print('finsihed sql')














# ########## month on month users
mom_users_df=pd.DataFrame([],columns=['dao name','month','mom growth sales'])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    print(dao_name)
    mom_users = f"""
    SELECT '{dao_details_row['Name'].values[0]}' as dao_name,Month, ((Monthly_Transactions/Previous_Month)-1) *100 as MoM_Growth_Rates
    FROM(
    SELECT 
        date_trunc('month', block_timestamp) as Month
        ,count(distinct to_address) as Monthly_Transactions 
        ,lag(Monthly_Transactions) OVER (ORDER BY Month) as Previous_Month
        FROM {dao_details_row['Table'].values[0]}
        Where 1=1 
            AND contract_address = lower('{dao_details_row['Token'].values[0]}')
            -- AND STATUS = 'SUCCESS'
            AND date_trunc('month', block_timestamp) > CURRENT_DATE() - interval '5 month'
    GROUP BY Month
    ORDER BY Month ASC 
    ) 
    WHERE Previous_Month != 0

    """
    query_result_set = sdk.query(mom_users)
    res=(pd.DataFrame(query_result_set.records))
    mom_users_df=pd.concat([mom_users_df,res],axis=0)
mom_users_df.to_csv('RRR/mom_users.csv')







# ############# ########## month on month users
nve_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    nve = f"""
    with user_cohorts as (
        SELECT   {dao_details_row['user'].values[0]}  as address
                , min(block_timestamp::date) as cohortDate
        FROM {dao_details_row['Table'].values[0]} 
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
            -- AND STATUS = 'SUCCESS'
        GROUP BY address
    ),
        new_users as (
        SELECT  cohortDate as date, count(distinct address) as new_users_count
        FROM user_cohorts uc
        GROUP BY date
    ),
        all_users as (
        SELECT block_timestamp::date as date
            ,count(distinct  {dao_details_row['user'].values[0]} ) as total_players
    
        FROM {dao_details_row['Table'].values[0]} 
        Where 1=1 
            AND CONTRACT_ADDRESS = lower('{dao_details_row['Token'].values[0]}' )
            -- AND STATUS = 'SUCCESS'
    GROUP BY date
    )
        SELECT  '{dao_details_row['Name'].values[0]}' as dao_name, 
            au.date
            , nu.new_users_count
            , au.total_players - nu.new_users_count AS Existing_Users
            , (nu.new_users_count/au.total_players)*100 as New_User_Percentage
        FROM all_users au
        LEFT JOIN new_users nu
            ON au.date = nu.date;

    """
    query_result_set = sdk.query(nve)
    res=(pd.DataFrame(query_result_set.records))
    nve_df=pd.concat([nve_df,res],axis=0)
nve_df.to_csv('RRR/nve_users.csv')







############# ########## month on month users
sr_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    sr = f"""
    With daily_active_users as (
    SELECT date_trunc('month', day) as date, avg(active_addresses) as avg_dau
    FROM (
        SELECT date_trunc('day', block_timestamp) as day, count(distinct  {dao_details_row['user'].values[0]} ) AS active_addresses
        FROM {dao_details_row['Table'].values[0]}
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]}  = lower('{dao_details_row['Token'].values[0]}' )
            -- AND STATUS = 'SUCCESS'
            AND block_timestamp > CURRENT_DATE - interval '12 month'
    GROUP BY day
            )
    GROUP BY date
    ),
    monthly_active_users as (
            SELECT date_trunc('month', block_timestamp) as date, count(distinct  {dao_details_row['user'].values[0]})  AS mau
        FROM {dao_details_row['Table'].values[0]}
        Where 1=1 
            AND  {dao_details_row['user'].values[0]}  = lower('{dao_details_row['Token'].values[0]}')
            -- AND STATUS = 'SUCCESS'
            AND block_timestamp > CURRENT_DATE - interval '12 month'
            GROUP BY date
    )
    SELECT '{dao_details_row['Name'].values[0]}' as dao_name, daily.date as date, (daily.avg_dau/monthly.mau) as stickiness_ratio
    FROM daily_active_users daily
    LEFT JOIN monthly_active_users monthly
        ON daily.date = monthly.date
    ORDER BY date,1
        


    """
    query_result_set = sdk.query(sr)
    res=(pd.DataFrame(query_result_set.records))
    sr_df=pd.concat([sr_df,res],axis=0)
sr_df.to_csv('RRR/stickiness_ratio.csv')

###### new addresses
na_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    sr = f"""
    WITH active_addresses AS (
        SELECT block_timestamp,  {dao_details_row['user'].values[0]} as address
        FROM {dao_details_row['Table'].values[0]} 
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]} ')
            --AND STATUS = 'SUCCESS'
        -- WHERE [chain_name:chainname]                     
    UNION ALL 
        SELECT block_timestamp,  {dao_details_row['user'].values[0]}  as address
        FROM {dao_details_row['Table'].values[0]} 
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]} ')
            --AND STATUS = 'SUCCESS'
        -- WHERE [chain_name:chainname]
    )
    SELECT '{dao_details_row['Name'].values[0]}'  as dao_name, date, count (distinct address) 
    FROM (
        SELECT min(block_timestamp) AS date, address
        FROM active_addresses 
        GROUP BY address
    )     
    WHERE date > current_date - INTERVAL ' 6 month '
    GROUP BY date
    ORDER BY date desc




    """
    query_result_set = sdk.query(sr)
    res=(pd.DataFrame(query_result_set.records))
    na_df=pd.concat([na_df,res],axis=0)
na_df.to_csv('RRR/new_users.csv')






######### Governance


dao_details=pd.read_csv('dao_details.csv')
########## Number of proposals
total_number_of_proposals_past = "https://node-api.flipsidecrypto.com/api/v2/queries/8cb84a98-d2bd-48f4-a886-5c67cadf518c/data/latest"
total_number_of_proposals_past = pd.read_json(total_number_of_proposals_past)
print(dao_details)
print(total_number_of_proposals_past)
total_number_of_proposals_past_merged=pd.merge(total_number_of_proposals_past,dao_details,on='SPACE_ID',how='left')
total_number_of_proposals_past_merged=total_number_of_proposals_past_merged[['Name','SPACE_ID','NUMBER_OF_PROPOSALS']]
total_number_of_proposals_past_merged.to_csv('governance/total_number_of_proposals_past.csv')


######## ongoing proposals

number_of_ongoing_proposals = "https://node-api.flipsidecrypto.com/api/v2/queries/f5dd825e-4701-46b8-a453-5820030b943a/data/latest"
number_of_ongoing_proposals = pd.read_json(number_of_ongoing_proposals)
try:
    number_of_ongoing_proposals_merged=pd.merge(number_of_ongoing_proposals,dao_details,on='SPACE_ID',how='left')
    number_of_ongoing_proposals_merged=number_of_ongoing_proposals_merged[['Name','SPACE_ID','NUMBER_OF_PROPOSALS']]
    number_of_ongoing_proposals_merged.to_csv('governance/number_of_ongoing_proposals.csv')
except:
    pd.DataFrame([]).to_csv('governance/number_of_ongoing_proposals.csv')


###### ongoing proposals
ongoing_proposals = "https://node-api.flipsidecrypto.com/api/v2/queries/32f8725c-4734-4d67-82ae-32fc3fcc2b51/data/latest"
ongoing_proposals = pd.read_json(ongoing_proposals)
try:
    ongoing_proposals_merged=pd.merge(ongoing_proposals,dao_details,on='SPACE_ID',how='left')
    ongoing_proposals_merged=ongoing_proposals_merged[['Name','SPACE_ID','PROPOSAL_ID','PROPOSAL_TITLE','PROPOSAL_TEXT','VOTING_START','VOTING_ENDS']]
    ongoing_proposals_merged.to_csv('governance/ongoing_proposals.csv')
except:
    pd.DataFrame([]).to_csv('governance/ongoing_proposals.csv')


######### Voting trend

proposal_voter_trend = "https://node-api.flipsidecrypto.com/api/v2/queries/6953f8c5-da3f-4790-9bf9-5a79d25f084d/data/latest"
proposal_voter_trend = pd.read_json(proposal_voter_trend)
proposal_voter_trend_with_dao_name=pd.merge(proposal_voter_trend,dao_details,on='SPACE_ID',how='left')
proposal_voter_trend_with_dao_name=proposal_voter_trend_with_dao_name[['Name','date','SPACE_ID','NUMBER_OF_PROPOSALS','NUMBER_OF_VOTERS','VOTES','RATIO']]
proposal_voter_trend_with_dao_name.to_csv('governance/voting_prop_trend.csv')


######### Proposal trend

proposal_trend = "https://node-api.flipsidecrypto.com/api/v2/queries/c9b80d34-b79d-465e-a41f-71e46a458e0e/data/latest"
proposal_trend = pd.read_json(proposal_trend)
proposal_trend_with_dao_name=pd.merge(proposal_trend,dao_details,on='SPACE_ID',how='left')
proposal_trend_with_dao_name=proposal_trend_with_dao_name[['Name','date','SPACE_ID','NUMBER_OF_PROPOSALS','NUMBER_OF_VOTERS','VOTES','RATIO']]
proposal_trend_with_dao_name.to_csv('governance/proposal_trend.csv')

########### Average duration beween proposals
average_duration_between_proposals = "https://node-api.flipsidecrypto.com/api/v2/queries/f579fe5a-239b-42a4-b97a-de700b1a26fd/data/latest"
average_duration_between_proposals = pd.read_json(average_duration_between_proposals)
average_duration_between_proposals_with_dao_name=pd.merge(average_duration_between_proposals,dao_details,on='SPACE_ID',how='left')
average_duration_between_proposals_with_dao_name=average_duration_between_proposals_with_dao_name[['Name','SPACE_ID','AVERAGE_DURATION_BETWEEN_PROPOSALS']]
average_duration_between_proposals_with_dao_name.to_csv('governance/average_duration_between_proposals.csv')


########### voting power dist 
##### voting power dist
voting_power_dist=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    vp = f"""
        with latest_proposal as 
            (
            select distinct proposal_id
            from ethereum.core.ez_snapshot
            where space_id = '{dao_details_row['SPACE_ID'].values[0]}'
            qualify(row_number() over (partition by space_id order by PROPOSAL_END_TIME desc)=1)  
            ) 
        select '{dao_details_row['Name'].values[0]}'  as dao_name,space_id, proposal_id,voter, VOTING_POWER from ethereum.core.ez_snapshot
        where proposal_id in ( select * from latest_proposal)

    """
    query_result_set = sdk.query(vp)
    res=(pd.DataFrame(query_result_set.records))
    voting_power_dist=pd.concat([voting_power_dist,res],axis=0)
voting_power_dist.to_csv('governance/voting_power.csv')

