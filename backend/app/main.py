from fastapi import FastAPI, Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime
from typing import List

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.database.database import get_db
from app.services.data_service import DataService
from app.crud import crud_operations
from app.models.schemas import ProductCreate, ProductResponse, CustomerCreate, CustomerResponse, OrderCreate, OrderResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Analytics Dashboard API",
    description="Backend API for Analytics Dashboard",
    version="1.0.0"
)

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(router, prefix="/api", tags=["analytics"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# Analytics endpoints
@app.get("/api/analytics/dashboard")
def get_dashboard_analytics(db: Session = Depends(get_db)):
    return DataService(db).get_all_analytics()

@app.get("/api/analytics/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return DataService(db).get_dashboard_stats()

@app.get("/api/analytics/sales-chart")
def get_sales_chart(days: int = 30, db: Session = Depends(get_db)):
    return DataService(db).get_sales_chart_data(days)

@app.get("/api/analytics/category-chart")
def get_category_chart(db: Session = Depends(get_db)):
    return DataService(db).get_category_chart_data()

@app.get("/api/analytics/recent-orders")
def get_recent_orders(limit: int = 10, db: Session = Depends(get_db)):
    return DataService(db).get_recent_orders(limit)

@app.get("/api/analytics/top-products")
def get_top_products(limit: int = 5, db: Session = Depends(get_db)):
    return DataService(db).get_top_products_data(limit)

@app.get("/api/analytics/orders-by-status")
def get_orders_by_status(db: Session = Depends(get_db)):
    return DataService(db).get_orders_by_status_data()

# NEW: Product endpoints
@app.get("/api/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud_operations.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/api/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_operations.create_product(db, product)

@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    return crud_operations.update_product(db, product_id, product)

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud_operations.delete_product(db, product_id)
    return {"message": "Product deleted successfully"}

# NEW: Customer endpoints
@app.get("/api/customers", response_model=List[CustomerResponse])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud_operations.get_customers(db, skip=skip, limit=limit)
    return customers

@app.post("/api/customers", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud_operations.create_customer(db, customer)

@app.put("/api/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud_operations.update_customer(db, customer_id, customer)

@app.delete("/api/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    crud_operations.delete_customer(db, customer_id)
    return {"message": "Customer deleted successfully"}

# NEW: Order endpoints
@app.get("/api/orders", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud_operations.get_orders(db, skip=skip, limit=limit)
    return orders

@app.post("/api/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud_operations.create_order(db, order)

@app.put("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    return crud_operations.update_order_status(db, order_id, status)

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    crud_operations.delete_order(db, order_id)
    return {"message": "Order deleted successfully"}


@app.get("/api/orders/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific order"""
    order = crud_operations.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/refresh-data")
def refresh_data():
    return {
        "status": "success",
        "message": "Data refreshed successfully",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    return {
        "message": "Analytics Dashboard API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
