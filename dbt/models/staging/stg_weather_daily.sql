select
    city,
    date,
    temperature_2m_mean,
    temperature_2m_max,
    temperature_2m_min,
    precipitation_sum
from {{ source('weather', 'weather_daily') }}