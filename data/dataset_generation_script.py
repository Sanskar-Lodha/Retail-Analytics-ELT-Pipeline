import os
import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# allow quick test overrides via environment variables
NUM_CUSTOMERS = int(os.getenv("NUM_CUSTOMERS", "10000"))
NUM_PRODUCTS = int(os.getenv("NUM_PRODUCTS", "5000"))
NUM_SHOPS = int(os.getenv("NUM_SHOPS", "100"))
NUM_ORDERS = int(os.getenv("NUM_ORDERS", "50000"))

# -----------------------------
# MASTER DATA
# -----------------------------

# FIX: country_weights was referenced in get_country() but never defined
country_weights = {
    "India": 50,
    "USA": 20,
    "UK": 10,
    "Germany": 8,
    "Australia": 5,
    "Canada": 4,
    "Singapore": 3,
}

# simple currency map for countries used in generated data
currency_map = {
    "India": "INR",
    "USA": "USD",
    "UK": "GBP",
    "Germany": "EUR",
    "Australia": "AUD",
    "Canada": "CAD",
    "Singapore": "SGD",
}

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Wallet",
    "COD"
]

category_weights = {
    "Electronics": 34,
    "Fashion": 24,
    "Sports": 14,
    "Beauty": 10,
    "Books": 8,
    "Furniture": 6,
    "Toys": 4
}

price_ranges = {
    "Electronics": (5000, 90000),
    "Fashion": (600, 8000),
    "Books": (200, 2500),
    "Furniture": (5000, 60000),
    "Beauty": (250, 3500),
    "Sports": (800, 15000),
    "Toys": (300, 7000)
}

discount_ranges = {
    "Electronics": (5, 15),
    "Fashion": (20, 50),
    "Books": (5, 15),
    "Furniture": (15, 30),
    "Beauty": (10, 30),
    "Sports": (10, 25),
    "Toys": (15, 35)
}

cost_margin_ranges = {
    "Electronics": (0.75, 0.90),
    "Fashion": (0.35, 0.55),
    "Books": (0.30, 0.45),
    "Furniture": (0.55, 0.75),
    "Beauty": (0.35, 0.50),
    "Sports": (0.45, 0.65),
    "Toys": (0.40, 0.60)
}

quantity_ranges = {
    "Electronics": (1, 1),
    "Fashion": (1, 3),
    "Books": (1, 5),
    "Furniture": (1, 1),
    "Beauty": (1, 6),
    "Sports": (1, 2),
    "Toys": (1, 4)
}

marketplace_weights = {
    "amazon": 40,
    "flipkart": 25,
    "myntra": 15,
    "meesho": 10,
    "first_party": 10
}

month_weights = {
    1: 5,
    2: 6,
    3: 8,
    4: 8,
    5: 9,
    6: 10,
    7: 12,
    8: 14,
    9: 16,
    10: 18,
    11: 25,
    12: 30
}

product_catalog = {
    "Electronics": [
        ("iPhone 15", 18),
        ("Galaxy S24", 16),
        ("MacBook Air", 12),
        ("AirPods Pro", 10),
        ("Boat Rockerz", 14),
        ("Dell Inspiron", 10),
        ("HP Pavilion", 8),
        ("Sony WH1000XM5", 12)
    ],
    "Fashion": [
        ("Air Max Shoes", 18),
        ("Ultraboost", 16),
        ("Running Jacket", 14),
        ("Sports Hoodie", 12),
        ("Sneakers", 10),
        ("Denim Jeans", 8),
        ("Leather Jacket", 6),
        ("Summer Dress", 6)
    ],
    "Books": [
        ("Python Programming", 18),
        ("SQL Cookbook", 16),
        ("Machine Learning Basics", 14),
        ("Data Engineering Handbook", 12),
        ("The Startup Way", 10),
        ("Deep Work", 8),
        ("Atomic Habits", 8),
        ("Zero to One", 6)
    ],
    "Furniture": [
        ("Office Chair", 18),
        ("Study Table", 16),
        ("Wooden Shelf", 14),
        ("Bookshelf", 12),
        ("Sofa Set", 10),
        ("Dining Table", 8),
        ("Wardrobe", 8),
        ("TV Unit", 6)
    ],
    "Beauty": [
        ("Face Wash", 18),
        ("Shampoo", 16),
        ("Moisturizer", 14),
        ("Sunscreen", 12),
        ("Lipstick", 10),
        ("Perfume", 8),
        ("Body Lotion", 8),
        ("Serum", 6)
    ],
    "Sports": [
        ("Football", 18),
        ("Basketball", 16),
        ("Cricket Bat", 14),
        ("Yoga Mat", 12),
        ("Tennis Racket", 10),
        ("Fitness Band", 8),
        ("Running Shoes", 12)
    ],
    "Toys": [
        ("Building Blocks", 18),
        ("Remote Car", 16),
        ("Puzzle Set", 14),
        ("Action Figure", 12),
        ("Board Game", 10),
        ("Doll House", 8),
        ("Toy Train", 6)
    ]
}

