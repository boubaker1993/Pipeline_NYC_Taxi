select *
from {{ ref('stg_yellow_taxi') }}
where trip_distance <= 0
   or trip_distance > 1000
