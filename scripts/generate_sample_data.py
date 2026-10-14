import csv
import random
from datetime import datetime, timedelta

def generate_ecommerce_data(filename="data/sample_ecommerce_sales.csv", num_rows=500):
    categories = {
        "Electronics": ["Smartphone Pro", "Noise-Cancelling Headphones", "4K Ultra Monitor", "Mechanical Keyboard"],
        "Home & Kitchen": ["Air Fryer XL", "Espresso Machine", "Robot Vacuum", "Ergonomic Desk Chair"],
        "Fitness & Outdoors": ["Smart Fitness Watch", "Adjustable Dumbbells", "Yoga Mat Pro", "Hydration Backpack"],
        "Office Supplies": ["Standing Desk Converter", "Dual-Arm Monitor Mount", "Wireless Trackball", "LED Desk Lamp"]
    }
    
    regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
    channels = ["Direct Web", "Organic Search", "Partner Referral", "Social Campaign"]
    
    start_date = datetime(2025, 1, 1)
    
    rows = []
    random.seed(42)
    
    for order_id in range(1001, 1001 + num_rows):
        cat = random.choice(list(categories.keys()))
        prod = random.choice(categories[cat])
        region = random.choice(regions)
        channel = random.choice(channels)
        
        # Realistic pricing & quantities
        if cat == "Electronics":
            unit_price = round(random.uniform(120, 899), 2)
            quantity = random.choices([1, 2, 3, 5], weights=[0.6, 0.25, 0.1, 0.05])[0]
            discount_pct = random.choices([0.0, 0.05, 0.10, 0.15], weights=[0.5, 0.2, 0.2, 0.1])[0]
        elif cat == "Home & Kitchen":
            unit_price = round(random.uniform(45, 350), 2)
            quantity = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
            discount_pct = random.choices([0.0, 0.10, 0.20], weights=[0.6, 0.25, 0.15])[0]
        elif cat == "Fitness & Outdoors":
            unit_price = round(random.uniform(30, 220), 2)
            quantity = random.choices([1, 2, 4], weights=[0.65, 0.25, 0.1])[0]
            discount_pct = random.choices([0.0, 0.05, 0.15], weights=[0.7, 0.2, 0.1])[0]
        else:
            unit_price = round(random.uniform(25, 180), 2)
            quantity = random.choices([1, 2, 5, 10], weights=[0.5, 0.3, 0.15, 0.05])[0]
            discount_pct = random.choices([0.0, 0.05, 0.10, 0.25], weights=[0.5, 0.25, 0.15, 0.1])[0]
            
        gross_sales = round(unit_price * quantity, 2)
        discount_amount = round(gross_sales * discount_pct, 2)
        net_revenue = round(gross_sales - discount_amount, 2)
        cost = round(gross_sales * random.uniform(0.40, 0.65), 2)
        profit = round(net_revenue - cost, 2)
        customer_rating = round(random.choices([5.0, 4.0, 3.0, 2.0, 1.0], weights=[0.55, 0.25, 0.12, 0.05, 0.03])[0], 1)
        
        date_offset = random.randint(0, 180)
        order_date = (start_date + timedelta(days=date_offset)).strftime("%Y-%m-%d")
        
        rows.append({
            "order_id": order_id,
            "order_date": order_date,
            "region": region,
            "acquisition_channel": channel,
            "product_category": cat,
            "product_name": prod,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount_pct": discount_pct,
            "net_revenue": net_revenue,
            "profit": profit,
            "customer_rating": customer_rating
        })
        
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} records in {filename}")

if __name__ == "__main__":
    generate_ecommerce_data()
