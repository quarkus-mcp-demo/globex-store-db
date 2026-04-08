#!/usr/bin/env python3
"""
Generate orders ensuring every product appears in approximately 100 orders.
Each customer (excluding asilva) gets multiple orders with 1-4 line items.
Shipping addresses use the customer's actual address.
"""
import random
import re
from datetime import datetime, timedelta
from collections import defaultdict

# File paths
INITIALIZE_SQL = '/home/bernard/projects_internal/cloud-architecture-workshop/globex/globex-store-db/contrib/sql/initialize.sql'

# Configuration
TARGET_ORDERS_PER_PRODUCT = 100
MIN_LINE_ITEMS = 1
MAX_LINE_ITEMS = 4
MIN_QUANTITY = 1
MAX_QUANTITY = 3
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 4, 1)
DATE_RANGE = (END_DATE - START_DATE).total_seconds()

def random_timestamp():
    """Generate a random timestamp between START_DATE and END_DATE"""
    random_seconds = random.random() * DATE_RANGE
    timestamp = START_DATE + timedelta(seconds=random_seconds)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def extract_products():
    """Extract all products from catalog"""
    products = []
    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    pattern = r"INSERT INTO catalog \(item_id, name, description, category, price\) VALUES \('([^']+)'.*?(\d+\.\d+)\);"
    for match in re.finditer(pattern, content):
        item_id, price = match.groups()
        products.append((item_id, float(price)))

    return products

def extract_customers():
    """Extract all customers excluding asilva"""
    customers = {}
    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    pattern = r"INSERT INTO public\.customer \(id, user_id, first_name, last_name, email, phone\) VALUES \(\d+, '([^']+)', '([^']+)', '([^']+)', '[^']+', '([^']+)'\);"
    for match in re.finditer(pattern, content):
        user_id, first_name, last_name, phone = match.groups()
        if user_id != 'asilva':
            customers[user_id] = {
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone
            }

    return customers

def extract_customer_addresses():
    """Extract one shipping address per customer from existing orders"""
    customer_addresses = {}
    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    # First, map order_id to customer_id
    order_to_customer = {}
    order_pattern = r"INSERT INTO public\.orders \(id, customer_id, order_ts\) VALUES \((\d+), '([^']+)', '[^']+'\);"
    for match in re.finditer(order_pattern, content):
        order_id, customer_id = match.groups()
        if customer_id != 'asilva':
            order_to_customer[order_id] = customer_id

    # Then, extract shipping addresses
    shipping_pattern = r"INSERT INTO public\.shipping_address \(id, address1, address2, city, country, name, phone, state, zip, order_id\) VALUES \(\d+, '([^']+)', '([^']*)', '([^']+)', '([^']+)', '[^']+', '[^']+', '([^']+)', '([^']+)', (\d+)\);"
    for match in re.finditer(shipping_pattern, content):
        address1, address2, city, country, state, zip_code, order_id = match.groups()

        if order_id in order_to_customer:
            customer_id = order_to_customer[order_id]
            # Only store first address found for each customer
            if customer_id not in customer_addresses:
                customer_addresses[customer_id] = {
                    'address1': address1,
                    'address2': address2,
                    'city': city,
                    'country': country,
                    'state': state,
                    'zip': zip_code
                }

    return customer_addresses

def generate_customer_address(customer_id, customer_data):
    """Generate a random address for a customer if not found in existing data"""
    streets = [
        '10 Aspen Lane', '15 Grove Street', '21 Peachtree Place', '28 Redwood Avenue',
        '32 Aspen Lane', '37 Cedar Court', '43 Elmwood Terrace', '51 Elm Avenue',
        '57 Willow Lane', '65 Oakwood Place', '72 Dogwood Drive', '78 Magnolia Court',
    ]

    city_state_zip = [
        ('Tooele', 'UT', '84074'), ('Belk', 'AL', '35545'), ('Fontana', 'KS', '66026'),
        ('Burlington', 'CO', '80807'), ('Cedar', 'MI', '49621'), ('Riley', 'IN', '47871'),
        ('Monroe Center', 'IL', '61052'), ('Berlin', 'OH', '44654'), ('Genola', 'UT', '84655'),
        ('Albertson', 'NY', '11507'), ('Lansing', 'IL', '60438'), ('Merrimac', 'WI', '53561'),
    ]

    # Use hash of customer_id to ensure consistency
    random.seed(hash(customer_id))
    street = random.choice(streets)
    city, state, zip_code = random.choice(city_state_zip)
    random.seed()  # Reset seed

    return {
        'address1': street,
        'address2': '',
        'city': city,
        'country': 'USA',
        'state': state,
        'zip': zip_code
    }

def find_start_ids():
    """Find the next available IDs for orders, line_items, and shipping_addresses"""
    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    # Find max order ID
    order_ids = []
    for match in re.finditer(r"INSERT INTO public\.orders \(id, customer_id, order_ts\) VALUES \((\d+),", content):
        order_ids.append(int(match.group(1)))
    next_order_id = max(order_ids) + 1 if order_ids else 1

    # Find max line_item ID
    line_item_ids = []
    for match in re.finditer(r"INSERT INTO public\.line_item \(id, price, product_code, quantity, order_id\) VALUES \((\d+),", content):
        line_item_ids.append(int(match.group(1)))
    next_line_item_id = max(line_item_ids) + 1 if line_item_ids else 1

    # Find max shipping_address ID
    shipping_ids = []
    for match in re.finditer(r"INSERT INTO public\.shipping_address \(id,", content):
        # Extract ID from the full pattern
        full_match = re.search(r"INSERT INTO public\.shipping_address \(id, [^)]+\) VALUES \((\d+),", content[match.start():match.start()+200])
        if full_match:
            shipping_ids.append(int(full_match.group(1)))
    next_shipping_id = max(shipping_ids) + 1 if shipping_ids else 1

    return next_order_id, next_line_item_id, next_shipping_id

