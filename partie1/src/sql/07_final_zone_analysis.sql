USE DATABASE NYC_TAXI_DB_PARTIE_1;
USE SCHEMA FINAL;

CREATE OR REPLACE TABLE ZONE_ANALYSIS AS
SELECT
    pickup_location_id,
    COUNT(*) AS total_trips,
    COUNT(DISTINCT dropoff_location_id) AS distinct_dropoff_zones,
    ROUND(AVG(trip_distance), 2) AS avg_distance_miles,
    ROUND(AVG(trip_duration_minutes), 2) AS avg_duration_minutes,
    ROUND(AVG(avg_speed_mph), 2) AS avg_speed_mph,
    ROUND(AVG(total_amount), 2) AS avg_trip_amount,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(tip_amount), 2) AS avg_tip_amount
FROM NYC_TAXI_DB_PARTIE_1.STAGING.YELLOW_TAXI
GROUP BY pickup_location_id;