shop_names = [
    "Amazon India",
    "Flipkart Electronics",
    "Nike Store Mumbai",
    "Samsung Experience Store",
    "Apple Premium Reseller",
    "Reliance Digital",
    "Croma",
    "Boat Official",
    "Myntra Fashion Hub",
    "Meesho Marketplace"
]

def weighted_choice(options):
    choices, weights = zip(*options)
    return random.choices(choices, weights=weights, k=1)[0]


def get_country():
    return random.choices(list(country_weights.keys()), weights=country_weights.values(), k=1)[0]


def get_shop_name():
    return random.choice(shop_names)


def get_marketplace():
    return random.choices(list(marketplace_weights.keys()), weights=marketplace_weights.values(), k=1)[0]


def get_order_date():
    year = random.choice([datetime.now().year - 1, datetime.now().year])
    month = random.choices(list(month_weights.keys()), weights=month_weights.values(), k=1)[0]
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime(year, month, day, hour, minute, second)


def get_product_name(category):
    return weighted_choice(product_catalog[category])


def get_quantity(category):
    min_q, max_q = quantity_ranges[category]
    return random.randint(min_q, max_q)


def get_discount(category):
    low, high = discount_ranges[category]
    return random.randint(low, high)


def get_cost_price(listed_price, category):
    low, high = cost_margin_ranges[category]
    return round(listed_price * random.uniform(low, high), 2)

brand_map = {

    "Electronics": [
        "Apple",
        "Samsung",
        "Sony",
        "Dell",
        "HP",
        "Boat"
    ],

    "Fashion": [
        "Nike",
        "Adidas",
        "Puma"
    ],

    "Sports": [
        "Nike",
        "Adidas",
        "Puma"
    ],

    "Books": [
        "Penguin",
        "Oxford",
        "HarperCollins"
    ],

    "Furniture": [
        "IKEA",
        "Nilkamal",
        "Godrej"
    ],

    "Beauty": [
        "L'Oreal",
        "Maybelline",
        "Dove"
    ],

    "Toys": [
        "Lego",
        "Mattel",
        "Hasbro"
    ]
}

# -----------------------------
# CUSTOMERS
# -----------------------------

customers = []

for i in range(NUM_CUSTOMERS):

    # signup_date left general here; we'll ensure per-order that signup_date <= order_date
    customers.append({
        "customer_id": f"CUST{i}",
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "gender": random.choice(["Male", "Female", "Other"]),
        "signup_date": fake.date_between(start_date='-5y', end_date='-1d').isoformat()
    })

# -----------------------------
# PRODUCTS

products = []

for i in range(NUM_PRODUCTS):
    category = random.choices(list(category_weights.keys()), weights=category_weights.values(), k=1)[0]
    products.append({
        "product_id": f"PROD{i}",
        "product_name": get_product_name(category),
        "brand": random.choice(brand_map[category]),
        "category": category
    })

# -----------------------------
# SHOPS
# -----------------------------

shops = []

for i in range(NUM_SHOPS):
    shops.append({
        "shop_id": f"SHOP{i}",
        "shop_name": get_shop_name(),
        "country": get_country()
    })

# -----------------------------
# ORDER GENERATION
# -----------------------------

orders = []

