WITH ordered_events AS (
    SELECT
        order_id,
        event_name,
        event_timestamp,
        LEAD(event_name) OVER (
            PARTITION BY order_id ORDER BY event_timestamp
        ) AS next_event_name
    FROM {{ ref('order_events_stg') }}
)

SELECT
    order_id,
    event_name AS from_stage,
    next_event_name AS to_stage
FROM ordered_events
WHERE next_event_name IS NOT NULL