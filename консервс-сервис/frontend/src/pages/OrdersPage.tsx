import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { fetchOrders, setFilters, updateOrder } from '../store/slices/orderSlice';
import { OrderCard } from '../components/OrderCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { Plus, Search, Filter, ChevronLeft, ChevronRight } from 'lucide-react';
import { toast } from 'react-toastify';

export const OrdersPage: React.FC = () => {
  const dispatch = useDispatch();
  const { orders, pagination, filters, isLoading, error } = useSelector((state: RootState) => state.orders);
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [showFilters, setShowFilters] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [urgencyFilter, setUrgencyFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');

  useEffect(() => {
    dispatch(fetchOrders({ page: pagination.page, limit: pagination.limit, filters }));
  }, [dispatch, pagination.page, pagination.limit, filters]);

  const handleSearch = () => {
    const newFilters = {
      search: searchTerm,
      status: statusFilter,
      urgency: urgencyFilter,
      category: categoryFilter,
    };
    dispatch(setFilters(newFilters));
    dispatch(fetchOrders({ page: 1, limit: pagination.limit, filters: newFilters }));
  };

  const handlePageChange = (page: number) => {
    dispatch(fetchOrders({ page, limit: pagination.limit, filters }));
  };

  const handleAssignOrder = (orderId: string) => {
    // Логика назначения заказа
    toast.info('Функция назначения заказа будет реализована');
  };

  const handleCompleteOrder = (orderId: string) => {
    dispatch(updateOrder({ orderId, data: { status: 'COMPLETED' } }));
    toast.success('Заказ завершен');
  };

  const handleEditOrder = (order: any) => {
    // Логика редактирования заказа
    toast.info('Функция редактирования будет реализована');
  };

  const handleDeleteOrder = (orderId: string) => {
    if (window.confirm('Вы уверены, что хотите удалить этот заказ?')) {
      // Логика удаления заказа
      toast.info('Функция удаления будет реализована');
    }
  };

  const statusOptions = [
    { value: '', label: 'Все статусы' },
    { value: 'PENDING', label: 'Ожидает' },
    { value: 'IN_PROGRESS', label: 'В работе' },
    { value: 'COMPLETED', label: 'Завершен' },
    { value: 'CANCELLED', label: 'Отменен' },
  ];

  const urgencyOptions = [
    { value: '', label: 'Все приоритеты' },
    { value: 'LOW', label: 'Низкий' },
    { value: 'MEDIUM', label: 'Средний' },
    { value: 'HIGH', label: 'Высокий' },
  ];

  const categoryOptions = [
    { value: '', label: 'Все категории' },
    { value: 'plumbing', label: 'Сантехника' },
    { value: 'electrical', label: 'Электрика' },
    { value: 'repair', label: 'Ремонт' },
    { value: 'cleaning', label: 'Уборка' },
    { value: 'delivery', label: 'Доставка' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Заказы</h1>
            <p className="text-gray-600 mt-1">
              Управление заказами и отслеживание выполнения
            </p>
          </div>
          <button className="btn btn-primary flex items-center space-x-2">
            <Plus className="h-4 w-4" />
            <span>Создать заказ</span>
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-4 mb-4">
          <div className="flex-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Поиск заказов..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input pl-10 w-full"
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn btn-secondary flex items-center space-x-2"
          >
            <Filter className="h-4 w-4" />
            <span>Фильтры</span>
          </button>
          <button
            onClick={handleSearch}
            className="btn btn-primary"
          >
            Поиск
          </button>
        </div>

        {showFilters && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Статус
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="input w-full"
              >
                {statusOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Приоритет
              </label>
              <select
                value={urgencyFilter}
                onChange={(e) => setUrgencyFilter(e.target.value)}
                className="input w-full"
              >
                {urgencyOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Категория
              </label>
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="input w-full"
              >
                {categoryOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Orders List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Всего заказов: {pagination.total}
          </h2>
        </div>
        
        <div className="p-6">
          {error && (
            <ErrorMessage message={error} className="mb-4" />
          )}
          
          {isLoading ? (
            <LoadingSpinner className="py-8" />
          ) : orders.length === 0 ? (
            <div className="text-center py-8">
              <Plus className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Заказов не найдено</p>
              <p className="text-sm text-gray-400">Попробуйте изменить фильтры поиска</p>
            </div>
          ) : (
            <div className="space-y-4">
              {orders.map((order) => (
                <OrderCard
                  key={order.id}
                  order={order}
                  onEdit={handleEditOrder}
                  onDelete={handleDeleteOrder}
                  onAssign={handleAssignOrder}
                  onComplete={handleCompleteOrder}
                  showActions={true}
                />
              ))}
            </div>
          )}
        </div>

        {/* Pagination */}
        {pagination.totalPages > 1 && (
          <div className="px-6 py-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-700">
                Показано {((pagination.page - 1) * pagination.limit) + 1} - {Math.min(pagination.page * pagination.limit, pagination.total)} из {pagination.total} заказов
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handlePageChange(pagination.page - 1)}
                  disabled={pagination.page === 1}
                  className="btn btn-secondary p-2 disabled:opacity-50"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>
                
                {[...Array(pagination.totalPages)].map((_, index) => {
                  const page = index + 1;
                  return (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`px-3 py-1 rounded-md text-sm ${
                        pagination.page === page
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {page}
                    </button>
                  );
                })}
                
                <button
                  onClick={() => handlePageChange(pagination.page + 1)}
                  disabled={pagination.page === pagination.totalPages}
                  className="btn btn-secondary p-2 disabled:opacity-50"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};