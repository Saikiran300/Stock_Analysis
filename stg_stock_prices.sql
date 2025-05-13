with raw as (
  select
    date,
    open::float   as open,
    high::float   as high,
    low::float    as low,
    close::float  as close,
    volume::bigint as volume,
    symbol
  from {{ source('raw', 'stock_prices') }}
)

select
  date,
  open,
  high,
  low,
  close,
  volume,
  symbol
from raw