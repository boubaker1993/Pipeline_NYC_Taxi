select
    pickup_location_id,
    count(*) as total_trips,
    count(distinct dropoff_location_id) as distinct_dropoff_zones,
    round(avg(trip_distance), 2) as avg_distance_miles,
    round(avg(trip_duration_minutes), 2) as avg_duration_minutes,
    round(avg(avg_speed_mph), 2) as avg_speed_mph,
    round(avg(total_amount), 2) as avg_trip_amount,
    round(sum(total_amount), 2) as total_revenue,
    round(avg(tip_amount), 2) as avg_tip_amount
from {{ ref('stg_yellow_taxi') }}
group by pickup_location_id
