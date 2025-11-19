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
        
        # Clear existing data
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(Customer).delete()
        db.commit()
        
        # Add sample products
        products = [
            Product(name="MacBook Pro", category="Electronics", price=1000, stock=50, description="16-inch MacBook Pro"),
            Product(name="iPhone 15", category="Electronics", price=800, stock=100, description="Latest iPhone model"),
            Product(name="Office Chair", category="Furniture", price=299.99, stock=30, description="Ergonomic office chair"),
            Product(name="Desk Lamp", category="Home", price=49.99, stock=80, description="LED desk lamp"),
            Product(name="Desk Lamp", category="Home", price=50, stock=90, description="LED desk lamp"),
            Product(name="book", category="Stationery", price=12.99, stock=200, description="book"),
            Product(name="Notebook", category="Stationery", price=12.99, stock=200, description="Premium notebook"),
            Product(name="pen", category="Stationery", price=12.99, stock=200, description="pen"),
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        # Add sample customers
        customers = [
            Customer(name="John Smith", email="john.smith@email.com", phone="123-456-7890", city="New York"),
            Customer(name="Sarah Johnson", email="sarah.j@email.com", phone="123-456-7891", city="Los Angeles"),
            Customer(name="Mike Brown", email="mike.brown@email.com", phone="123-456-7892", city="Chicago"),
            Customer(name=" Brown", email="mike.brown@email.com", phone="123-456-7892", city="Chicago"),
            Customer(name="Mike ", email="mike.brown@email.com", phone="123-456-7892", city="Chicago"),
        ]
        
        for customer in customers:
            db.add(customer)
        db.commit()
        
        # Add sample orders with realistic dates
        for i in range(50):
            order_date = datetime.now() - timedelta(days=random.randint(0, 30))
            customer = random.choice(customers)
            product = random.choice(products)
            quantity = random.randint(1, 3)
            subtotal = product.price * quantity
            
            order = Order(
                order_number=f"ORD{1000 + i}",
                customer_id=customer.id,
                status=random.choice(["pending", "processing", "completed", "completed", "completed"]),
                total_amount=subtotal,
                payment_method=random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
                created_at=order_date
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            
            # Add order items
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                subtotal=subtotal
            )
            db.add(order_item)
            db.commit()
        
        print("Sample data added successfully!")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_sample_data()