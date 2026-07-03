WITH orders AS (

    SELECT * FROM {{ ref('orders_stg') }}

),

flattened_items AS (

    SELECT
        o.order_id::VARCHAR AS order_id,
        f.value:item_id::VARCHAR AS item_id,
        o.order_date::TIMESTAMP_NTZ AS order_date,
        o.customer_id::VARCHAR AS customer_id,
        f.value:brand::VARCHAR AS brand,
        f.value:category::VARCHAR AS category,
        o.currency,
        o.usd_rate,
        f.value:cost_price::NUMBER(10,2) AS cost_price,
        f.value:discount_percent::NUMBER(10,2) AS discount_pct,
        f.value:listed_price::NUMBER(10,2) AS listed_price,
        f.value:paid_price::NUMBER(10,2) AS paid_price,
        f.value:quantity::NUMBER(10,0) AS quantity,
        ROUND(f.value:paid_price::FLOAT * f.value:quantity::FLOAT, 2) AS item_revenue,
        ROUND(f.value:listed_price::FLOAT * f.value:quantity::FLOAT, 2) AS item_listed_revenue,
        ROUND(f.value:cost_price::FLOAT * f.value:quantity::FLOAT, 2) AS item_cost,
        ROUND(f.value:cost_price::FLOAT * o.usd_rate, 2) AS cost_price_usd,
        ROUND(f.value:listed_price::FLOAT * o.usd_rate, 2) AS listed_price_usd,
        ROUND(f.value:paid_price::FLOAT * o.usd_rate, 2) AS paid_price_usd,
        ROUND(f.value:paid_price::FLOAT * f.value:quantity::FLOAT * o.usd_rate, 2) AS item_revenue_usd,
        ROUND(f.value:listed_price::FLOAT * f.value:quantity::FLOAT * o.usd_rate, 2) AS item_listed_revenue_usd,
        ROUND(f.value:cost_price::FLOAT  * f.value:quantity::FLOAT * o.usd_rate, 2) AS item_cost_usd,
        f.value:product_id::VARCHAR AS product_id,
        f.value:product_name::VARCHAR AS product_name,
        o.delivery_city,
        o.delivery_country,
        o.delivery_state,
        o.delivery_street,
        o.delivery_zipcode

    FROM orders o,
    LATERAL FLATTEN(input => o.items) f

)

SELECT * FROM flattened_items