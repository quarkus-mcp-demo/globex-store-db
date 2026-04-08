# Complaint Generation Scripts

This directory contains Python scripts to generate SQL INSERT statements for customer complaints with realistic defects based on product categories.

## Scripts

### generate_rhnl017_complaints.py
Generates 40-50 complaints specifically for product RHNL-017 (Quarkus sweatshirt).

**Features:**
- 40-50 complaints for a single product
- Complaints linked to existing orders containing RHNL-017
- Realistic sweatshirt-specific defect descriptions
- Evenly distributed severity levels (critical, high, medium, low)
- Issue types mostly "defect" with some "quality"
- Timestamps after order date but before 2026-04-01

**Usage:**
```bash
python3 scripts/complaints/generate_rhnl017_complaints.py > /tmp/rhnl017_complaints.sql
```

### generate_all_product_complaints.py
Generates 40-50 complaints per product for all products in the catalog with category-specific realistic defect descriptions.

**Features:**
- Generates ~1,800-2,000 complaints across all products
- 40-50 complaints per product (randomized)
- Category-aware complaint templates:
  - **Clothing** (t-shirts, sweatshirts, polos, socks): fabric issues, shrinkage, color bleeding, allergic reactions
  - **Utensils** (bottles, mugs, tumblers): leaks, thermal failures, coating issues, breakage
  - **Bags** (backpacks, duffle bags, cooler bags): strap failures, zipper issues, material tears
  - **Office supplies** (pens, journals, webcam covers): ink leaks, adhesive failures, binding problems
  - **Fashion accessory** (pins, earrings, keychains, masks): clasp failures, skin reactions, elastic breaks
  - **Electronics** (webcam lights, headphones): electrical hazards, battery failures, connectivity issues
  - **Drum sticks**: splintering, breaking during play, finish issues, balance problems
  - **Drum shell sets**: shell cracking, hardware failures, bearing edge issues, finish defects
  - **Default**: generic quality and safety issues for uncategorized products
- 15 unique complaint templates per severity level per category (60 per category, 540+ total templates)
- All complaints have detailed 2+ sentence descriptions with unique wording
- Complaints linked to existing orders for each product
- No duplicate complaints (one complaint per product per order maximum)
- Evenly distributed severity levels across all products
- Issue types: ~80% defect, ~20% quality
- Resolution options: refund or replacement
- Status: mostly "open" with some "in_progress"
- Timestamps: after order date but before 2026-04-01
- Auto-detection of next available complaint ID

**Usage:**
```bash
# Generate SQL and view statistics
python3 scripts/complaints/generate_all_product_complaints.py

# Generate SQL only (suppress statistics)
python3 scripts/complaints/generate_all_product_complaints.py 2>/dev/null

# Append to initialize.sql
python3 scripts/complaints/generate_all_product_complaints.py 2>/dev/null >> contrib/sql/initialize.sql
```

**Statistics Output (stderr):**
```
-- Generated complaints for all products
-- Extracting products from catalog...
-- Found 48 products
-- Extracting orders by product...
-- Found orders for 48 products
-- Generating 40-50 complaints per product...
-- Generated 1832 total complaints
-- Products processed: 41
-- Products skipped (no orders): 0
-- Severity distribution:
--   critical: 455
--   high: 461
--   medium: 458
--   low: 458
-- Issue type distribution:
--   defect: 1480
--   quality: 352
```

## Complaint Template Categories

### Clothing (T-shirts, Sweatshirts, Polos, Socks)
- **Critical**: Chemical burns, severe allergic reactions, fabric disintegration, toxic odors
- **High**: Extreme shrinkage, color bleeding, seam failures, excessive pilling
- **Medium**: Logo misalignment, inconsistent sizing, minor pilling, color variations
- **Low**: Itchy tags, slight color differences, minor loose threads

### Utensils (Bottles, Mugs, Tumblers)
- **Critical**: Catastrophic leaks, lid failures causing burns, shattering, metal contamination
- **High**: Persistent leaking, coating peeling into beverages, insulation failure, handle breakage
- **Medium**: Difficult to clean, logo wearing off, stiff mechanisms, metallic taste
- **Low**: Minor capacity differences, color variations, small scratches

### Bags (Backpacks, Duffle Bags, Cooler Bags)
- **Critical**: Strap detachment under load, complete zipper failure, material tears, bottom collapse
- **High**: Zipper separation, strap stitching failure, water resistance failure, material fraying
- **Medium**: Poor pocket design, sticky zippers, fabric wear, logo peeling
- **Low**: Color differences, loose threads, smaller capacity, less padding

