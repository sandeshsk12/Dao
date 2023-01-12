
import pandas as pd 
import numpy as np
import plotly.express as px 
from datetime import date
today = date.today()
import os
from shroomdk import ShroomDK

sdk = ShroomDK("00dba474-bd21-4d4d-a9b9-c5eaa08aac33")
current_directory = os.getcwd()


dao_list=['Biconomy','MetricsDAO']
dao_details=pd.read_csv('dao_details.csv')











# cohort_analysis_df=pd.DataFrame([])
# for dao_name in dao_list: 
#     dao_details_row=dao_details[dao_details['Name']==dao_name]
#     nve_users = f"""
#     with user_cohorts as (
#         SELECT  {dao_details_row['user'].values[0]} as address
#                 , min(date_trunc('month', block_timestamp)) as cohortMonth
#         FROM {dao_details_row['Table'].values[0]}
#         Where 1=1 
#             AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
#             -- AND STATUS = 'SUCCESS'
#             -- AND date_trunc('month', block_timestamp) > CURRENT_DATE() - interval '5 month'
#             AND block_timestamp >  '2021-10-12'
#         GROUP BY address
#     ),
#     following_months as (
#         SELECT  {dao_details_row['user'].values[0]} as addresss
#                 , datediff('month', uc.cohortMonth, date_trunc('month', block_timestamp))  as month_number
#         FROM {dao_details_row['Table'].values[0]}
#         LEFT JOIN user_cohorts uc ON address = uc.address
#         Where 1=1 
#             AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
#             -- AND STATUS = 'SUCCESS'
#             -- AND date_trunc('month', block_timestamp) > CURRENT_DATE() - interval '5 month'
#             AND block_timestamp >  '2021-10-12'
#         GROUP BY addresss, month_number
#     ),
#     cohort_size as (
#         SELECT  uc.cohortMonth as cohortMonth
#                 , count(distinct address) as num_users
#         FROM user_cohorts uc
#         GROUP BY cohortMonth
#         ORDER BY cohortMonth
#     ),
#     retention_table as (
#         SELECT  c.cohortMonth as cohortMonth
#                 , o.month_number as month_number
#                 , count(distinct c.address) as num_users
            
#         FROM following_months o
#         LEFT JOIN user_cohorts c ON o.addresss = c.address
#         GROUP BY cohortMonth, month_number
#     )
#     SELECT  '{dao_details_row['Name'].values[0]}' as dao_name, 
#             r.cohortMonth
#             , s.num_users as new_users
#             , r.month_number
#             , r.num_users / s.num_users as retention
#     FROM retention_table r
#     LEFT JOIN cohort_size s 
#         ON r.cohortMonth = s.cohortMonth
#     WHERE r.month_number != 0
#     AND r.cohortMonth >   '2022-10-12'
#     ORDER BY r.cohortMonth, r.month_number


#     """
#     query_result_set = sdk.query(nve_users)
#     res=(pd.DataFrame(query_result_set.records))
#     cohort_analysis_df=pd.concat([cohort_analysis_df,res],axis=0)
#     print('finished')

# cohort_analysis_df.to_csv('RRR/cohort_users.csv')
















# ########## month on month users
# mom_users_df=pd.DataFrame([],columns=['dao name','month','mom growth sales'])
# for dao_name in dao_list: 
#     dao_details_row=dao_details[dao_details['Name']==dao_name]
#     print(dao_name)
#     mom_users = f"""
#     SELECT '{dao_details_row['Name'].values[0]}' as dao_name,Month, ((Monthly_Transactions/Previous_Month)-1) *100 as MoM_Growth_Rates
#     FROM(
#     SELECT 
#         date_trunc('month', block_timestamp) as Month
#         ,count(distinct to_address) as Monthly_Transactions 
#         ,lag(Monthly_Transactions) OVER (ORDER BY Month) as Previous_Month
#         FROM {dao_details_row['Table'].values[0]}
#         Where 1=1 
#             AND contract_address = lower('{dao_details_row['Token'].values[0]}')
#             -- AND STATUS = 'SUCCESS'
#             AND date_trunc('month', block_timestamp) > CURRENT_DATE() - interval '5 month'
#     GROUP BY Month
#     ORDER BY Month ASC 
#     ) 
#     WHERE Previous_Month != 0

#     """
#     query_result_set = sdk.query(mom_users)
#     res=(pd.DataFrame(query_result_set.records))
#     mom_users_df=pd.concat([mom_users_df,res],axis=1)
# mom_users_df.to_csv('RRR/mom_users.csv')







# ############# ########## month on month users
# nve_df=pd.DataFrame([])
# for dao_name in dao_list: 
#     dao_details_row=dao_details[dao_details['Name']==dao_name]
#     nve = f"""
#     with user_cohorts as (
#         SELECT   {dao_details_row['user'].values[0]}  as address
#                 , min(block_timestamp::date) as cohortDate
#         FROM {dao_details_row['Table'].values[0]} 
#         Where 1=1 
#             AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]}')
#             -- AND STATUS = 'SUCCESS'
#         GROUP BY address
#     ),
#         new_users as (
#         SELECT  cohortDate as date, count(distinct address) as new_users_count
#         FROM user_cohorts uc
#         GROUP BY date
#     ),
#         all_users as (
#         SELECT block_timestamp::date as date
#             ,count(distinct  {dao_details_row['user'].values[0]} ) as total_players
    
