select
    city,
    date,
    count(*) as row_count
from {{ ref('daily_weather') }}
group by
    city,
    date
having count(*) > 1