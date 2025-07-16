import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  ShoppingCart, 
  Users, 
  Activity,
  Calendar
} from 'lucide-react';

export const AnalyticsPage: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  // Моковые данные для демонстрации
  const mockAnalytics = {
    totalOrders: 156,
    completedOrders: 128,
    pendingOrders: 18,
    totalRevenue: 2840000,
    averageOrderValue: 18200,
    ordersByStatus: {
      'PENDING': 18,
      'IN_PROGRESS': 10,
      'COMPLETED': 128,
      'CANCELLED': 5
    },
    ordersByCategory: {
      'Сантехника': 45,
      'Электрика': 38,
      'Ремонт': 32,
      'Уборка': 25,
      'Доставка': 16
    },
    revenueByMonth: [
      { month: 'Янв', revenue: 180000 },
      { month: 'Фев', revenue: 220000 },
      { month: 'Мар', revenue: 280000 },
      { month: 'Апр', revenue: 320000 },
      { month: 'Май', revenue: 290000 },
      { month: 'Июн', revenue: 350000 },
    ]
  };

  const stats = [
    {
      title: 'Общий доход',
      value: '₽2,840,000',
      change: '+12.5%',
      changeType: 'positive' as const,
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Всего заказов',
      value: '156',
      change: '+8.2%',
      changeType: 'positive' as const,
      icon: ShoppingCart,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Активные клиенты',
      value: '89',
      change: '+15.3%',
      changeType: 'positive' as const,
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Средняя стоимость',
      value: '₽18,200',
      change: '-2.1%',
      changeType: 'negative' as const,
      icon: Activity,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
  ];

  const statusData = [
    { name: 'Завершено', value: 128, color: '#10B981' },
    { name: 'Ожидает', value: 18, color: '#F59E0B' },
    { name: 'В работе', value: 10, color: '#3B82F6' },
    { name: 'Отменено', value: 5, color: '#EF4444' },
  ];

  const categoryData = Object.entries(mockAnalytics.ordersByCategory).map(([name, value]) => ({
    name,
    value,
  }));

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Аналитика</h1>
            <p className="text-gray-600 mt-1">
              Статистика и отчеты по работе сервиса
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <button className="btn btn-secondary flex items-center space-x-2">
              <Calendar className="h-4 w-4" />
              <span>Период</span>
            </button>
            <button className="btn btn-primary">
              Экспорт
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.title} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div className={`flex-shrink-0 p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className={`flex items-center space-x-1 ${
                  stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.changeType === 'positive' ? (
                    <TrendingUp className="h-4 w-4" />
                  ) : (
                    <TrendingDown className="h-4 w-4" />
                  )}
                  <span className="text-sm font-medium">{stat.change}</span>
                </div>
              </div>
              <div className="mt-4">
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className="text-sm text-gray-500">{stat.title}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Доходы по месяцам
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockAnalytics.revenueByMonth}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => [`₽${value.toLocaleString()}`, 'Доход']} />
              <Line 
                type="monotone" 
                dataKey="revenue" 
                stroke="#3B82F6" 
                strokeWidth={2}
                dot={{ fill: '#3B82F6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Order Status Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Статусы заказов
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Category Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Заказы по категориям
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Contractors */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Топ исполнителей
          </h3>
          <div className="space-y-4">
            {[
              { name: 'Иван Петров', orders: 23, revenue: 420000 },
              { name: 'Мария Сидорова', orders: 18, revenue: 380000 },
              { name: 'Алексей Козлов', orders: 15, revenue: 290000 },
              { name: 'Елена Васильева', orders: 12, revenue: 240000 },
              { name: 'Дмитрий Смирнов', orders: 10, revenue: 180000 },
            ].map((contractor, index) => (
              <div key={contractor.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {index + 1}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{contractor.name}</p>
                    <p className="text-sm text-gray-500">{contractor.orders} заказов</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">
                    ₽{contractor.revenue.toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-500">доход</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Последняя активность
        </h3>
        <div className="space-y-4">
          {[
            { action: 'Новый заказ создан', user: 'Анна Иванова', time: '5 минут назад', type: 'order' },
            { action: 'Заказ завершен', user: 'Петр Сидоров', time: '15 минут назад', type: 'complete' },
            { action: 'Новый клиент зарегистрирован', user: 'Елена Петрова', time: '30 минут назад', type: 'user' },
            { action: 'Заказ отменен', user: 'Михаил Козлов', time: '1 час назад', type: 'cancel' },
          ].map((activity, index) => (
            <div key={index} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                activity.type === 'order' ? 'bg-blue-100' :
                activity.type === 'complete' ? 'bg-green-100' :
                activity.type === 'user' ? 'bg-purple-100' :
                'bg-red-100'
              }`}>
                <Activity className={`h-4 w-4 ${
                  activity.type === 'order' ? 'text-blue-600' :
                  activity.type === 'complete' ? 'text-green-600' :
                  activity.type === 'user' ? 'text-purple-600' :
                  'text-red-600'
                }`} />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                <p className="text-xs text-gray-500">{activity.user}</p>
              </div>
              <div className="text-xs text-gray-500">
                {activity.time}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};