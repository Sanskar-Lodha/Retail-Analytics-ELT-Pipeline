WITH orders AS (

    SELECT *
    FROM {{ ref('orders_stg') }}

),

flattened_events AS (

    SELECT
        o.order_id,
        e.value:event_name::VARCHAR AS event_name,
        e.value:event_timestamp::TIMESTAMP_NTZ AS event_timestamp

    FROM orders o,
    LATERAL FLATTEN(input => o.events) e

)

SELECT *
FROM flattened_events