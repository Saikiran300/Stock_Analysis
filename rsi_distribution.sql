{{ config(materialized='table') }}

with rsi_values as (
    select 
        symbol,
        date,
        rsi_14,
        lag(rsi_14) over (partition by symbol order by date) as prev_rsi,
        current_timestamp() as load_timestamp
    from {{ ref('ma_rsi') }}
),

rsi_changes as (
    select 
        symbol,
        rsi_14,
        case 
            when prev_rsi != 0 then round((rsi_14 - prev_rsi) / prev_rsi * 100, 2)
            else null 
        end as rsi_change_pct,
        load_timestamp
    from rsi_values
)

select * from rsi_changes



