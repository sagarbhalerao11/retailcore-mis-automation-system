from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os

fake = Faker()

#INPUT_DIR = "input"

#os.makedirs(INPUT_DIR, exist_ok=True)


PRODUCTS = []

categories = [
    "Electronics",
    "Fashion",
    "Home",
    "Sports"
]

for i in range(1, 101):
    PRODUCTS.append(
        {
            "product_id": f"P{i:03}",
            "product_name": f"Product_{i}",
            "category": random.choice(categories)
        }
    )


def generate_sales_data():
    """
    Generate mock retail sales data containing
    order, product, pricing, region, and sales
    representative information.
    """
    sales = []

    regions = [
        "North",
        "South",
        "East",
        "West",
        "Central"
    ]

    sales_reps = [
        "Rahul",
        "Priya",
        "Amit",
        "Sneha",
        "Vikas",
        "Anjali"
    ]

    start_date = datetime.now() - timedelta(days=90)

    for i in range(1000):

        product = random.choice(PRODUCTS)

        sales.append(
            {
                "order_id": f"ORD{i+1:05}",
                "date": start_date + timedelta(
                    days=random.randint(0, 90)
                ),
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "region": random.choice(regions),
                "quantity_sold": random.randint(1, 20),
                "unit_price": round(
                    random.uniform(100, 10000),
                    2
                ),
                "discount_pct": random.choice(
                    [0, 5, 10, 15, None]
                ),
                "sales_rep": random.choice(sales_reps)
            }
        )

    df = pd.DataFrame(sales)

    return df


def add_dirty_data(df):
    """
    Introduce duplicate order IDs and negative
    quantity values to simulate real-world
    data quality issues.
    """

    # duplicate order ids
    duplicate_rows = df.sample(20)

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    # negative quantity
    negative_rows = df.sample(
        int(len(df) * 0.03)
    ).index

    df.loc[
        negative_rows,
        "quantity_sold"
    ] *= -1

    return df


def generate_inventory_data():
    """
    Generate mock inventory data including
    stock levels, reorder thresholds, and
    warehouse information.
    """

    inventory = []

    for product in PRODUCTS:

        reorder_level = random.randint(20, 100)

        stock_available = random.randint(
            0,
            150
        )

        inventory.append(
            {
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "stock_available": stock_available,
                "reorder_level": reorder_level,
                "last_restocked_date":
                    fake.date_between(
                        start_date="-180d",
                        end_date="today"
                    ),
                "warehouse_location":
                    random.choice(
                        ["Mumbai",
                         "Delhi",
                         "Pune",
                         "Chennai"]
                    )
            }
        )

    df = pd.DataFrame(inventory)

    return df


def generate_returns_data(sales_df):
    """
    Generate mock returns data linked to
    existing sales orders with return reasons
    and refund amounts.
    """

    reasons = [
        "Damaged Product",
        "Wrong Size",
        "Customer Changed Mind",
        "Late Delivery",
        "Wrong Item"
    ]

    returns = []

    sample_orders = sales_df.sample(
        120
    )

    for i, row in enumerate(
        sample_orders.itertuples()
    ):

        returns.append(
            {
                "return_id": f"RET{i+1:04}",
                "order_id": row.order_id,
                "product_id": row.product_id,
                "return_date":
                    fake.date_between(
                        start_date="-60d",
                        end_date="today"
                    ),
                "return_reason":
                    random.choice(reasons),
                "refund_amount":
                    round(
                        row.unit_price *
                        row.quantity_sold,
                        2
                    )
            }
        )

    return pd.DataFrame(returns)


def save_files(input_dir: str = "input"):
    """
    Generate all mock datasets and save them
    as CSV files in the specified input
    directory.
    """
    os.makedirs(
        input_dir,
        exist_ok=True
    )

    sales_df = generate_sales_data()

    sales_df = add_dirty_data(
        sales_df
    )

    inventory_df = generate_inventory_data()

    returns_df = generate_returns_data(
        sales_df
    )

    sales_df.to_csv(
        os.path.join(
        input_dir,
        "sales_data.csv",
        ),
        index=False
    )

    inventory_df.to_csv(
        os.path.join(
        input_dir,
        "inventory_data.csv",
        ),
        index=False
    )

    returns_df.to_csv(
        os.path.join(
        input_dir,
        "returns_data.csv",
        ),
        index=False
    )

    print("CSV files generated.")


#if __name__ == "__main__":
    #save_files()
