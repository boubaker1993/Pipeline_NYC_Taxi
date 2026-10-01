select
    pickup_hour,
    time_period,
    count(*) as total_trips,
    round(avg(trip_distance), 2) as avg_distance_miles,
    round(avg(trip_duration_minutes), 2) as avg_duration_minutes,
    round(avg(avg_speed_mph), 2) as avg_speed_mph,
    round(avg(total_amount), 2) as avg_trip_amount,
    round(sum(total_amount), 2) as total_revenue
from {{ ref('stg_yellow_taxi') }}
group by pickup_hour, time_period
order by pickup_hour
