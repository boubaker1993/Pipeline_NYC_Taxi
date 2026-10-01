select *
from {{ ref('stg_yellow_taxi') }}
where total_amount < 0
