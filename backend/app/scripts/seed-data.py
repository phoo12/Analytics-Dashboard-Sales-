import sys
import os
from datetime import datetime, timedelta
import random

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from database.analytics_models import Customer, Product, Order, OrderItem

def seed_sample_data():
    db = SessionLocal()
    
    try:
        print("Starting to seed sample data...")
        
        # Clear existing data in correct order (due to foreign keys)
        print("Clearing existing data...")
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(Customer).delete()
        db.commit()
        print("Existing data cleared.")
        
        # Add sample products
        print("Adding products...")
        products = [
            Product(name="MacBook Pro", category="Electronics", price=1999.99, description="16-inch MacBook Pro"),
            Product(name="iPhone 15", category="Electronics", price=999.99, description="Latest iPhone model"),
            Product(name="iPad Air", category="Electronics", price=599.99, description="iPad Air tablet"),
            Product(name="Office Chair", category="Furniture", price=299.99, description="Ergonomic office chair"),
            Product(name="Standing Desk", category="Furniture", price=499.99, description="Adjustable standing desk"),
            Product(name="Desk Lamp", category="Home", price=49.99, description="LED desk lamp"),
            Product(name="Notebook", category="Stationery", price=12.99, description="Premium notebook"),
            Product(name="Pen Set", category="Stationery", price=24.99, description="Professional pen set"),
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        print(f"Added {len(products)} products.")
        
        # Add sample customers (without city field)
        print("Adding customers...")
        customers = [
            Customer(name="Aiko", email="Aiko@email.com", phone="123-456-7890", address="123 Main St"),
            Customer(name="Puku", email="Puku@email.com", phone="123-456-7891", address="456 Oak Ave"),
            Customer(name="Wai", email="Wai@email.com", phone="123-456-7892", address="789 Pine Rd"),
            Customer(name="Kitty", email="Kitty.d@email.com", phone="123-456-7893", address="321 Elm St"),
            Customer(name="Cat", email="Cat@email.com", phone="123-456-7894", address="654 Maple Dr"),
        ]
        
        for customer in customers:
            db.add(customer)
        db.commit()
        print(f"Added {len(customers)} customers.")
        
        # Refresh to get IDs
        db.refresh(products[0])
        db.refresh(customers[0])
        
        # Add sample orders with realistic dates
        print("Adding orders...")
        for i in range(50):
            order_date = datetime.now() - timedelta(days=random.randint(0, 30))
            customer = random.choice(customers)
            
            # Create order first
            order = Order(
                order_number=f"ORD{1000 + i}",
                customer_id=customer.id,
                status=random.choice(["pending", "processing", "completed", "completed", "completed"]),
                total_amount=0,  # Will calculate from items
                payment_method=random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
                created_at=order_date
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            
            # Add 1-3 order items
            total = 0
            num_items = random.randint(1, 3)
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                subtotal = product.price * quantity
                total += subtotal
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                    subtotal=subtotal
                )
                db.add(order_item)
            
            # Update order total
            order.total_amount = total
            db.commit()
        
        print(f"Added 50 orders with items.")
        print("Sample data seeded successfully!")
        
        # Verify data
        order_count = db.query(Order).count()
        customer_count = db.query(Customer).count()
        product_count = db.query(Product).count()
        print(f"\nVerification:")
        print(f"  - Products: {product_count}")
        print(f"  - Customers: {customer_count}")
        print(f"  - Orders: {order_count}")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_sample_data()