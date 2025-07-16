import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { RootState } from '../store/store';
import { fetchOrders } from '../store/slices/orderSlice';
import { fetchChatSessions } from '../store/slices/chatSlice';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { OrderCard } from '../components/OrderCard';
import { 
  ShoppingCart, 
  MessageCircle, 
  CheckCircle, 
  Clock, 
  AlertTriangle,
  Plus,
  TrendingUp
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { orders, isLoading: ordersLoading } = useSelector((state: RootState) => state.orders);
  const { sessions, isLoading: sessionsLoading } = useSelector((state: RootState) => state.chat);

  useEffect(() => {
    dispatch(fetchOrders({ limit: 5 }));
    dispatch(fetchChatSessions());
  }, [dispatch]);

  const pendingOrders = orders.filter(order => order.status === 'PENDING');
  const inProgressOrders = orders.filter(order => order.status === 'IN_PROGRESS');
  const completedOrders = orders.filter(order => order.status === 'COMPLETED');

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Доброе утро';
    if (hour < 18) return 'Добрый день';
    return 'Добрый вечер';
  };

  const stats = [
    {
      title: 'Ожидают',
      value: pendingOrders.length,
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      title: 'В работе',
      value: inProgressOrders.length,
      icon: AlertTriangle,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Завершено',
      value: completedOrders.length,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Чаты',
      value: sessions.length,
      icon: MessageCircle,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {getGreeting()}, {user?.name}!
            </h1>
            <p className="text-gray-600 mt-1">
              Добро пожаловать в систему управления заказами
            </p>
          </div>
          <div className="flex space-x-3">
            <Link
              to="/orders"
              className="btn btn-primary flex items-center space-x-2"
            >
              <Plus className="h-4 w-4" />
              <span>Создать заказ</span>
            </Link>
            <Link
              to="/chat"
              className="btn btn-secondary flex items-center space-x-2"
            >
              <MessageCircle className="h-4 w-4" />
              <span>Чат</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.title} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className={`flex-shrink-0 p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Orders */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              Последние заказы
            </h2>
            <Link
              to="/orders"
              className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center space-x-1"
            >
              <span>Все заказы</span>
              <TrendingUp className="h-4 w-4" />
            </Link>
          </div>
        </div>
        
        <div className="p-6">
          {ordersLoading ? (
            <LoadingSpinner className="py-8" />
          ) : orders.length === 0 ? (
            <div className="text-center py-8">
              <ShoppingCart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Заказов пока нет</p>
              <Link
                to="/orders"
                className="btn btn-primary mt-4 inline-flex items-center space-x-2"
              >
                <Plus className="h-4 w-4" />
                <span>Создать первый заказ</span>
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {orders.slice(0, 3).map((order) => (
                <OrderCard key={order.id} order={order} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Быстрые действия
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/orders"
            className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
          >
            <div className="text-center">
              <ShoppingCart className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900">Управление заказами</p>
              <p className="text-xs text-gray-500">Создавайте и отслеживайте заказы</p>
            </div>
          </Link>
          
          <Link
            to="/chat"
            className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
          >
            <div className="text-center">
              <MessageCircle className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900">Чат с поддержкой</p>
              <p className="text-xs text-gray-500">Получите помощь от AI-ассистента</p>
            </div>
          </Link>
          
          <Link
            to="/profile"
            className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
          >
            <div className="text-center">
              <TrendingUp className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900">Мой профиль</p>
              <p className="text-xs text-gray-500">Настройки и предпочтения</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};