#         FROM {dao_details_row['Table'].values[0]} 
#         Where 1=1 
#             AND CONTRACT_ADDRESS = lower('{dao_details_row['Token'].values[0]}' )
#             -- AND STATUS = 'SUCCESS'
#     GROUP BY date
#     )
#         SELECT  '{dao_details_row['Name'].values[0]}' as dao_name, 
#             au.date
#             , nu.new_users_count
#             , au.total_players - nu.new_users_count AS Existing_Users
#             , (nu.new_users_count/au.total_players)*100 as New_User_Percentage
#         FROM all_users au
#         LEFT JOIN new_users nu
#             ON au.date = nu.date;

#     """
#     query_result_set = sdk.query(nve)
#     res=(pd.DataFrame(query_result_set.records))
#     nve_df=pd.concat([nve_df,res],axis=1)
# nve_df.to_csv('RRR/nve_users.csv')







############# ########## month on month users
# sr_df=pd.DataFrame([])
# for dao_name in dao_list: 
#     dao_details_row=dao_details[dao_details['Name']==dao_name]
#     sr = f"""
#     With daily_active_users as (
#     SELECT date_trunc('month', day) as date, avg(active_addresses) as avg_dau
#     FROM (
#         SELECT date_trunc('day', block_timestamp) as day, count(distinct  {dao_details_row['user'].values[0]} ) AS active_addresses
#         FROM {dao_details_row['Table'].values[0]}
#         Where 1=1 
#             AND {dao_details_row['identifier'].values[0]}  = lower('{dao_details_row['Token'].values[0]}' )
#             -- AND STATUS = 'SUCCESS'
#             AND block_timestamp > CURRENT_DATE - interval '12 month'
#     GROUP BY day
#             )
#     GROUP BY date
#     ),
#     monthly_active_users as (
#             SELECT date_trunc('month', block_timestamp) as date, count(distinct  {dao_details_row['user'].values[0]})  AS mau
#         FROM {dao_details_row['Table'].values[0]}
#         Where 1=1 
#             AND  {dao_details_row['user'].values[0]}  = lower('{dao_details_row['Token'].values[0]}')
#             -- AND STATUS = 'SUCCESS'
#             AND block_timestamp > CURRENT_DATE - interval '12 month'
#             GROUP BY date
#     )
#     SELECT '{dao_details_row['Name'].values[0]}' as dao_name, daily.date as date, (daily.avg_dau/monthly.mau) as stickiness_ratio
#     FROM daily_active_users daily
#     LEFT JOIN monthly_active_users monthly
#         ON daily.date = monthly.date
#     ORDER BY date
        


#     """
#     query_result_set = sdk.query(sr)
#     res=(pd.DataFrame(query_result_set.records))
#     print(res)
#     sr_df=pd.concat([sr_df,res],axis=0)
# sr_df.to_csv('RRR/stickiness_ratio.csv')

###### new addresses
# na_df=pd.DataFrame([])
# for dao_name in dao_list: 
#     dao_details_row=dao_details[dao_details['Name']==dao_name]
#     sr = f"""
#     WITH active_addresses AS (
#         SELECT block_timestamp,  {dao_details_row['user'].values[0]} as address
#         FROM {dao_details_row['Table'].values[0]} 
#         Where 1=1 
#             AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]} ')
#             --AND STATUS = 'SUCCESS'
#         -- WHERE [chain_name:chainname]                     
#     UNION ALL 
#         SELECT block_timestamp,  {dao_details_row['user'].values[0]}  as address
#         FROM {dao_details_row['Table'].values[0]} 
#         Where 1=1 
#             AND {dao_details_row['identifier'].values[0]} = lower('{dao_details_row['Token'].values[0]} ')
#             --AND STATUS = 'SUCCESS'
#         -- WHERE [chain_name:chainname]
#     )
#     SELECT '{dao_details_row['Name'].values[0]}'  as dao_name, date, count (distinct address) 
#     FROM (
#         SELECT min(block_timestamp) AS date, address
#         FROM active_addresses 
#         GROUP BY address
#     )     
#     WHERE date > current_date - INTERVAL ' 6 month '
#     GROUP BY date
#     ORDER BY date desc




#     """
#     query_result_set = sdk.query(sr)
#     res=(pd.DataFrame(query_result_set.records))
#     na_df=pd.concat([na_df,res],axis=1)
# na_df.to_csv('RRR/new_users.csv')


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
        select '{dao_details_row['Name'].values[0]}'  as dao_name,space_id, proposal_id,VOTING_POWER from ethereum.core.ez_snapshot
        where proposal_id in ( select * from latest_proposal)

    """
    query_result_set = sdk.query(vp)
    res=(pd.DataFrame(query_result_set.records))
    voting_power_dist=pd.concat([voting_power_dist,res],axis=0)
voting_power_dist.to_csv('governance/voting_power.csv')