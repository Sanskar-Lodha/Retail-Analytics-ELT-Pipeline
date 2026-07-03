WITH shops AS (

    SELECT
        shop:shop_id::VARCHAR AS shop_id,
        shop:shop_name::VARCHAR AS shop_name,
        shop:country::VARCHAR AS shop_country,
        meta:marketplace::VARCHAR AS marketplace,
        meta:seller_id::VARCHAR AS seller_id,
        ROW_NUMBER() OVER (
            PARTITION BY shop:shop_id::VARCHAR
            ORDER BY order_date DESC
        ) AS rn

    FROM {{ ref('orders_stg') }}

)

SELECT
    shop_id,
    shop_name,
    shop_country,
    marketplace,
    seller_id
FROM shops
WHERE rn = 1