import pandas as pd 
import gspread as gs
import numpy as np
from gspread_dataframe import set_with_dataframe
from datetime import date
today = date.today()
from shroomdk import ShroomDK
import tweepy
import requests
import json
import discum
import re


sdk = ShroomDK("00dba474-bd21-4d4d-a9b9-c5eaa08aac33")
gc = gs.service_account(filename='/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1wmVhR3GYJIcAvKR1j_XawVwbTI0Vmi_8K5Bv4vGGHF8/edit?usp=sharing')
ws = sh.worksheet('dao_details')
df = pd.DataFrame(ws.get_all_records())


ws = sh.worksheet('dao_details')
dao_details = pd.DataFrame(ws.get_all_records())
dao_list=dao_details['twitter handle'].apply(lambda x: x.replace('https://twitter.com/',''))


ws = sh.worksheet('twitter_log')
twitter_log=pd.DataFrame(ws.get_all_records())
auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAEKQiwEAAAAACaGFqOl1LhYAkmTGKqN9%2FrrFNqc%3D47Yh8KbJE0crZ8bUtE7AS7h88iT5gJq9H3cy63zWZqGmf8DwJJ")
api = tweepy.API(auth)
for dao in dao_list:
    user_dict=(api.get_user(screen_name=dao))._json
    twitter_today=pd.DataFrame([[today,re.sub(r'[^a-zA-Z0-9\s]', '', user_dict['name']),user_dict['followers_count'],user_dict['friends_count']]],columns=['Date','Dao Name','Followers','Following'])
    twitter_log=pd.concat([twitter_log,twitter_today])
df = pd.DataFrame(ws.get_all_records())
set_with_dataframe(ws, twitter_log)
print('finsihed twitter')
# assert False


###### Discord

# discord_log=pd.DataFrame([],columns=['Date','Dao Name','Total users','Active users'])
dao_list_discord=dao_details['discord_code']
ws = sh.worksheet('discord log')
discord_log=pd.DataFrame(ws.get_all_records())

for dao in dao_list_discord:
    response_API = requests.get('https://discord.com/api/v9/invites/{}?with_counts=true&with_expiration=true'.format(dao))
#print(response_API.status_code)
    data = response_API.text
    parse_json = pd.read_json(data)

# active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
# print("Active cases in South Andaman:", active_case)
    discord_today=pd.DataFrame([[today,parse_json['guild']['name'],parse_json['approximate_member_count']['id'],parse_json['approximate_presence_count']['id']]],columns=['Date','Dao Name','Total users','Active users'])
    discord_log=pd.concat([discord_log,discord_today])
set_with_dataframe(ws, discord_log)
print('finsihed discord daily')



### Discord contributors


bot = discum.Client(token="MzkwNDkzMjU1MTY4Njg4MTI4.G9EaCb.2NaUxCoDcasjXh2k0pywfGmhdMYaUye74rl8ow")

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
    all_role=[]
    non_role=[]
    for role in roles_data['role']:
        all_role.append(role)
        if role in imp_roles:
            value_count = member_data_with_role.eq(role).sum().sum()

            role_count_row.append(role)
            role_count_row.append(value_count)
            role_count.append(role_count_row)
            role_count_row=[]
        else:
            non_role.append(role)
    role_count_df=pd.DataFrame(role_count)
    # ws = sh.worksheet('temp')
    # res=pd.DataFrame(all_role)
    # ws.append_rows(res.values.tolist())
    # ws = sh.worksheet('temp2')
    # res=pd.DataFrame(non_role)
    # ws.append_rows(res.values.tolist())
    # role_count_df.to_csv('/media/sandesh/7b4515cf-7277-44bc-a068-425d5c6990f9/crypto/dummy/res/mdao_role_count.csv')
    # role_count_df[1]=100*role_count_df[1]/role_count_df[1].sum()
    role_count_df['dao_name']=server_name
    role_count_df['date']=date.today()
    role_count_df['date']=role_count_df['date'].astype(str)
    return role_count_df


# # dao_params={
# #     "server_name": ['MetricsDAO','Biconomy'],
# #     "server_id" : ['902943676685230100','692403655474937856'],
# #     "channel_id" : ['903338987022876702','845957610792157187'],
# #     "imp_roles" :
# #     [
# #         ['Verified','xMETRICMaster','Contributor','Curator','Moderator','Admin','Governor','Connected'], # metrics_dao
# #         ['Developer','BiconautGenerals','Biconaut']
# #     ],
# # }
# #dao_params=pd.DataFrame(dao_params)
# # dao_params=pd.read_csv('dao_details.csv')
# # print(dao_params['server_id'])

