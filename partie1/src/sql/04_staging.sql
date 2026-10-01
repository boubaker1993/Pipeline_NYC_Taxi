USE DATABASE NYC_TAXI_DB_PARTIE_1;
USE SCHEMA STAGING;

CREATE OR REPLACE TABLE YELLOW_TAXI AS
WITH cleaned AS (
    SELECT
        VENDORID AS vendor_id,
        TO_TIMESTAMP_NTZ(TPEP_PICKUP_DATETIME / 1000000) AS pickup_datetime,
        TO_TIMESTAMP_NTZ(TPEP_DROPOFF_DATETIME / 1000000) AS dropoff_datetime,
        PASSENGER_COUNT AS passenger_count,
        TRIP_DISTANCE AS trip_distance,
        RATECODEID AS rate_code_id,
        STORE_AND_FWD_FLAG AS store_and_forward_flag,
        PULOCATIONID AS pickup_location_id,
        DOLOCATIONID AS dropoff_location_id,
        PAYMENT_TYPE AS payment_type,
        FARE_AMOUNT AS fare_amount,
        EXTRA AS extra,
        MTA_TAX AS mta_tax,
        TIP_AMOUNT AS tip_amount,
        TOLLS_AMOUNT AS tolls_amount,
        IMPROVEMENT_SURCHARGE AS improvement_surcharge,
        TOTAL_AMOUNT AS total_amount,
        CONGESTION_SURCHARGE AS congestion_surcharge,
        AIRPORT_FEE AS airport_fee,
        CBD_CONGESTION_FEE AS cbd_congestion_fee
    FROM NYC_TAXI_DB_PARTIE_1.RAW.YELLOW_TAXI_RAW
), enriched AS (
    SELECT
        *,
        DATEDIFF('second', pickup_datetime, dropoff_datetime) AS trip_duration_seconds,
        DATEDIFF('second', pickup_datetime, dropoff_datetime) / 60.0 AS trip_duration_minutes,
        TO_DATE(pickup_datetime) AS trip_date,
        EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour
    FROM cleaned
)
SELECT
    *,
    CASE
        WHEN trip_duration_seconds > 0 AND trip_distance > 0
        THEN trip_distance / (trip_duration_seconds / 3600.0)
        ELSE NULL
    END AS avg_speed_mph,
    CASE
        WHEN trip_distance < 1 THEN 'SHORT'
        WHEN trip_distance < 5 THEN 'MEDIUM'
        WHEN trip_distance < 15 THEN 'LONG'
        WHEN trip_distance >= 15 THEN 'VERY_LONG'
        ELSE 'INVALID'
    END AS distance_category,
    CASE
        WHEN trip_duration_minutes < 10 THEN 'SHORT'
        WHEN trip_duration_minutes < 30 THEN 'MEDIUM'
        WHEN trip_duration_minutes < 60 THEN 'LONG'
        WHEN trip_duration_minutes >= 60 THEN 'VERY_LONG'
        ELSE 'INVALID'
    END AS duration_category,
    CASE
        WHEN pickup_hour BETWEEN 6 AND 9 THEN 'MORNING_RUSH'
        WHEN pickup_hour BETWEEN 10 AND 15 THEN 'DAYTIME'
        WHEN pickup_hour BETWEEN 16 AND 19 THEN 'EVENING_RUSH'
        ELSE 'NIGHT'
    END AS time_period
FROM enriched
WHERE pickup_datetime IS NOT NULL
  AND dropoff_datetime IS NOT NULL
  AND dropoff_datetime > pickup_datetime
  AND trip_distance > 0
  AND trip_distance <= 1000
  AND total_amount >= 0;
