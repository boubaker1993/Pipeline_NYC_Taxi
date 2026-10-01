{{ config(alias='yellow_taxi') }}

with cleaned as (
    select
        VENDORID as vendor_id,
        to_timestamp_ntz(TPEP_PICKUP_DATETIME / 1000000) as pickup_datetime,
        to_timestamp_ntz(TPEP_DROPOFF_DATETIME / 1000000) as dropoff_datetime,
        PASSENGER_COUNT as passenger_count,
        TRIP_DISTANCE as trip_distance,
        RATECODEID as rate_code_id,
        STORE_AND_FWD_FLAG as store_and_forward_flag,
        PULOCATIONID as pickup_location_id,
        DOLOCATIONID as dropoff_location_id,
        PAYMENT_TYPE as payment_type,
        FARE_AMOUNT as fare_amount,
        EXTRA as extra,
        MTA_TAX as mta_tax,
        TIP_AMOUNT as tip_amount,
        TOLLS_AMOUNT as tolls_amount,
        IMPROVEMENT_SURCHARGE as improvement_surcharge,
        TOTAL_AMOUNT as total_amount,
        CONGESTION_SURCHARGE as congestion_surcharge,
        AIRPORT_FEE as airport_fee,
        CBD_CONGESTION_FEE as cbd_congestion_fee
    from {{ source('raw', 'yellow_taxi_raw') }}
),

enriched as (
    select
        *,
        datediff('second', pickup_datetime, dropoff_datetime) as trip_duration_seconds,
        datediff('second', pickup_datetime, dropoff_datetime) / 60.0 as trip_duration_minutes,
        to_date(pickup_datetime) as trip_date,
        extract(hour from pickup_datetime) as pickup_hour
    from cleaned
)

select
    *,
    case
        when trip_duration_seconds > 0 and trip_distance > 0
        then trip_distance / (trip_duration_seconds / 3600.0)
        else null
    end as avg_speed_mph,
    case
        when trip_distance < 1 then 'SHORT'
        when trip_distance < 5 then 'MEDIUM'
        when trip_distance < 15 then 'LONG'
        when trip_distance >= 15 then 'VERY_LONG'
        else 'INVALID'
    end as distance_category,
    case
        when trip_duration_minutes < 10 then 'SHORT'
        when trip_duration_minutes < 30 then 'MEDIUM'
        when trip_duration_minutes < 60 then 'LONG'
        when trip_duration_minutes >= 60 then 'VERY_LONG'
        else 'INVALID'
    end as duration_category,
    case
        when pickup_hour between 6 and 9 then 'MORNING_RUSH'
        when pickup_hour between 10 and 15 then 'DAYTIME'
        when pickup_hour between 16 and 19 then 'EVENING_RUSH'
        else 'NIGHT'
    end as time_period
from enriched
where pickup_datetime is not null
  and dropoff_datetime is not null
  and dropoff_datetime > pickup_datetime
  and trip_distance > 0
  and trip_distance <= 1000
  and total_amount >= 0