### Office Supplies (Pens, Journals, Webcam Covers)
- **Critical**: Adhesive damaging screens, ink explosions, sharp edges, toxic fumes
- **High**: Pens stopping after minimal use, adhesive failure, binding collapse, mechanism breakage
- **Medium**: Poor ink quality, thin pages with bleed-through, cheap feel, inconsistent function
- **Low**: Color variations, size differences, minor cosmetic defects

### Fashion Accessory (Pins, Earrings, Keychains, Masks)
- **Critical**: Pin stab injuries, severe allergic reactions, sharp broken edges, elastic snap injuries
- **High**: Clasp breakage, dramatic color fading, immediate tarnishing, elastic failure
- **Medium**: Design wearing off, incorrect sizing, low build quality, uneven finish
- **Low**: Slight color differences, minor imperfections, lighter weight

### Electronics (Webcam Lights, Headphones)
- **Critical**: Fire hazards, electrical shocks, battery explosions, devices dead on arrival
- **High**: Complete failure after minimal use, terrible sound quality, false battery claims, port breakage
- **Medium**: Dimmer than advertised, sticky buttons, cheap feel, compatibility issues
- **Low**: Color temperature differences, slightly bulkier, minor cosmetic defects

### Drum Sticks
- **Critical**: Splintering causing eye injuries, sticks breaking and hitting face, chemical burns from treatment, sharp edges causing cuts
- **High**: Breaking after minimal use, tips breaking off, severe warping, finish peeling causing blisters
- **Medium**: Uneven weight in matched pairs, inconsistent tips, finish wearing quickly, poor wood grain
- **Low**: Minor weight differences, cosmetic finish imperfections, slight balance variations

### Drum Shell Sets
- **Critical**: Lugs ripping out of shells, mounting hardware catastrophic failures, shell cracking/delamination, sharp edges causing injury
- **High**: Tension rods stripping, severe shell warping, finish peeling, bearing edges tearing drum heads, hardware rusting
- **Medium**: Inconsistent bearing edges, finish imperfections, loose lugs, rough internal finish, uneven drum depths
- **Low**: Minor finish color variations, small cosmetic defects, slightly crooked badges, minor alignment issues

## Data Extraction

Both scripts automatically extract required data from `contrib/sql/initialize.sql`:
- Products from `catalog` table with category information
- Orders and line_items to find which orders contain which products
- Order timestamps for complaint date generation
- Customer IDs for linking complaints to users
- Next available complaint ID

## Database Schema

Complaints are inserted with the following structure:
```sql
INSERT INTO public.complaints (
    id,              -- Auto-incremented from last ID + 1
    user_id,         -- Customer who placed the order
    order_id,        -- Order containing the product
    product_code,    -- Product being complained about
    issue_type,      -- 'defect' or 'quality'
    severity,        -- 'critical', 'high', 'medium', or 'low'
    complaint,       -- Detailed description (2+ sentences)
    status,          -- 'open' or 'in_progress'
    resolution,      -- 'refund' or 'replacement'
    created_at,      -- Timestamp after order_ts, before 2026-04-01
    updated_at,      -- Same as created_at initially
    version          -- Always 1 for new complaints
) VALUES (...);
```

## Timestamp Logic

Complaint timestamps are generated to ensure data integrity:
1. Always **after** the associated order timestamp
2. Always **before** 2026-04-01 (MAX_DATE)
3. Typically 1-60 days after order date
4. For orders close to MAX_DATE, complaints are scheduled proportionally

## Duplicate Prevention

The `generate_all_product_complaints.py` script ensures:
- No more than one complaint per product per order
- Tracks used (product_code, order_id) combinations
- Skips products with insufficient orders
- Warns when products have fewer orders than desired complaints

## Quality Distribution

Complaints are carefully balanced:
- **Severity**: 25% each of critical, high, medium, low
- **Issue Type**: 80% defect, 20% quality (4:1 ratio)
- **Status**: 75% open, 25% in_progress (3:1 ratio)
- **Resolution**: 50% refund, 50% replacement

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
- Access to `contrib/sql/initialize.sql` file
- Existing orders in the database for products to complain about

## Template Variety

To minimize repetition across ~1,800 complaints:
- 9 product categories with unique templates (clothing, utensils, bags, office supplies, fashion accessory, electronics, drum sticks, drum shell sets, default)
- 15 templates per severity level per category (12 for 'low' severity in drum categories)
- 57-60 total templates per category
- 540+ unique complaint templates across all categories
- All descriptions are 2+ sentences with detailed context
- Varied wording ensures minimal duplication
