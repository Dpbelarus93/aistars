import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { 
  Star, 
  MapPin, 
  DollarSign, 
  TrendingUp, 
  Users, 
  Award, 
  Shield, 
  Clock,
  Phone,
  Mail,
  FileText,
  CheckCircle,
  XCircle,
  Eye,
  Filter,
  Search
} from 'lucide-react';
import { Partner } from '../types';
import { toast } from 'react-toastify';

export const PartnersPage: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [partners, setPartners] = useState<Partner[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'top' | 'new' | 'my'>('all');
  const [showFilters, setShowFilters] = useState(false);
  
  // Фильтры
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');

  // Моковые данные партнеров
  const mockPartners: Partner[] = [
    {
      id: '1',
      userId: 'user1',
      user: {
        id: 'user1',
        name: 'Иван Петров',
        email: 'ivan@example.com',
        role: 'CONTRACTOR',
        phone: '+7 (999) 123-45-67',
        isVerified: true,
        cityId: 'moscow',
        createdAt: '2023-01-15T10:00:00Z',
        updatedAt: '2023-01-15T10:00:00Z'
      },
      companyName: 'Быстрый Ремонт',
      businessType: 'COMPANY',
      level: 'GOLD',
      commissionRate: 12,
      totalEarnings: 450000,
      totalOrders: 89,
      activeServices: 5,
      rating: 4.8,
      isActive: true,
      joinedAt: '2023-01-15T10:00:00Z',
      verificationStatus: 'VERIFIED',
      documents: ['passport.jpg', 'license.pdf'],
      specializations: ['Сантехника', 'Электрика', 'Ремонт'],
      workingHours: {
        monday: { start: '09:00', end: '18:00', isWorking: true },
        tuesday: { start: '09:00', end: '18:00', isWorking: true },
        wednesday: { start: '09:00', end: '18:00', isWorking: true },
        thursday: { start: '09:00', end: '18:00', isWorking: true },
        friday: { start: '09:00', end: '18:00', isWorking: true },
        saturday: { start: '10:00', end: '16:00', isWorking: true },
        sunday: { start: '10:00', end: '16:00', isWorking: false }
      },
      createdAt: '2023-01-15T10:00:00Z',
      updatedAt: '2023-01-15T10:00:00Z'
    },
    {
      id: '2',
      userId: 'user2',
      user: {
        id: 'user2',
        name: 'Мария Сидорова',
        email: 'maria@example.com',
        role: 'CONTRACTOR',
        phone: '+7 (999) 234-56-78',
        isVerified: true,
        cityId: 'spb',
        createdAt: '2023-02-20T10:00:00Z',
        updatedAt: '2023-02-20T10:00:00Z'
      },
      companyName: 'Чистый Дом СПб',
      businessType: 'COMPANY',
      level: 'SILVER',
      commissionRate: 15,
      totalEarnings: 280000,
      totalOrders: 67,
      activeServices: 3,
      rating: 4.6,
      isActive: true,
      joinedAt: '2023-02-20T10:00:00Z',
      verificationStatus: 'VERIFIED',
      documents: ['passport.jpg', 'license.pdf'],
      specializations: ['Уборка', 'Клининг'],
      workingHours: {
        monday: { start: '08:00', end: '20:00', isWorking: true },
        tuesday: { start: '08:00', end: '20:00', isWorking: true },
        wednesday: { start: '08:00', end: '20:00', isWorking: true },
        thursday: { start: '08:00', end: '20:00', isWorking: true },
        friday: { start: '08:00', end: '20:00', isWorking: true },
        saturday: { start: '09:00', end: '18:00', isWorking: true },
        sunday: { start: '09:00', end: '18:00', isWorking: false }
      },
      createdAt: '2023-02-20T10:00:00Z',
      updatedAt: '2023-02-20T10:00:00Z'
    },
    {
      id: '3',
      userId: 'user3',
      user: {
        id: 'user3',
        name: 'Алексей Козлов',
        email: 'alexey@example.com',
        role: 'CONTRACTOR',
        phone: '+7 (999) 345-67-89',
        isVerified: false,
        cityId: 'ekb',
        createdAt: '2023-03-10T10:00:00Z',
        updatedAt: '2023-03-10T10:00:00Z'
      },
      businessType: 'INDIVIDUAL',
      level: 'BRONZE',
      commissionRate: 18,
      totalEarnings: 95000,
      totalOrders: 23,
      activeServices: 2,
      rating: 4.3,
      isActive: true,
      joinedAt: '2023-03-10T10:00:00Z',
      verificationStatus: 'PENDING',
      documents: ['passport.jpg'],
      specializations: ['Доставка', 'Курьерские услуги'],
      workingHours: {
        monday: { start: '10:00', end: '22:00', isWorking: true },
        tuesday: { start: '10:00', end: '22:00', isWorking: true },
        wednesday: { start: '10:00', end: '22:00', isWorking: true },
        thursday: { start: '10:00', end: '22:00', isWorking: true },
        friday: { start: '10:00', end: '22:00', isWorking: true },
        saturday: { start: '10:00', end: '22:00', isWorking: true },
        sunday: { start: '10:00', end: '22:00', isWorking: true }
      },
      createdAt: '2023-03-10T10:00:00Z',
      updatedAt: '2023-03-10T10:00:00Z'
    }
  ];

  useEffect(() => {
    // Симуляция загрузки данных
    setTimeout(() => {
      setPartners(mockPartners);
      setLoading(false);
    }, 1000);
  }, []);

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'PLATINUM': return 'bg-purple-100 text-purple-800';
      case 'GOLD': return 'bg-yellow-100 text-yellow-800';
      case 'SILVER': return 'bg-gray-100 text-gray-800';
      case 'BRONZE': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'VERIFIED': return 'text-green-600';
      case 'PENDING': return 'text-yellow-600';
      case 'REJECTED': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'VERIFIED': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'PENDING': return <Clock className="h-4 w-4 text-yellow-600" />;
      case 'REJECTED': return <XCircle className="h-4 w-4 text-red-600" />;
      default: return <Clock className="h-4 w-4 text-gray-600" />;
    }
  };

  const filteredPartners = partners.filter(partner => {
    const matchesSearch = partner.user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         partner.companyName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         partner.specializations.some(spec => spec.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesLevel = !selectedLevel || partner.level === selectedLevel;
    const matchesType = !selectedType || partner.businessType === selectedType;
    const matchesStatus = !selectedStatus || partner.verificationStatus === selectedStatus;
    
    return matchesSearch && matchesLevel && matchesType && matchesStatus;
  });

  const handleViewPartner = (partnerId: string) => {
    toast.info('Открытие профиля партнера');
  };

  const handleContactPartner = (partnerId: string) => {
    toast.info('Открытие чата с партнером');
  };

  const PartnerCard: React.FC<{ partner: Partner }> = ({ partner }) => (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold">
              {partner.user.name.charAt(0)}
            </span>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">
              {partner.companyName || partner.user.name}
            </h3>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">{partner.user.name}</span>
              {getStatusIcon(partner.verificationStatus)}
            </div>
          </div>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(partner.level)}`}>
          {partner.level}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="flex items-center space-x-2">
          <Star className="h-4 w-4 text-yellow-500" />
          <span className="text-sm">
            {partner.rating} ({partner.totalOrders} заказов)
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <DollarSign className="h-4 w-4 text-green-500" />
          <span className="text-sm">
            {partner.totalEarnings.toLocaleString()}₽
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <Users className="h-4 w-4 text-blue-500" />
          <span className="text-sm">
            {partner.activeServices} услуг
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <TrendingUp className="h-4 w-4 text-purple-500" />
          <span className="text-sm">
            {partner.commissionRate}% комиссия
          </span>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-600 mb-2">Специализации:</p>
        <div className="flex flex-wrap gap-2">
          {partner.specializations.map((spec, index) => (
            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
              {spec}
            </span>
          ))}
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={() => handleViewPartner(partner.id)}
          className="btn btn-secondary flex items-center space-x-1 flex-1"
        >
          <Eye className="h-4 w-4" />
          <span>Профиль</span>
        </button>
        <button
          onClick={() => handleContactPartner(partner.id)}
          className="btn btn-primary flex items-center space-x-1 flex-1"
        >
          <Mail className="h-4 w-4" />
          <span>Написать</span>
        </button>
      </div>
    </div>
  );

  if (loading) {
    return <LoadingSpinner className="py-8" />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Партнеры</h1>
            <p className="text-gray-600 mt-1">
              Проверенные исполнители и поставщики услуг
            </p>
          </div>
          {user?.role === 'ADMIN' && (
            <button className="btn btn-primary">
              Управление партнерами
            </button>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{partners.length}</p>
              <p className="text-sm text-gray-500">Всего партнеров</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {partners.filter(p => p.verificationStatus === 'VERIFIED').length}
              </p>
              <p className="text-sm text-gray-500">Верифицированных</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-yellow-100 rounded-lg">
              <Award className="h-6 w-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {partners.filter(p => p.level === 'GOLD' || p.level === 'PLATINUM').length}
              </p>
              <p className="text-sm text-gray-500">Премиум партнеров</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-purple-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {partners.reduce((sum, p) => sum + p.totalEarnings, 0).toLocaleString()}₽
              </p>
              <p className="text-sm text-gray-500">Общий доход</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            {[
              { id: 'all', label: 'Все партнеры', count: partners.length },
              { id: 'top', label: 'Топ партнеры', count: partners.filter(p => p.level === 'GOLD' || p.level === 'PLATINUM').length },
              { id: 'new', label: 'Новые', count: partners.filter(p => p.verificationStatus === 'PENDING').length },
              { id: 'my', label: 'Мои', count: 0 }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        {/* Search and Filters */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-4">
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Поиск партнеров..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10 w-full"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn btn-secondary flex items-center space-x-2"
            >
              <Filter className="h-4 w-4" />
              <span>Фильтры</span>
            </button>
          </div>

          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 pt-4 border-t">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Уровень
                </label>
                <select
                  value={selectedLevel}
                  onChange={(e) => setSelectedLevel(e.target.value)}
                  className="input w-full"
                >
                  <option value="">Все уровни</option>
                  <option value="PLATINUM">Платина</option>
                  <option value="GOLD">Золото</option>
                  <option value="SILVER">Серебро</option>
                  <option value="BRONZE">Бронза</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Тип бизнеса
                </label>
                <select
                  value={selectedType}
                  onChange={(e) => setSelectedType(e.target.value)}
                  className="input w-full"
                >
                  <option value="">Все типы</option>
                  <option value="INDIVIDUAL">Индивидуальный</option>
                  <option value="COMPANY">Компания</option>
                  <option value="AGENCY">Агентство</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Статус
                </label>
                <select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value)}
                  className="input w-full"
                >
                  <option value="">Все статусы</option>
                  <option value="VERIFIED">Верифицирован</option>
                  <option value="PENDING">На проверке</option>
                  <option value="REJECTED">Отклонен</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Partners Grid */}
        <div className="p-6">
          {filteredPartners.length === 0 ? (
            <div className="text-center py-8">
              <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Партнеры не найдены</p>
              <p className="text-sm text-gray-400">Попробуйте изменить параметры поиска</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPartners.map(partner => (
                <PartnerCard key={partner.id} partner={partner} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Partner Program Info */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Партнерская программа
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Преимущества</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Стабильный поток заказов</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Прозрачная система комиссий</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Поддержка 24/7</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Бонусы за качество</span>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Уровни партнерства</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-orange-600">Бронза</span>
                <span className="text-gray-600">15-18% комиссия</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Серебро</span>
                <span className="text-gray-600">12-15% комиссия</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-yellow-600">Золото</span>
                <span className="text-gray-600">8-12% комиссия</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-purple-600">Платина</span>
                <span className="text-gray-600">5-8% комиссия</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};