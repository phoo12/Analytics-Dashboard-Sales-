import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataService:
    def __init__(self):
        self.data = self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate realistic sample sales data for the last 30 days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        data = []
        for date in dates:
            # Generate realistic sales data with some trends
            base_revenue = 10000 + random.uniform(-2000, 3000)
            day_of_week = date.weekday()
            
            # Weekend boost
            if day_of_week >= 5:
                base_revenue *= 1.3
            
            # Add some growth trend
            days_from_start = (date - start_date).days
            growth_factor = 1 + (days_from_start * 0.01)
            
            revenue = base_revenue * growth_factor
            orders = int(revenue / random.uniform(80, 120))
            customers = int(orders * random.uniform(0.7, 0.95))
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'revenue': round(revenue, 2),
                'orders': orders,
                'customers': customers
            })
        
        return pd.DataFrame(data)
    
    def get_dashboard_stats(self):
        """Calculate overall dashboard statistics"""
        total_revenue = self.data['revenue'].sum()
        total_orders = self.data['orders'].sum()
        total_customers = self.data['customers'].sum()
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Calculate growth (last 7 days vs previous 7 days)
        last_7_days = self.data.tail(7)
        prev_7_days = self.data.tail(14).head(7)
        
        revenue_growth = ((last_7_days['revenue'].sum() - prev_7_days['revenue'].sum()) 
                         / prev_7_days['revenue'].sum() * 100)
        orders_growth = ((last_7_days['orders'].sum() - prev_7_days['orders'].sum()) 
                        / prev_7_days['orders'].sum() * 100)
        customers_growth = ((last_7_days['customers'].sum() - prev_7_days['customers'].sum()) 
                           / prev_7_days['customers'].sum() * 100)
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_orders': int(total_orders),
            'total_customers': int(total_customers),
            'average_order_value': round(average_order_value, 2),
            'revenue_growth': round(revenue_growth, 2),
            'orders_growth': round(orders_growth, 2),
            'customers_growth': round(customers_growth, 2)
        }
    
    def get_sales_chart_data(self):
        """Get data formatted for sales chart"""
        return {
            'labels': self.data['date'].tolist(),
            'datasets': [
                {
                    'label': 'Revenue',
                    'data': self.data['revenue'].tolist(),
                    'borderColor': 'rgb(59, 130, 246)',
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'tension': 0.4
                }
            ]
        }
    
    def get_category_chart_data(self):
        """Get data for category breakdown (sample data)"""
        categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
        values = [random.randint(5000, 15000) for _ in range(5)]
        
        return {
            'labels': categories,
            'datasets': [
                {
                    'label': 'Sales by Category',
                    'data': values,
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
    
    def get_recent_sales(self, limit=10):
        """Get most recent sales data"""
        recent = self.data.tail(limit)
        return recent.to_dict('records')
    
    def get_all_analytics(self):
        """Get all analytics data for dashboard"""
        return {
            'stats': self.get_dashboard_stats(),
            'sales_chart': self.get_sales_chart_data(),
            'category_chart': self.get_category_chart_data(),
            'recent_sales': self.get_recent_sales()
        }

# Create a singleton instance
data_service = DataService()