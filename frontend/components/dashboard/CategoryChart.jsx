import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

export default function CategoryChart({ data }) {
  if (!data || !data.labels || !data.datasets) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  // Transform data for Recharts
  const chartData = data.labels.map((label, index) => ({
    category: label,
    sales: data.datasets[0]?.data[index] || 0
  }));

  // Colors for bars
  const COLORS = [
    '#3b82f6', // blue
    '#10b981', // green
    '#fbbf24', // yellow
    '#ef4444', // red
    '#8b5cf6'  // purple
  ];

  // Format currency
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Sales by Category</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="category" 
            stroke="#888"
            fontSize={12}
          />
          <YAxis 
            tickFormatter={formatCurrency}
            stroke="#888"
            fontSize={12}
          />
          <Tooltip 
            formatter={(value) => formatCurrency(value)}
            contentStyle={{ 
              backgroundColor: 'white', 
              border: '1px solid #e5e7eb',
              borderRadius: '6px'
            }}
          />
          <Legend />
          <Bar dataKey="sales" name="Sales" radius={[8, 8, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}