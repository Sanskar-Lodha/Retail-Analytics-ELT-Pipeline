WITH latest_event AS (

    SELECT
        order_id,
        event_name,
        event_timestamp,

        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY event_timestamp DESC
        ) AS rn

    FROM {{ ref('order_events_stg') }}

),

orders_with_status AS (

    SELECT
        o.order_id,
        o.order_date,
        TO_DATE(o.order_date) AS order_day,
        DATE_TRUNC('week', o.order_date) AS order_week,
        DATE_TRUNC('month', o.order_date) AS order_month,
        YEAR(o.order_date) AS order_year,
        MONTH(o.order_date) AS order_month_number,
        MONTHNAME(o.order_date) AS order_month_name,
        DAYNAME(o.order_date) AS day_name,
        DAY(o.order_date) AS day_of_month,
        WEEKOFYEAR(o.order_date) AS week_number,
        QUARTER(o.order_date) AS order_quarter_number,
        DATE_TRUNC('quarter', o.order_date) AS order_quarter,
        TO_CHAR(o.order_date, 'YYYY-MM') AS order_year_month,
        o.customer_id,
        o.shop:shop_id::VARCHAR AS shop_id,
        o.currency,
        o.usd_rate,
        o.shipping_cost,
        o.shipping_cost_usd,
        o.items_total,
        o.items_total_usd,
        o.item_count,
        o.promo_code,
        o.delivery_city,
        o.delivery_country,
        o.delivery_state,
        o.delivery_street,
        o.delivery_zipcode,
        o.fulfillment_center_id,
        le.event_name AS current_status,
        le.event_timestamp AS current_status_timestamp

    FROM {{ ref('orders_stg') }} o

    LEFT JOIN latest_event le
        ON o.order_id = le.order_id
       AND le.rn = 1

)

SELECT
    order_id,
    order_date,
    order_day,
    order_week,
    order_month,
    order_month_number,
    order_year,
    order_month_name,
    day_name,
    day_of_month,
    week_number,
    order_quarter_number,
    order_year_month,
    order_quarter,
    customer_id,
    shop_id,
    currency,
    usd_rate,
    current_status,
    current_status_timestamp,
    item_count,
    promo_code,
    shipping_cost,
    items_total,
    items_total + shipping_cost AS gross_order_value,
    items_total / NULLIF(item_count, 0) AS avg_item_value,
    shipping_cost_usd,
    items_total_usd,
    items_total_usd + shipping_cost_usd AS gross_order_value_usd,
    items_total_usd / NULLIF(item_count, 0) AS avg_item_value_usd,
    CASE WHEN current_status = 'CANCELLED' THEN 1 ELSE 0 END AS is_cancelled,
    CASE WHEN current_status = 'DELIVERED' THEN 1 ELSE 0 END AS is_delivered,
    CASE
        WHEN current_status = 'DELIVERED'
        THEN items_total + shipping_cost
        ELSE 0
    END AS realized_revenue,

    CASE
        WHEN current_status = 'CANCELLED'
        THEN items_total + shipping_cost
        ELSE 0
    END AS cancelled_value,
    CASE
        WHEN current_status = 'DELIVERED'
        THEN items_total_usd + shipping_cost_usd
        ELSE 0
    END AS realized_revenue_usd,

    CASE
        WHEN current_status = 'CANCELLED'
        THEN items_total_usd + shipping_cost_usd
        ELSE 0
    END AS cancelled_value_usd,
    delivery_city,
    delivery_country,
    delivery_state,
    delivery_street,
    delivery_zipcode,
    fulfillment_center_id
FROM orders_with_status