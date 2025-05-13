-- models/analytics/stock_summary.sql
{{ config(materialized='table') }}

with stats as (
    select 
        symbol,
        round(avg(rsi_14), 2) as avg_rsi,
        round(avg(ma_20), 2) as avg_ma_20,
        round(avg(ma_50), 2) as avg_ma_50,
        min(date) as start_date,
        max(date) as end_date,
        current_timestamp() as load_timestamp
    from {{ ref('ma_rsi') }}
    group by symbol
)

select * from stats
