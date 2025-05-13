{% snapshot stock_summary_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='symbol',
        strategy='check',
        check_cols=['avg_rsi', 'avg_ma_20', 'avg_ma_50', 'first_date', 'last_date']
    )
}}

select *
from {{ ref('stock_summary') }}

{% endsnapshot %}