def generate_orders(products, customers, customer_addresses):
    """Generate orders ensuring each product appears in ~TARGET_ORDERS_PER_PRODUCT orders"""

    # Calculate how many orders we need
    # Average line items per order
    avg_line_items = (MIN_LINE_ITEMS + MAX_LINE_ITEMS) / 2
    # Total product placements needed
    total_placements = len(products) * TARGET_ORDERS_PER_PRODUCT
    # Number of orders needed
    num_orders = int(total_placements / avg_line_items)

    print(f"# Generating {num_orders} orders for {len(products)} products", file=sys.stderr)
    print(f"# Each product will appear in approximately {TARGET_ORDERS_PER_PRODUCT} orders", file=sys.stderr)

    # Track product usage to ensure even distribution
    product_usage = defaultdict(int)

    # Get starting IDs
    start_order_id, start_line_item_id, start_shipping_id = find_start_ids()

    order_id = start_order_id
    line_item_id = start_line_item_id
    shipping_id = start_shipping_id

    orders_sql = []
    line_items_sql = []
    shipping_sql = []

    customer_list = list(customers.keys())

    for i in range(num_orders):
        # Select random customer
        customer_id = random.choice(customer_list)
        customer = customers[customer_id]

        # Generate random timestamp
        order_ts = random_timestamp()

        # Create order
        orders_sql.append(
            f"INSERT INTO public.orders (id, customer_id, order_ts) VALUES ({order_id}, '{customer_id}', '{order_ts}');"
        )

        # Generate shipping address
        full_name = f"{customer['first_name']} {customer['last_name']}"
        phone = customer['phone']

        # Get or generate address for customer
        if customer_id in customer_addresses:
            address = customer_addresses[customer_id]
        else:
            address = generate_customer_address(customer_id, customer)
            customer_addresses[customer_id] = address  # Cache it

        shipping_sql.append(
            f"INSERT INTO public.shipping_address (id, address1, address2, city, country, name, phone, state, zip, order_id) "
            f"VALUES ({shipping_id}, '{address['address1']}', '{address['address2']}', '{address['city']}', "
            f"'{address['country']}', '{full_name}', '{phone}', '{address['state']}', '{address['zip']}', {order_id});"
        )
        shipping_id += 1

        # Determine number of line items
        num_line_items = random.randint(MIN_LINE_ITEMS, MAX_LINE_ITEMS)

        # Select products for this order, preferring products with lower usage
        # This ensures even distribution
        sorted_products = sorted(products, key=lambda p: product_usage[p[0]])
        selected_products = random.sample(sorted_products[:len(products)//2], min(num_line_items, len(products)))

        for product_code, price in selected_products:
            quantity = random.randint(MIN_QUANTITY, MAX_QUANTITY)
            line_items_sql.append(
                f"INSERT INTO public.line_item (id, price, product_code, quantity, order_id) "
                f"VALUES ({line_item_id}, {price:.2f}, '{product_code}', {quantity}, {order_id});"
            )
            line_item_id += 1
            product_usage[product_code] += 1

        order_id += 1

    return orders_sql, line_items_sql, shipping_sql, product_usage

def main():
    import sys

    print("-- Generated orders for all products", file=sys.stderr)
    print("-- Extracting data from initialize.sql...", file=sys.stderr)

    # Extract data
    products = extract_products()
    customers = extract_customers()
    customer_addresses = extract_customer_addresses()

    print(f"-- Found {len(products)} products", file=sys.stderr)
    print(f"-- Found {len(customers)} customers (excluding asilva)", file=sys.stderr)
    print(f"-- Found {len(customer_addresses)} existing customer addresses", file=sys.stderr)

    # Set random seed for reproducibility
    random.seed(42)

    # Generate orders
    orders_sql, line_items_sql, shipping_sql, product_usage = generate_orders(
        products, customers, customer_addresses
    )

    # Print statistics
    print(f"-- Generated {len(orders_sql)} orders", file=sys.stderr)
    print(f"-- Generated {len(line_items_sql)} line items", file=sys.stderr)
    print(f"-- Generated {len(shipping_sql)} shipping addresses", file=sys.stderr)
    print(f"-- Product usage stats:", file=sys.stderr)
    print(f"--   Min: {min(product_usage.values())}", file=sys.stderr)
    print(f"--   Max: {max(product_usage.values())}", file=sys.stderr)
    print(f"--   Avg: {sum(product_usage.values()) / len(product_usage):.1f}", file=sys.stderr)

    # Output SQL
    print()
    print("-- Orders for all products (each product in ~100 orders)")
    for sql in orders_sql:
        print(sql)

    print()
    print("-- Line items for the orders")
    for sql in line_items_sql:
        print(sql)

    print()
    print("-- Shipping addresses for the orders")
    for sql in shipping_sql:
        print(sql)

if __name__ == '__main__':
    import sys
    main()
