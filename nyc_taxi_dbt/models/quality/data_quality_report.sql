select
    count(*) as total_rows,
    count_if(PASSENGER_COUNT is null) as missing_passenger_count,
    count_if(TRIP_DISTANCE is null) as missing_trip_distance,
    count_if(TOTAL_AMOUNT is null) as missing_total_amount,
    count_if(TPEP_PICKUP_DATETIME is null) as missing_pickup,
    count_if(TPEP_DROPOFF_DATETIME is null) as missing_dropoff,
    count_if(TOTAL_AMOUNT < 0) as negative_amounts,
    round(100 * count_if(TOTAL_AMOUNT < 0) / count(*), 2) as negative_amount_pct,
    count_if(TRIP_DISTANCE = 0) as zero_distance,
    round(100 * count_if(TRIP_DISTANCE = 0) / count(*), 2) as zero_distance_pct,
    count_if(TRIP_DISTANCE > 1000) as extreme_distance
from {{ source('raw', 'yellow_taxi_raw') }}
