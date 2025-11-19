'use client';

import { useState, useEffect } from 'react';
import { DollarSign, ShoppingCart, Users, TrendingUp, RefreshCw } from 'lucide-react';
import StatsCard from '@/components/dashboard/StatsCard';
import SalesChart from '@/components/dashboard/SalesChart';
import CategoryChart from '@/components/dashboard/CategoryChart';
import RecentSales from '@/components/dashboard/RecentSales';
import { fetchAnalytics, refreshData } from '@/lib/api';

export default function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  // Fetch analytics data
  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const analyticsData = await fetchAnalytics();
      setData(analyticsData);
    } catch (err) {
      setError('Failed to load analytics data. Please make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Refresh data
  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      await refreshData();
      await loadData();
    } catch (err) {
      setError('Failed to refresh data.');
      console.error(err);
    } finally {
      setRefreshing(false);
    }
  };

  // Load data on mount
  useEffect(() => {
    loadData();
  }, []);

  // Format currency
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(value);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
              <p className="mt-1 text-sm text-gray-500">
                Real-time insights and performance metrics
              </p>
            </div>
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              {refreshing ? 'Refreshing...' : 'Refresh Data'}
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Revenue"
            value={formatCurrency(data?.stats?.total_revenue || 0)}
            change={data?.stats?.revenue_growth || 0}
            icon={DollarSign}
          />
          <StatsCard
            title="Total Orders"
            value={data?.stats?.total_orders?.toLocaleString() || '0'}
            change={data?.stats?.orders_growth || 0}
            icon={ShoppingCart}
          />
          <StatsCard
            title="Total Customers"
            value={data?.stats?.total_customers?.toLocaleString() || '0'}
            change={data?.stats?.customers_growth || 0}
            icon={Users}
          />
          <StatsCard
            title="Avg Order Value"
            value={formatCurrency(data?.stats?.average_order_value || 0)}
            change={data?.stats?.revenue_growth || 0}
            icon={TrendingUp}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <SalesChart data={data?.sales_chart} />
          <CategoryChart data={data?.category_chart} />
        </div>

        {/* Recent Sales Table */}
        <RecentSales data={data?.recent_sales} />
      </div>
    </main>
  );
}