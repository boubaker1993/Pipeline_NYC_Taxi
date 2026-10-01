select *
from {{ ref('stg_yellow_taxi') }}
where dropoff_datetime <= pickup_datetime