for i in range(NUM_ORDERS):

    customer = random.choice(customers)
    shop = random.choice(shops)

    order_date = get_order_date()

    # pick an order shipping country up-front so currency can be attached
    order_country = get_country()
    order_currency = currency_map.get(order_country, "USD")

    item_count = random.randint(1, 5)

    items = []

    subtotal = 0

    for item_idx in range(item_count):

        product = random.choice(products)

        listed_price = round(
            random.uniform(*price_ranges[product["category"]]),
            2
        )

        discount_percent = get_discount(product["category"])

        quantity = get_quantity(product["category"])

        paid_price = round(
            listed_price * (1 - discount_percent / 100),
            2
        )

        # cost price (merchant cost) - kept separate so margin can be computed in dbt
        cost_price = get_cost_price(listed_price, product["category"])

        # note: we intentionally DO NOT store derived per-item revenue/aggregates
        # such as item_revenue or order subtotal/total so dbt can compute them
        # from raw `paid_price` and `quantity`.

        items.append({
            "item_id": f"ITEM{ i }_{ item_idx }",
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "brand": product["brand"],
            "category": product["category"],
            "listed_price": listed_price,
            "paid_price": paid_price,
            "cost_price": cost_price,
            "discount_percent": discount_percent,
            "quantity": quantity,
            "added_timestamp": (
                order_date - timedelta(minutes=random.randint(5, 180))
            ).isoformat()
        })

    # defensive: remove item-level currency if present from any prior edits
    for _it in items:
        if "currency" in _it:
            _it.pop("currency")

    # don't expose derived subtotal/total/gst here; keep raw fields only
    shipping_cost = round(random.uniform(50, 300), 2)

    # Decide event sequence with probabilities; most orders are delivered,
    # but some are cancelled or returned. When returned/cancelled, include
    # the full prior lifecycle events so downstream models can reconstruct flows.
    r = random.random()

    if r < 0.75:
        # normal delivered flow
        statuses = [
            "CREATED",
            "PACKED",
            "SHIPPED",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
        ]
    elif r < 0.80:
        # early cancellation
        statuses = ["CREATED", "CANCELLED"]
    elif r < 0.86:
        # cancelled after pack
        statuses = ["CREATED", "PACKED", "CANCELLED"]
    elif r < 0.95:
        # returned after delivery (full lifecycle)
        statuses = [
            "CREATED",
            "PACKED",
            "SHIPPED",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "RETURN_REQUESTED",
            "PICKUP_COMPLETED",
            "RETURNED",
        ]
    else:
        # rare: lost/in-transit/other
        statuses = [
            "CREATED",
            "PACKED",
            "SHIPPED",
            "IN_TRANSIT",
        ]

    events = []
    current_time = order_date
    for status in statuses:
        # variable delays to simulate messy real-world events
        current_time += timedelta(hours=random.randint(1, 72))
        events.append({
            "event_name": status,
            "event_timestamp": current_time.isoformat(),
        })

    orders.append({
        "order_id": f"ORD{i}",
        "order_date": order_date.isoformat(),
        "customer": {
            "customer_id": customer["customer_id"],
            "name": customer["name"],
            "email": customer["email"],
            "phone": customer["phone"],
            "gender": customer["gender"],
            # ensure signup_date is before order_date
            "signup_date": (order_date - timedelta(days=random.randint(1, 365 * 3))).date().isoformat()
        },
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "country": order_country,
            "zipcode": fake.postcode(),
        },
        "shop": {
            "shop_id": shop["shop_id"],
            "shop_name": shop["shop_name"],
            "country": shop["country"],
        },
        "pricing": {
            "shipping_cost": shipping_cost,
            "payment_method": random.choice(payment_methods),
            "payment_status": (
                "REFUNDED" if any(s in ["CANCELLED", "RETURNED"] for s in statuses)
                else ("PAID" if random.random() < 0.85 else ("PENDING" if random.random() < 0.5 else "FAILED"))
            ),
            "promo_code": random.choice([None, None, f"PROMO{random.randint(5,50)}"]),
        },
        "currency": order_currency,
        "items": items,
        "events": events,
        "tracking": {
            "courier_partner": (
                (random.choice(["DHL", "FedEx", "Delhivery", "BlueDart", "EcomExpress"]) if random.random() < 0.9 else None)
                if "SHIPPED" in statuses else None
            ),
            "tracking_id": (f"TRK{random.randint(1000000,9999999)}" if "SHIPPED" in statuses else None),
            "fulfillment_center_id": f"FC{random.randint(1,50)}",
        },
        "meta": {
            "seller_id": f"SELL{random.randint(1,300)}",
            "marketplace": get_marketplace()
        }
    })

# -----------------------------
# SAVE JSON
# -----------------------------

with open(
    "raw_orders.json",
    "w",
    encoding="utf-8"
) as f:

    # defensive cleanup: ensure RAW file has no derived aggregations or item-level currency
    for _o in orders:
        if "order_quantity" in _o:
            del _o["order_quantity"]
        for _it in _o.get("items", []):
            _it.pop("currency", None)

    json.dump(orders, f, indent=2)

print(
    f"Generated {NUM_ORDERS} Orders"
)