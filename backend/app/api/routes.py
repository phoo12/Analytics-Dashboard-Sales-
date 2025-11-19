from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.data_service import DataService
from app.models.schemas import AnalyticsResponse, DashboardStats, ChartData
from app.auth.auth import get_current_active_user
from app.database.analytics_models import User

router = APIRouter()

@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all analytics data for the dashboard
    """
    try:
        data_service = DataService(db)  # Create instance with db session
        data = data_service.get_all_analytics()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=DashboardStats)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics only
    """
    try:
        data_service = DataService(db)  # Create instance with db session
        stats = data_service.get_dashboard_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sales-chart", response_model=ChartData)
async def get_sales_chart(db: Session = Depends(get_db)):
    """
    Get sales chart data
    """
    try:
        data_service = DataService(db)  # Create instance with db session
        chart_data = data_service.get_sales_chart_data()
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category-chart", response_model=ChartData)
async def get_category_chart(db: Session = Depends(get_db)):
    """
    Get category breakdown chart data
    """
    try:
        data_service = DataService(db)  # Create instance with db session
        chart_data = data_service.get_category_chart_data()
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-sales")
async def get_recent_sales(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get recent sales data
    """
    try:
        data_service = DataService(db)  # Create instance with db session
        sales = data_service.get_recent_orders(limit)  # Fixed method name
        return {"sales": sales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh-data")
async def refresh_data(db: Session = Depends(get_db)):
    """
    Refresh/regenerate sample data
    """
    try:
        # This would typically reseed the database
        # For now, just return success
        return {"message": "Refresh endpoint - would reseed data here"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))