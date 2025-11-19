from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class SalesData(BaseModel):
    date: str
    revenue: float
    orders: int 
    customers: int

class MetricCard(BaseModel):
    title: str 
    value: str
    change: float
    trend: str

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Any]

class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    average_order_value: float
    revenue_growth: float
    orders_growth: float
    customers_growth: float

class AnalyticsResponse(BaseModel):
    stats: DashboardStats
    sales_chart: ChartData
    category_chart: ChartData
    recent_sales: List[SalesData]
