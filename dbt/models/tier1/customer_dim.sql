WITH customers AS (

    SELECT
        customer:customer_id::VARCHAR AS customer_id,
        customer:name::VARCHAR AS customer_name,
        customer:email::VARCHAR AS email,
        customer:gender::VARCHAR AS gender,
        customer:phone::VARCHAR AS phone,
        customer:signup_date::DATE AS signup_date,

        ROW_NUMBER() OVER (
            PARTITION BY customer:customer_id::VARCHAR
            ORDER BY order_date DESC
        ) AS rn

    FROM {{ ref('orders_stg') }}

)

SELECT
    customer_id,
    customer_name,
    email,
    gender,
    phone,
    signup_date
FROM customers
WHERE rn = 1