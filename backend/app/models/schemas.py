from pydantic import BaseModel, EmailStr
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


# NEW: Product Schemas (define these FIRST)
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int = 0
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# NEW: Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# NEW: Order Item Schemas (define these AFTER ProductResponse)
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    subtotal: float
    product: ProductResponse  # Now ProductResponse is defined above
    
    class Config:
        from_attributes = True

# NEW: Order Schemas
class OrderBase(BaseModel):
    customer_id: int
    status: str = "pending"
    payment_method: Optional[str] = None
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    order_number: str
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    customer: CustomerResponse
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

# NEW: Simple response models for lists
class ProductList(BaseModel):
    products: List[ProductResponse]

class CustomerList(BaseModel):
    customers: List[CustomerResponse]

class OrderList(BaseModel):
    orders: List[OrderResponse]