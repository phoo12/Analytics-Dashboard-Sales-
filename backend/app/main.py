from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.database.database import get_db
from app.services.data_service import DataService

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
    "http://localhost:3003",
    "http://127.0.0.1:3003",
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
