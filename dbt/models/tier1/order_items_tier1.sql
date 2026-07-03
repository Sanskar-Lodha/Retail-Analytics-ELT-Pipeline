WITH order_items AS (

    SELECT *
    FROM {{ ref('order_items_stg') }}

),

orders AS (

    SELECT
        order_id,
        shop_id,
        current_status,
        is_cancelled,
        is_delivered
    FROM {{ ref('orders_tier1') }}

)

SELECT
    oi.order_id,
    oi.item_id,
    oi.order_date,
    oi.customer_id,
    o.shop_id,
    oi.product_id,
    oi.product_name,
    oi.brand,
    oi.category,
    oi.quantity,
    oi.currency,
    oi.usd_rate,
    oi.cost_price,
    oi.listed_price,
    oi.paid_price,
    oi.discount_pct,
    oi.cost_price_usd,
    oi.listed_price_usd,
    oi.paid_price_usd,
    o.current_status,
    o.is_cancelled,
    o.is_delivered,
    oi.paid_price * oi.quantity AS gross_item_revenue,
    (oi.listed_price - oi.paid_price) * oi.quantity AS discount_amount,
    oi.cost_price * oi.quantity AS total_cost,
    (oi.paid_price - oi.cost_price)  * oi.quantity  AS gross_margin,
    oi.paid_price_usd * oi.quantity AS gross_item_revenue_usd,
    (oi.listed_price_usd - oi.paid_price_usd) * oi.quantity AS discount_amount_usd,
    oi.cost_price_usd * oi.quantity AS total_cost_usd,
    (oi.paid_price_usd - oi.cost_price_usd)* oi.quantity AS gross_margin_usd

FROM order_items oi

LEFT JOIN orders o
    ON oi.order_id = o.order_id