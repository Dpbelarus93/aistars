import React from 'react';
import { Order } from '../types';
import { 
  Clock, 
  MapPin, 
  DollarSign, 
  User, 
  AlertTriangle,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

interface OrderCardProps {
  order: Order;
  onEdit?: (order: Order) => void;
  onDelete?: (orderId: string) => void;
  onAssign?: (orderId: string) => void;
  onComplete?: (orderId: string) => void;
  showActions?: boolean;
}

export const OrderCard: React.FC<OrderCardProps> = ({
  order,
  onEdit,
  onDelete,
  onAssign,
  onComplete,
  showActions = false
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'IN_PROGRESS':
        return 'bg-blue-100 text-blue-800';
      case 'COMPLETED':
        return 'bg-green-100 text-green-800';
      case 'CANCELLED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'PENDING':
        return 'Ожидает';
      case 'IN_PROGRESS':
        return 'В работе';
      case 'COMPLETED':
        return 'Завершен';
      case 'CANCELLED':
        return 'Отменен';
      default:
        return status;
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'LOW':
        return 'text-green-600';
      case 'MEDIUM':
        return 'text-yellow-600';
      case 'HIGH':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getUrgencyText = (urgency: string) => {
    switch (urgency) {
      case 'LOW':
        return 'Низкая';
      case 'MEDIUM':
        return 'Средняя';
      case 'HIGH':
        return 'Высокая';
      default:
        return urgency;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {order.title}
          </h3>
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {order.description}
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
            {getStatusText(order.status)}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="flex items-center space-x-2">
          <AlertTriangle className={`h-4 w-4 ${getUrgencyColor(order.urgency)}`} />
          <span className="text-sm text-gray-600">
            {getUrgencyText(order.urgency)}
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <Clock className="h-4 w-4 text-gray-400" />
          <span className="text-sm text-gray-600">
            {format(new Date(order.createdAt), 'dd MMM yyyy', { locale: ru })}
          </span>
        </div>

        {order.location && (
          <div className="flex items-center space-x-2">
            <MapPin className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600 truncate">
              {order.location}
            </span>
          </div>
        )}

        {order.budget && (
          <div className="flex items-center space-x-2">
            <DollarSign className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600">
              {order.budget.toLocaleString()} ₽
            </span>
          </div>
        )}
      </div>

      {/* Участники */}
      <div className="border-t pt-4">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-2">
            <User className="h-4 w-4 text-gray-400" />
            <span className="text-gray-600">
              Клиент: {order.client.name}
            </span>
          </div>
          
          {order.contractor && (
            <div className="flex items-center space-x-2">
              <span className="text-gray-600">
                Исполнитель: {order.contractor.name}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Действия */}
      {showActions && (
        <div className="border-t pt-4 mt-4">
          <div className="flex items-center justify-between">
            <div className="flex space-x-2">
              {onEdit && (
                <button
                  onClick={() => onEdit(order)}
                  className="btn btn-secondary px-3 py-1 text-xs"
                >
                  Редактировать
                </button>
              )}
              
              {onAssign && order.status === 'PENDING' && (
                <button
                  onClick={() => onAssign(order.id)}
                  className="btn btn-primary px-3 py-1 text-xs"
                >
                  Назначить
                </button>
              )}
              
              {onComplete && order.status === 'IN_PROGRESS' && (
                <button
                  onClick={() => onComplete(order.id)}
                  className="btn btn-primary px-3 py-1 text-xs flex items-center space-x-1"
                >
                  <CheckCircle className="h-3 w-3" />
                  <span>Завершить</span>
                </button>
              )}
            </div>
            
            {onDelete && (
              <button
                onClick={() => onDelete(order.id)}
                className="btn btn-danger px-3 py-1 text-xs flex items-center space-x-1"
              >
                <XCircle className="h-3 w-3" />
                <span>Удалить</span>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};