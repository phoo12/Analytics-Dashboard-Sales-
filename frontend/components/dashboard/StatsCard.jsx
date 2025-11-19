import { TrendingUp, TrendingDown } from 'lucide-react';

export default function StatsCard({ title, value, change, icon: Icon }) {
  const isPositive = change >= 0;
  
  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        {Icon && (
          <div className="bg-blue-50 p-3 rounded-lg">
            <Icon className="w-6 h-6 text-blue-600" />
          </div>
        )}
      </div>
      
      <div className="flex items-center mt-4">
        {isPositive ? (
          <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
        ) : (
          <TrendingDown className="w-4 h-4 text-red-600 mr-1" />
        )}
        <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
          {Math.abs(change).toFixed(1)}%
        </span>
        <span className="text-sm text-gray-500 ml-2">vs last week</span>
      </div>
    </div>
  );
}