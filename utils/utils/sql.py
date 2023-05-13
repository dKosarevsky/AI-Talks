QUERIES_QUERY = """
select *
from snowflake.account_usage.query_history
where START_TIME >= convert_timezone('UTC', 'UTC', ('{date_from}T00:00:00Z')::timestamp_ltz)
and START_TIME < convert_timezone('UTC', 'UTC', ('{date_to}T00:00:00Z')::timestamp_ltz);
"""

QUERIES_COUNT_QUERY = """
select QUERY_TEXT,
       count(*) as number_of_queries,
       sum(TOTAL_ELAPSED_TIME)/1000 as execution_seconds,
       sum(TOTAL_ELAPSED_TIME)/(1000*60) as execution_minutes,
       sum(TOTAL_ELAPSED_TIME)/(1000*60*60) as execution_hours
from SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY Q
where 1=1
  and Q.START_TIME >= convert_timezone('UTC', 'UTC', ('{date_from}T00:00:00Z')::timestamp_ltz)
  and Q.START_TIME <= convert_timezone('UTC', 'UTC', ('{date_to}T00:00:00Z')::timestamp_ltz)
  and TOTAL_ELAPSED_TIME > 0 --only get queries that actually used compute
  and WAREHOUSE_NAME = '{warehouse_name}'

group by 1
having count(*) >= {num_min} --configurable/minimal threshold

order by 2 desc
limit {limit}; --configurable upper bound threshold
"""

CONSUMPTION_PER_SERVICE_TYPE_QUERY = """
select date_trunc('hour', convert_timezone('UTC', start_time)) as start_time,
       name,
       service_type,
       round(sum(credits_used), 1) as credits_used,
       round(sum(credits_used_compute), 1) as credits_compute,
       round(sum(credits_used_cloud_services), 1) as credits_cloud
from snowflake.account_usage.metering_history
where start_time >= convert_timezone('UTC', 'UTC', ('{date_from}T00:00:00Z')::timestamp_ltz)
and start_time < convert_timezone('UTC', 'UTC', ('{date_to}T00:00:00Z')::timestamp_ltz)
group by 1, 2, 3;
"""

WAREHOUSE_USAGE_HOURLY = """
// Credits used by [hour, warehouse] (past 7 days)
select START_TIME ,
       WAREHOUSE_NAME ,
       CREDITS_USED_COMPUTE
from SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
where START_TIME >= convert_timezone('UTC', 'UTC', ('{date_from}T00:00:00Z')::timestamp_ltz)
  and start_time < convert_timezone('UTC', 'UTC', ('{date_to}T00:00:00Z')::timestamp_ltz)
  and WAREHOUSE_ID > 0 // Skip pseudo-VWs such as "CLOUD_SERVICES_ONLY"
order by 1 desc,
         2
"""

STORAGE_QUERY = """
select convert_timezone('UTC', usage_date) as usage_date,
       database_name as object_name,
       'database' as object_type,
       max(AVERAGE_DATABASE_BYTES) as database_bytes,
       max(AVERAGE_FAILSAFE_BYTES) as failsafe_bytes,
       0 as stage_bytes
from snowflake.account_usage.database_storage_usage_history
where usage_date >= date_trunc('day', ('{date_from}T00:00:00Z')::timestamp_ntz)
and usage_date < date_trunc('day', ('{date_to}T00:00:00Z')::timestamp_ntz)
group by 1, 2, 3
union all
select convert_timezone('UTC', usage_date) as usage_date,
       'Stages' as object_name,
       'stage' as object_type,
       0 as database_bytes,
       0 as failsafe_bytes,
       max(AVERAGE_STAGE_BYTES) as stage_bytes
from snowflake.account_usage.stage_storage_usage_history
where usage_date >= date_trunc('day', ('{date_from}T00:00:00Z')::timestamp_ntz)
and usage_date < date_trunc('day', ('{date_to}T00:00:00Z')::timestamp_ntz)
group by 1, 2, 3;
"""

DATA_TRANSFER_QUERY = """
select date_trunc('hour', convert_timezone('UTC', start_time)) as start_time,
       target_cloud,
       target_region,
       transfer_type,
       sum(bytes_transferred) as bytes_transferred
from snowflake.account_usage.data_transfer_history
where start_time >= convert_timezone('UTC', 'UTC', ('{date_from}T00:00:00Z')::timestamp_ltz)
and start_time < convert_timezone('UTC', 'UTC', ('{date_to}T00:00:00Z')::timestamp_ltz)
group by 1, 2, 3, 4;
"""

USERS_QUERY = """
with USER_HOUR_EXECUTION_CTE as
  (select USER_NAME ,
          WAREHOUSE_NAME ,
          DATE_TRUNC('hour', START_TIME) as START_TIME_HOUR ,
          SUM(EXECUTION_TIME) as USER_HOUR_EXECUTION_TIME
   from "SNOWFLAKE"."ACCOUNT_USAGE"."QUERY_HISTORY"
   where WAREHOUSE_NAME is not null
     and EXECUTION_TIME > 0
     and START_TIME > convert_timezone('UTC', 'UTC', ('{date_from}T00:00:00Z')::timestamp_ltz)
     and START_TIME <= convert_timezone('UTC', 'UTC', ('{date_to}T00:00:00Z')::timestamp_ltz)
   group by 1,
            2,
            3),
     HOUR_EXECUTION_CTE as
  (select START_TIME_HOUR ,
          WAREHOUSE_NAME ,
          SUM(USER_HOUR_EXECUTION_TIME) as HOUR_EXECUTION_TIME
   from USER_HOUR_EXECUTION_CTE
   group by 1,
            2),
     APPROXIMATE_CREDITS as
  (select A.USER_NAME ,
          C.WAREHOUSE_NAME ,
          (A.USER_HOUR_EXECUTION_TIME/B.HOUR_EXECUTION_TIME)*C.CREDITS_USED as APPROXIMATE_CREDITS_USED
   from USER_HOUR_EXECUTION_CTE A
   join HOUR_EXECUTION_CTE B on A.START_TIME_HOUR = B.START_TIME_HOUR
   and B.WAREHOUSE_NAME = A.WAREHOUSE_NAME
   join "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" C on C.WAREHOUSE_NAME = A.WAREHOUSE_NAME
   and C.START_TIME = A.START_TIME_HOUR)
select USER_NAME,
       WAREHOUSE_NAME,
       SUM(APPROXIMATE_CREDITS_USED) as APPROXIMATE_CREDITS_USED
from APPROXIMATE_CREDITS
group by 1,
         2
order by 3 desc;
"""

if __name__ == "__main__":
    pass