# #print(dao_params)
# #print(dao_params.iloc[0,1])

ws = sh.worksheet('dao_details')
dao_details = pd.DataFrame(ws.get_all_records())
dao_params=dao_details[['server_name','server_id','channel_id','imp_roles']]
dao_params = dao_params.astype(str)
dao_params['imp_roles'] = dao_params['imp_roles'].str.replace(r'[^\w\s()]','')



# print(dao_params.dtypes)
# assert False



for i in range(len(dao_params)):
    print(dao_params.iloc[i,0],dao_params.iloc[i,1],dao_params.iloc[i,2],dao_params.iloc[i,3])
    res=(get_counts(dao_params.iloc[i,0],dao_params.iloc[i,1],dao_params.iloc[i,2],dao_params.iloc[i,3]))
    # res.to_csv('dao_discord_dist/{}_dist.csv'.format(dao_params.iloc[i,0]))
    ws = sh.worksheet('Discord dist')
    ws.append_rows(res.values.tolist())

print('finsihed discord dist')
# assert False









# ############# project overview


ws = sh.worksheet('dao_details')
dao_details = pd.DataFrame(ws.get_all_records())
dao_list=dao_details['Name'].to_list()











###### Cohort analysis
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
    AND r.cohortMonth >   '2022-11-12'
    ORDER BY r.cohortMonth, r.month_number
    """
    query_result_set = sdk.query(nve_users, timeout_minutes=30)
    res=(pd.DataFrame(query_result_set.records))
    cohort_analysis_df=pd.concat([cohort_analysis_df,res],axis=0)
    print('finished')


# cohort_analysis_df.to_csv('RRR/cohort_users.csv')
ws = sh.worksheet('cohort_users')
set_with_dataframe(ws, cohort_analysis_df)

print('finsihed cohort analysis')














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
# mom_users_df.to_csv('RRR/mom_users.csv')
ws = sh.worksheet('mom_users')
set_with_dataframe(ws, mom_users_df)
print('finsihed mom')








# # ############# new vs existing users

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
nve_df.dropna(inplace=True)
# nve_df.to_csv('RRR/nve_users.csv')
ws = sh.worksheet('nve_users')
set_with_dataframe(ws, nve_df)
print('finished new vs existing users')








############# ########## stickiness ratio

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
# sr_df.to_csv('RRR/stickiness_ratio.csv')
ws = sh.worksheet('stickiness_ratio')
set_with_dataframe(ws, sr_df)
print('stickiness ratio')

###### new addresses
na_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    na = f"""
    WITH active_addresses AS (
        SELECT block_timestamp,  {dao_details_row['user'].values[0]} as address
        FROM {dao_details_row['Table'].values[0]} 
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
            --AND STATUS = 'SUCCESS'
        -- WHERE [chain_name:chainname]                     
    UNION ALL 
        SELECT block_timestamp,  {dao_details_row['user'].values[0]}  as address
        FROM {dao_details_row['Table'].values[0]} 
        Where 1=1 
            AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
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
    query_result_set = sdk.query(na)
    res=(pd.DataFrame(query_result_set.records))
    na_df=pd.concat([na_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('new_users')
set_with_dataframe(ws, na_df)
print('new users')






######### Governance
ws = sh.worksheet('dao_details')
dao_details = pd.DataFrame(ws.get_all_records())
# dao_details=pd.read_csv('dao_details.csv')
########## Number of proposals
# total_number_of_proposals_past = "https://node-api.flipsidecrypto.com/api/v2/queries/8cb84a98-d2bd-48f4-a886-5c67cadf518c/data/latest"
# total_number_of_proposals_past = pd.read_json(total_number_of_proposals_past)
# print(dao_details)
# print(total_number_of_proposals_past)
# total_number_of_proposals_past_merged=pd.merge(total_number_of_proposals_past,dao_details,on='SPACE_ID',how='left')
# total_number_of_proposals_past_merged=total_number_of_proposals_past_merged[['Name','SPACE_ID','NUMBER_OF_PROPOSALS']]
# ws = sh.worksheet('total_number_of_proposals_past')
# set_with_dataframe(ws, total_number_of_proposals_past_merged)


###### Number of proposals
Number_of_proposals_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    Number_of_proposals = f"""

    select '{dao_details_row['Name'].values[0]}' as dao_name,space_id, count(distinct proposal_id) as number_of_proposals from ethereum.core.ez_snapshot
    where 1=1 
    and space_id='{dao_details_row['SPACE_ID'].values[0]}'
    and PROPOSAL_END_TIME <= CURRENT_DATE
    group by space_id

    """
    query_result_set = sdk.query(Number_of_proposals)
    res=(pd.DataFrame(query_result_set.records))
    Number_of_proposals_df=pd.concat([Number_of_proposals_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('total_number_of_proposals_past')
set_with_dataframe(ws, Number_of_proposals_df)






# total_number_of_proposals_past_merged.to_csv('governance/total_number_of_proposals_past.csv')


######## ongoing proposals
Number_of_new_proposals_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    Number_of_new_proposals = f"""

    select '{dao_details_row['Name'].values[0]}' as dao_name,space_id, count(distinct proposal_id) as number_of_proposals from ethereum.core.ez_snapshot
    where 1=1 
    and space_id='{dao_details_row['SPACE_ID'].values[0]}'
    and PROPOSAL_END_TIME >= CURRENT_DATE
    group by space_id

    """
    query_result_set = sdk.query(Number_of_new_proposals)
    res=(pd.DataFrame(query_result_set.records))
    Number_of_new_proposals_df=pd.concat([Number_of_new_proposals_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('number_of_ongoing_proposals')
set_with_dataframe(ws, Number_of_new_proposals_df)


# number_of_ongoing_proposals = "https://node-api.flipsidecrypto.com/api/v2/queries/f5dd825e-4701-46b8-a453-5820030b943a/data/latest"
# number_of_ongoing_proposals = pd.read_json(number_of_ongoing_proposals)
# try:
#     number_of_ongoing_proposals_merged=pd.merge(number_of_ongoing_proposals,dao_details,on='SPACE_ID',how='left')
#     number_of_ongoing_proposals_merged=number_of_ongoing_proposals_merged[['Name','SPACE_ID','NUMBER_OF_PROPOSALS']]
#     # number_of_ongoing_proposals_merged.to_csv('governance/number_of_ongoing_proposals.csv')
#     ws = sh.worksheet('number_of_ongoing_proposals')
#     set_with_dataframe(ws, number_of_ongoing_proposals_merged)
# except:
#     ws = sh.worksheet('number_of_ongoing_proposals')
#     set_with_dataframe(ws, pd.DataFrame([]))



###### ongoing proposals
ongoing_proposals_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    ongoing_proposals = f"""

    select '{dao_details_row['Name'].values[0]}' as dao_name,space_id,PROPOSAL_ID, proposal_text, PROPOSAL_TITLE, min(PROPOSAL_START_TIME) as Voting_start, max(PROPOSAL_START_TIME) as voting_ends from ethereum.core.ez_snapshot
    where 1=1 
    and space_id='{dao_details_row['SPACE_ID'].values[0]}'
    and PROPOSAL_END_TIME >= CURRENT_DATE
    group by 1,2,3,4,5

    """
    query_result_set = sdk.query(ongoing_proposals)
    res=(pd.DataFrame(query_result_set.records))
    ongoing_proposals_df=pd.concat([ongoing_proposals_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('ongoing_proposals')
set_with_dataframe(ws, ongoing_proposals_df)


# ongoing_proposals = "https://node-api.flipsidecrypto.com/api/v2/queries/32f8725c-4734-4d67-82ae-32fc3fcc2b51/data/latest"
# ongoing_proposals = pd.read_json(ongoing_proposals)
# try:
#     ongoing_proposals_merged=pd.merge(ongoing_proposals,dao_details,on='SPACE_ID',how='left')
#     ongoing_proposals_merged=ongoing_proposals_merged[['Name','SPACE_ID','PROPOSAL_ID','PROPOSAL_TITLE','PROPOSAL_TEXT','VOTING_START','VOTING_ENDS']]
#     ongoing_proposals_merged.to_csv('governance/ongoing_proposals.csv')
#     ws = sh.worksheet('ongoing_proposals')
#     set_with_dataframe(ws, ongoing_proposals_merged)
# except:
#     ws = sh.worksheet('ongoing_proposals')
#     set_with_dataframe(ws, pd.DataFrame([]))


######### Voting trend
proposal_voter_trend_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    proposal_voter_trend = f"""

    select 
    VOTE_TIMESTAMP::date as "date", 
    '{dao_details_row['Name'].values[0]}' as dao_name,
    space_id,
    count(distinct proposal_id) as number_of_proposals, 
    count(distinct voter) as number_of_voters,
    sum(VOTING_POWER) as votes,
    votes/number_of_voters as ratio
    from ethereum.core.ez_snapshot
    where 1=1 
    and space_id='{dao_details_row['SPACE_ID'].values[0]}'
    -- and "date" > CURRENT_DATE - interval ' 6 months'
    group by "date",dao_name,space_id


    """
    query_result_set = sdk.query(proposal_voter_trend)
    res=(pd.DataFrame(query_result_set.records))
    proposal_voter_trend_df=pd.concat([proposal_voter_trend_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('voting_prop_trend')
set_with_dataframe(ws, proposal_voter_trend_df)



# proposal_voter_trend = "https://node-api.flipsidecrypto.com/api/v2/queries/6953f8c5-da3f-4790-9bf9-5a79d25f084d/data/latest"
# proposal_voter_trend = pd.read_json(proposal_voter_trend)
# proposal_voter_trend_with_dao_name=pd.merge(proposal_voter_trend,dao_details,on='SPACE_ID',how='left')
# proposal_voter_trend_with_dao_name=proposal_voter_trend_with_dao_name[['Name','date','SPACE_ID','NUMBER_OF_PROPOSALS','NUMBER_OF_VOTERS','VOTES','RATIO']]
# ws = sh.worksheet('voting_prop_trend')
# set_with_dataframe(ws, proposal_voter_trend_with_dao_name)


######### Proposal trend
proposal_trend_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    proposal_trend = f"""

    select 
    PROPOSAL_START_TIME::date as "date", 
    '{dao_details_row['Name'].values[0]}' as dao_name,
    space_id,
    count(distinct proposal_id) as number_of_proposals, 
    count(distinct voter) as number_of_voters,
    sum(VOTING_POWER) as votes,
    votes/number_of_voters as ratio
    from ethereum.core.ez_snapshot
    where 1=1 
    and space_id='{dao_details_row['SPACE_ID'].values[0]}'
    -- and "date" > CURRENT_DATE - interval ' 6 months'
    group by "date",dao_name,space_id


    """
    query_result_set = sdk.query(proposal_trend)
    res=(pd.DataFrame(query_result_set.records))
    proposal_trend_df=pd.concat([proposal_trend_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('proposal_trend')
set_with_dataframe(ws, proposal_trend_df)





# proposal_trend = "https://node-api.flipsidecrypto.com/api/v2/queries/c9b80d34-b79d-465e-a41f-71e46a458e0e/data/latest"
# proposal_trend = pd.read_json(proposal_trend)
# proposal_trend_with_dao_name=pd.merge(proposal_trend,dao_details,on='SPACE_ID',how='left')
# proposal_trend_with_dao_name=proposal_trend_with_dao_name[['Name','date','SPACE_ID','NUMBER_OF_PROPOSALS','NUMBER_OF_VOTERS','VOTES','RATIO']]
# ws = sh.worksheet('proposal_trend')
# set_with_dataframe(ws, proposal_trend_with_dao_name)

########### Average duration beween proposals

average_duration_between_proposals_df=pd.DataFrame([])
for dao_name in dao_list: 
    dao_details_row=dao_details[dao_details['Name']==dao_name]
    average_duration_between_proposals = f"""

    with temp as 
    (
    select '{dao_details_row['Name'].values[0]}' as dao_name,
    space_id,proposal_id, proposal_title, min(proposal_start_time) as voting_opens,
    datediff('day',(lag(voting_opens) over(partition by space_id order by voting_opens asc)),voting_opens) as time_diff
    from ethereum.core.ez_snapshot
    where 1=1
    and space_id='{dao_details_row['SPACE_ID'].values[0]}'
        group by 1,2,3,4
    -- having 
    )
    select '{dao_details_row['Name'].values[0]}' as dao_name,space_id, avg(abs(time_diff)) as average_duration_between_proposals from temp 
    group by dao_name,space_id


    """
    query_result_set = sdk.query(average_duration_between_proposals)
    res=(pd.DataFrame(query_result_set.records))
    average_duration_between_proposals_df=pd.concat([average_duration_between_proposals_df,res],axis=0)
# na_df.to_csv('RRR/new_users.csv')
ws = sh.worksheet('average_duration_between_proposals')
set_with_dataframe(ws, average_duration_between_proposals_df)






# average_duration_between_proposals = "https://node-api.flipsidecrypto.com/api/v2/queries/f579fe5a-239b-42a4-b97a-de700b1a26fd/data/latest"
# average_duration_between_proposals = pd.read_json(average_duration_between_proposals)
# average_duration_between_proposals_with_dao_name=pd.merge(average_duration_between_proposals,dao_details,on='SPACE_ID',how='left')
# average_duration_between_proposals_with_dao_name=average_duration_between_proposals_with_dao_name[['Name','SPACE_ID','AVERAGE_DURATION_BETWEEN_PROPOSALS']]
# ws = sh.worksheet('average_duration_between_proposals')
# set_with_dataframe(ws, average_duration_between_proposals_with_dao_name)


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
ws = sh.worksheet('voting_power')
set_with_dataframe(ws, voting_power_dist)

