WITH base AS (

    SELECT
        JSON:order_id::VARCHAR AS order_id,
        JSON:order_date::TIMESTAMP_NTZ AS order_date,
        JSON:currency::VARCHAR AS currency,
        JSON:customer.customer_id::VARCHAR AS customer_id,
        JSON:pricing.shipping_cost::FLOAT AS shipping_cost,
        JSON:items::VARIANT AS items,
        JSON:pricing.promo_code::VARCHAR AS promo_code,
        JSON:tracking.fulfillment_center_id::VARCHAR AS fulfillment_center_id,
        JSON:events::VARIANT AS events,
        JSON:meta::VARIANT AS meta,
        JSON:shop::VARIANT AS shop,
        JSON:tracking::VARIANT AS tracking,
        JSON:customer::VARIANT AS customer,
        JSON:address.city::VARCHAR AS delivery_city,
        JSON:address.country::VARCHAR AS delivery_country,
        JSON:address.state::VARCHAR AS delivery_state,
        JSON:address.street::VARCHAR AS delivery_street,
        JSON:address.zipcode::VARCHAR AS delivery_zipcode
    FROM {{ source('raw', 'RAW_ORDERS') }}

),

currency_rates AS (

    SELECT *
    FROM (VALUES
        ('USD', 1.0),      
        ('INR', 0.01058),   
        ('GBP', 1.321),     
        ('EUR', 1.147),    
        ('AUD', 0.701),    
        ('CAD', 0.707),    
        ('SGD', 0.771)     
    ) AS t(currency, usd_rate)

),

item_totals AS (

    SELECT
        b.order_id,
        SUM(f.value:paid_price::FLOAT)    AS items_total,
        SUM(f.value:listed_price::FLOAT)  AS items_listed_total,
        SUM(f.value:cost_price::FLOAT)    AS items_cost_total,
        COUNT(*)                           AS item_count
    FROM base b,
         LATERAL FLATTEN(input => b.items) f
    GROUP BY b.order_id

),

joined AS (

    SELECT
        b.order_date,
        b.order_id,
        b.customer_id,
        b.fulfillment_center_id,
        b.currency,
        cr.usd_rate,
        b.shipping_cost AS shipping_cost,
        it.items_total AS items_total,
        it.items_listed_total AS items_listed_total,
        it.items_cost_total AS items_cost_total,
        (it.items_total + b.shipping_cost) AS order_total,
        ROUND(b.shipping_cost * cr.usd_rate, 2) AS shipping_cost_usd,
        ROUND(it.items_total * cr.usd_rate, 2) AS items_total_usd,
        ROUND(it.items_listed_total * cr.usd_rate, 2) AS items_listed_total_usd,
        ROUND(it.items_cost_total * cr.usd_rate, 2) AS items_cost_total_usd,
        ROUND((it.items_total + b.shipping_cost) * cr.usd_rate, 2) AS order_total_usd,
        b.promo_code,
        it.item_count,
        b.items,
        b.events,
        b.delivery_city,
        b.delivery_country,
        b.delivery_state,
        b.delivery_street,
        b.delivery_zipcode,
        b.meta,
        b.shop,
        b.tracking,
        b.customer

    FROM base b
    JOIN item_totals it ON b.order_id = it.order_id
    LEFT JOIN currency_rates cr ON b.currency = cr.currency

)

SELECT * FROM joined