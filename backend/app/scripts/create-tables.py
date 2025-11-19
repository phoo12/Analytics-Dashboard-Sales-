"""
Script to create new database tables
This will create only the new tables (customers, products, orders, order_items)
without affecting your existing users table
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import engine, Base
from app.database.models import User, Customer, Product, Order, OrderItem

def create_tables():
    """Create all database tables"""
    print("\n Creating database tables...")
    
    try:
        # This will create only tables that don't exist yet
        Base.metadata.create_all(bind=engine)
        
        print(" Database tables created successfully!")
        print("\n Tables:")
        print("   - users (existing)")
        print("   - customers (new)")
        print("   - products (new)")
        print("   - orders (new)")
        print("   - order_items (new)")
        
        print("\n✓ Your existing user data is safe!")
        
    except Exception as e:
        print(f"\n Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()