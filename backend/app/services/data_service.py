import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

# Update imports based on structure
from app.database.database import get_db
from app.database.analytics_models import Customer, Product, Order, OrderItem

class DataService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self):
        """Calculate overall dashboard statistics from real database"""
        try:
            # Total revenue
            total_revenue = self.db.query(func.sum(Order.total_amount)).scalar() or 0
            
            # Total orders
            total_orders = self.db.query(Order).count()
            
            # Total customers
            total_customers = self.db.query(Customer).count()
            
            # Total products
            total_products = self.db.query(Product).count()
            
            # Average order value
            average_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Calculate growth (last 7 days vs previous 7 days)
            end_date = datetime.now()
            start_date_7 = end_date - timedelta(days=7)
            start_date_14 = end_date - timedelta(days=14)
            
            # Last 7 days revenue
            last_7_days_revenue = self.db.query(func.sum(Order.total_amount)).filter(
                Order.created_at >= start_date_7
            ).scalar() or 0
            
            # Previous 7 days revenue
            prev_7_days_revenue = self.db.query(func.sum(Order.total_amount)).filter(
                Order.created_at >= start_date_14,
                Order.created_at < start_date_7
            ).scalar() or 0
            
            # Calculate growth percentages
            revenue_growth = ((last_7_days_revenue - prev_7_days_revenue) / prev_7_days_revenue * 100) if prev_7_days_revenue > 0 else 0
            
            return {
                'total_revenue': round(total_revenue, 2),
                'total_orders': int(total_orders),
                'total_customers': int(total_customers),
                'total_products': int(total_products),
                'average_order_value': round(average_order_value, 2),
                'revenue_growth': round(revenue_growth, 2),
                'orders_growth': 0,  # You can add similar calculations
                'customers_growth': 0   # You can add similar calculations
            }
        except Exception as e:
            print(f"Error in get_dashboard_stats: {e}")
            return {
                'total_revenue': 0,
                'total_orders': 0,
                'total_customers': 0,
                'total_products': 0,
                'average_order_value': 0,
                'revenue_growth': 0,
                'orders_growth': 0,
                'customers_growth': 0
            }
    
    def get_sales_chart_data(self, days=30):
        """Get real sales data for chart"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Query daily sales data
            daily_sales = self.db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total_amount).label('revenue'),
                func.count(Order.id).label('orders')
            ).filter(
                Order.created_at >= start_date
            ).group_by(
                func.date(Order.created_at)
            ).order_by('date').all()
            
            # Create a complete date range to fill missing dates
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            sales_data = []
            for single_date in date_range:
                date_str = single_date.strftime('%Y-%m-%d')
                # Find matching sales data for this date
                daily_sale = next((sale for sale in daily_sales if sale.date.strftime('%Y-%m-%d') == date_str), None)
                
                sales_data.append({
                    'date': date_str,
                    'revenue': float(daily_sale.revenue) if daily_sale else 0.0,
                    'orders': daily_sale.orders if daily_sale else 0
                })
            
            return {
                'labels': [item['date'] for item in sales_data],
                'datasets': [
                    {
                        'label': 'Revenue',
                        'data': [item['revenue'] for item in sales_data],
                        'borderColor': 'rgb(59, 130, 246)',
                        'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                        'tension': 0.4
                    }
                ]
            }
        except Exception as e:
            print(f"Error in get_sales_chart_data: {e}")
            return {'labels': [], 'datasets': []}
    
    def get_category_chart_data(self):
        """Get real sales data by category"""
        try:
            category_sales = self.db.query(
                Product.category,
                func.sum(OrderItem.subtotal).label('total_sales')
            ).join(OrderItem, Product.id == OrderItem.product_id
            ).group_by(Product.category).all()
            
            labels = [sale.category for sale in category_sales] if category_sales else ['No Data']
            data = [float(sale.total_sales) for sale in category_sales] if category_sales else [0]
            
            return {
                'labels': labels,
                'datasets': [
                    {
                        'label': 'Sales by Category',
                        'data': data,
                        'backgroundColor': [
                            'rgba(59, 130, 246, 0.8)',
                            'rgba(16, 185, 129, 0.8)',
                            'rgba(251, 191, 36, 0.8)',
                            'rgba(239, 68, 68, 0.8)',
                            'rgba(139, 92, 246, 0.8)'
                        ]
                    }
                ]
            }
        except Exception as e:
            print(f"Error in get_category_chart_data: {e}")
            return {'labels': ['Error'], 'datasets': [{'data': [0]}]}
    
    def get_top_products_data(self, limit=5):
        """Get top selling products"""
        try:
            top_products = self.db.query(
                Product.name,
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(OrderItem.subtotal).label('total_revenue')
            ).join(OrderItem, Product.id == OrderItem.product_id
            ).group_by(Product.id, Product.name
            ).order_by(desc('total_quantity')
            ).limit(limit).all()
            
            return {
                'labels': [product.name for product in top_products],
                'datasets': [
                    {
                        'label': 'Units Sold',
                        'data': [product.total_quantity for product in top_products],
                        'backgroundColor': 'rgba(59, 130, 246, 0.8)',
                    }
                ]
            }
        except Exception as e:
            print(f"Error in get_top_products_data: {e}")
            return {'labels': [], 'datasets': []}
    
    def get_orders_by_status_data(self):
        """Get orders count by status"""
        try:
            status_counts = self.db.query(
                Order.status,
                func.count(Order.id).label('count')
            ).group_by(Order.status).all()
            
            return {
                'labels': [status.status for status in status_counts],
                'datasets': [
                    {
                        'label': 'Orders by Status',
                        'data': [status.count for status in status_counts],
                        'backgroundColor': [
                            'rgba(251, 191, 36, 0.8)',  # pending - yellow
                            'rgba(59, 130, 246, 0.8)',  # processing - blue
                            'rgba(16, 185, 129, 0.8)',  # completed - green
                            'rgba(239, 68, 68, 0.8)',   # cancelled - red
                        ]
                    }
                ]
            }
        except Exception as e:
            print(f"Error in get_orders_by_status_data: {e}")
            return {'labels': [], 'datasets': []}
    
    def get_recent_orders(self, limit=10):
        """Get most recent orders with customer info"""
        try:
            recent_orders = self.db.query(Order).join(Customer).order_by(
                desc(Order.created_at)
            ).limit(limit).all()
            
            orders_data = []
            for order in recent_orders:
                orders_data.append({
                    'id': order.id,
                    'order_number': order.order_number,
                    'customer_name': order.customer.name,
                    'total_amount': float(order.total_amount),
                    'status': order.status,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
                    'items_count': len(order.order_items)
                })
            
            return orders_data
        except Exception as e:
            print(f"Error in get_recent_orders: {e}")
            return []
    
    def get_all_analytics(self):
        """Get all analytics data for dashboard from real database"""
        return {
            'stats': self.get_dashboard_stats(),
            'sales_chart': self.get_sales_chart_data(),
            'category_chart': self.get_category_chart_data(),  # Fixed: removed get_
            'top_products': self.get_top_products_data(),
            'orders_by_status': self.get_orders_by_status_data(),
            'recent_orders': self.get_recent_orders()
        }