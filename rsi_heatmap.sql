{{ config(materialized='table') }}

with rsi_data as (
    select 
        date,
        symbol,
        rsi_14,
        current_timestamp() as load_timestamp
    from {{ ref('ma_rsi') }}
)

select * from rsi_data