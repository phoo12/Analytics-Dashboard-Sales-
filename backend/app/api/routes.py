from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import AnalyticsResponse, DashboardStats, ChartData
from app.services.data_service import data_service
from app.services.data_service import data_service
from app.auth.auth import get_current_active_user
from app.database.analytics_models import User

router = APIRouter()

@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(current_user: User = Depends(get_current_active_user)):
    """
    Get all analytics data for the dashboard
    """
    try:
        data = data_service.get_all_analytics()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=DashboardStats)
async def get_stats():
    """
    Get dashboard statistics only
    """
    try:
        stats = data_service.get_dashboard_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sales-chart", response_model=ChartData)
async def get_sales_chart():
    """
    Get sales chart data
    """
    try:
        chart_data = data_service.get_sales_chart_data()
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category-chart", response_model=ChartData)
async def get_category_chart():
    """
    Get category breakdown chart data
    """
    try:
        chart_data = data_service.get_category_chart_data()
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-sales")
async def get_recent_sales(limit: int = 10):
    """
    Get recent sales data
    """
    try:
        sales = data_service.get_recent_sales(limit)
        return {"sales": sales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh-data")
async def refresh_data():
    """
    Refresh/regenerate sample data
    """
    try:
        data_service.data = data_service.generate_sample_data()
        return {"message": "Data refreshed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))