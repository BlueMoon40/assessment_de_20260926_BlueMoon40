{{ config(materialized='table') }}

select
    city,
    date,
    round(avg(temperature_2m_mean), 2) as avg_temperature,
    round(max(temperature_2m_max), 2) as max_temperature,
    round(min(temperature_2m_min), 2) as min_temperature,
    round(sum(precipitation_sum), 2) as total_precipitation
from {{ ref('stg_weather_daily') }}
group by
    city,
    date
