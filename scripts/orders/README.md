# Order Generation Scripts

This directory contains Python scripts to generate SQL INSERT statements for orders, line items, and shipping addresses.

## Scripts

### generate_orders.py
Generates 100 orders that all contain a specific product (329299 - Quarkus T-shirt).

**Features:**
- 100 orders with 1-4 line items each
- All orders contain product '329299'
- Orders distributed across customers (excluding asilva)
- Random timestamps between 2026-01-01 and 2026-04-01
- Shipping addresses with randomized street/city/state/zip

**Usage:**
```bash
python3 scripts/orders/generate_orders.py > /tmp/orders_329299.sql
```

### generate_all_product_orders.py
Generates orders ensuring every product in the catalog appears in approximately 100 orders.

**Features:**
- Generates ~1920 orders for 48 products
- Each product appears in 96-101 orders (evenly distributed)
- Orders for all customers except asilva
- Each order has 1-4 line items with quantity 1-3
- Shipping addresses reuse existing customer addresses from the database
- Timestamps between 2026-01-01 and 2026-04-01

**Usage:**
```bash
# Generate SQL and view statistics
python3 scripts/orders/generate_all_product_orders.py

# Generate SQL only (suppress statistics)
python3 scripts/orders/generate_all_product_orders.py 2>/dev/null

# Append to initialize.sql
python3 scripts/orders/generate_all_product_orders.py 2>/dev/null >> contrib/sql/initialize.sql
```

**Statistics Output (stderr):**
```
-- Generated orders for all products
-- Extracting data from initialize.sql...
-- Found 48 products
-- Found 199 customers (excluding asilva)
-- Found 104 existing customer addresses
# Generating 1920 orders for 48 products
# Each product will appear in approximately 100 orders
-- Generated 1920 orders
-- Generated 4805 line items
-- Generated 1920 shipping addresses
-- Product usage stats:
--   Min: 98
--   Max: 101
--   Avg: 100.1
```

## Data Extraction

Both scripts automatically extract required data from `contrib/sql/initialize.sql`:
- Products from the `catalog` table
- Customers from the `customer` table (excluding asilva)
- Existing shipping addresses for address reuse
- Next available IDs for orders, line_items, and shipping_address tables

## ID Management

Scripts automatically detect the highest existing IDs and continue from there:
- Orders: Continues from last order ID + 1
- Line items: Continues from last line_item ID + 1
- Shipping addresses: Continues from last shipping_address ID + 1

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
- Access to `contrib/sql/initialize.sql` file
