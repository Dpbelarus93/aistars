import React from 'react';
import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-gray-300">404</h1>
          <h2 className="text-3xl font-bold text-gray-900 mt-4">
            Страница не найдена
          </h2>
          <p className="text-gray-600 mt-2 max-w-md mx-auto">
            Запрашиваемая страница не существует или была перемещена.
          </p>
        </div>
        
        <div className="space-y-4">
          <Link
            to="/"
            className="btn btn-primary inline-flex items-center space-x-2"
          >
            <Home className="h-4 w-4" />
            <span>На главную</span>
          </Link>
          
          <div className="mt-4">
            <button
              onClick={() => window.history.back()}
              className="btn btn-secondary inline-flex items-center space-x-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Назад</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};