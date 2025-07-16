import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { 
  Search, 
  Filter, 
  Star, 
  MapPin, 
  Clock, 
  DollarSign,
  Heart,
  ShoppingCart,
  Grid,
  List,
  Plus
} from 'lucide-react';
import { Service, ServiceCategory, City } from '../types';
import { toast } from 'react-toastify';

export const ServicesPage: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilters, setShowFilters] = useState(false);
  
  // Фильтры
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [priceFrom, setPriceFrom] = useState('');
  const [priceTo, setPriceTo] = useState('');
  const [sortBy, setSortBy] = useState('rating');

  // Моковые данные
  const mockServices: Service[] = [
    {
      id: '1',
      title: 'Аренда велосипедов',
      description: 'Качественные велосипеды для прогулок по городу. Разные модели для всех возрастов.',
      shortDescription: 'Велосипеды для прогулок',
      categoryId: 'bikes',
      category: { id: 'bikes', name: 'Велосипеды', description: 'Аренда и продажа велосипедов', isActive: true, servicesCount: 5, createdAt: '', updatedAt: '' },
      basePrice: 500,
      priceType: 'HOURLY' as const,
      duration: 60,
      images: ['https://via.placeholder.com/300x200'],
      isActive: true,
      cityId: 'moscow',
      city: { id: 'moscow', name: 'Москва', countryId: 'ru', country: { id: 'ru', name: 'Россия', code: 'RU', isActive: true, createdAt: '', updatedAt: '' }, isActive: true, servicesCount: 10, createdAt: '', updatedAt: '' },
      providerId: 'provider1',
      provider: { id: 'provider1', name: 'Велопрокат МСК', email: 'bike@example.com', role: 'CONTRACTOR' as const, isVerified: true, createdAt: '', updatedAt: '' },
      rating: 4.8,
      reviewsCount: 124,
      bookingsCount: 340,
      tags: ['спорт', 'активный отдых', 'экология'],
      requirements: ['Документ удостоверяющий личность', 'Залог 2000₽'],
      whatIncluded: ['Шлем', 'Замок', 'Карта маршрутов'],
      createdAt: '',
      updatedAt: ''
    },
    {
      id: '2',
      title: 'Доставка еды',
      description: 'Быстрая доставка еды из лучших ресторанов города. Горячие блюда за 30 минут.',
      shortDescription: 'Доставка еды за 30 минут',
      categoryId: 'delivery',
      category: { id: 'delivery', name: 'Доставка', description: 'Доставка еды и товаров', isActive: true, servicesCount: 8, createdAt: '', updatedAt: '' },
      basePrice: 200,
      priceType: 'FIXED' as const,
      duration: 30,
      images: ['https://via.placeholder.com/300x200'],
      isActive: true,
      cityId: 'moscow',
      city: { id: 'moscow', name: 'Москва', countryId: 'ru', country: { id: 'ru', name: 'Россия', code: 'RU', isActive: true, createdAt: '', updatedAt: '' }, isActive: true, servicesCount: 10, createdAt: '', updatedAt: '' },
      providerId: 'provider2',
      provider: { id: 'provider2', name: 'Быстрая доставка', email: 'delivery@example.com', role: 'CONTRACTOR' as const, isVerified: true, createdAt: '', updatedAt: '' },
      rating: 4.6,
      reviewsCount: 89,
      bookingsCount: 567,
      tags: ['еда', 'быстро', 'горячее'],
      requirements: ['Оплата при получении или онлайн'],
      whatIncluded: ['Упаковка', 'Приборы', 'Салфетки'],
      createdAt: '',
      updatedAt: ''
    },
    {
      id: '3',
      title: 'Уборка квартиры',
      description: 'Профессиональная уборка квартир и офисов. Используем экологически чистые средства.',
      shortDescription: 'Профессиональная уборка',
      categoryId: 'cleaning',
      category: { id: 'cleaning', name: 'Уборка', description: 'Клининговые услуги', isActive: true, servicesCount: 12, createdAt: '', updatedAt: '' },
      basePrice: 2000,
      priceType: 'FIXED' as const,
      duration: 120,
      images: ['https://via.placeholder.com/300x200'],
      isActive: true,
      cityId: 'spb',
      city: { id: 'spb', name: 'Санкт-Петербург', countryId: 'ru', country: { id: 'ru', name: 'Россия', code: 'RU', isActive: true, createdAt: '', updatedAt: '' }, isActive: true, servicesCount: 8, createdAt: '', updatedAt: '' },
      providerId: 'provider3',
      provider: { id: 'provider3', name: 'Чистый дом', email: 'clean@example.com', role: 'CONTRACTOR' as const, isVerified: true, createdAt: '', updatedAt: '' },
      rating: 4.9,
      reviewsCount: 156,
      bookingsCount: 234,
      tags: ['уборка', 'чистота', 'экология'],
      requirements: ['Доступ к объекту', 'Предоплата 50%'],
      whatIncluded: ['Все средства', 'Инвентарь', 'Гарантия качества'],
      createdAt: '',
      updatedAt: ''
    }
  ];

  const mockCategories: ServiceCategory[] = [
    { id: 'bikes', name: 'Велосипеды', description: 'Аренда и продажа велосипедов', isActive: true, servicesCount: 5, createdAt: '', updatedAt: '' },
    { id: 'delivery', name: 'Доставка', description: 'Доставка еды и товаров', isActive: true, servicesCount: 8, createdAt: '', updatedAt: '' },
    { id: 'cleaning', name: 'Уборка', description: 'Клининговые услуги', isActive: true, servicesCount: 12, createdAt: '', updatedAt: '' },
    { id: 'repair', name: 'Ремонт', description: 'Ремонт и обслуживание', isActive: true, servicesCount: 15, createdAt: '', updatedAt: '' },
    { id: 'transport', name: 'Транспорт', description: 'Транспортные услуги', isActive: true, servicesCount: 7, createdAt: '', updatedAt: '' }
  ];

  const mockCities: City[] = [
    { id: 'moscow', name: 'Москва', countryId: 'ru', country: { id: 'ru', name: 'Россия', code: 'RU', isActive: true, createdAt: '', updatedAt: '' }, isActive: true, servicesCount: 10, createdAt: '', updatedAt: '' },
    { id: 'spb', name: 'Санкт-Петербург', countryId: 'ru', country: { id: 'ru', name: 'Россия', code: 'RU', isActive: true, createdAt: '', updatedAt: '' }, isActive: true, servicesCount: 8, createdAt: '', updatedAt: '' },
    { id: 'ekb', name: 'Екатеринбург', countryId: 'ru', country: { id: 'ru', name: 'Россия', code: 'RU', isActive: true, createdAt: '', updatedAt: '' }, isActive: true, servicesCount: 5, createdAt: '', updatedAt: '' }
  ];

  useEffect(() => {
    // Симуляция загрузки данных
    setTimeout(() => {
      setServices(mockServices);
      setCategories(mockCategories);
      setCities(mockCities);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredServices = services.filter(service => {
    const matchesSearch = service.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || service.categoryId === selectedCategory;
    const matchesCity = !selectedCity || service.cityId === selectedCity;
    const matchesPrice = (!priceFrom || service.basePrice >= parseInt(priceFrom)) &&
                        (!priceTo || service.basePrice <= parseInt(priceTo));
    
    return matchesSearch && matchesCategory && matchesCity && matchesPrice;
  });

  const handleBookService = (serviceId: string) => {
    toast.success('Перенаправление на страницу заказа');
    // Здесь будет логика создания заказа
  };

  const handleToggleFavorite = (serviceId: string) => {
    toast.info('Добавлено в избранное');
  };

  const getPriceText = (service: Service) => {
    const priceTypeText = {
      FIXED: 'фиксированная цена',
      HOURLY: 'за час',
      NEGOTIABLE: 'договорная'
    };
    return `${service.basePrice}₽ ${priceTypeText[service.priceType]}`;
  };

  const ServiceCard: React.FC<{ service: Service }> = ({ service }) => (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="relative">
        <img 
          src={service.images[0]} 
          alt={service.title}
          className="w-full h-48 object-cover"
        />
        <button 
          onClick={() => handleToggleFavorite(service.id)}
          className="absolute top-2 right-2 p-2 bg-white rounded-full shadow-md hover:bg-gray-50"
        >
          <Heart className="h-4 w-4 text-gray-600" />
        </button>
        <div className="absolute top-2 left-2 bg-white px-2 py-1 rounded-full">
          <div className="flex items-center space-x-1">
            <Star className="h-3 w-3 text-yellow-500 fill-current" />
            <span className="text-xs font-medium">{service.rating}</span>
          </div>
        </div>
      </div>
      
      <div className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {service.title}
          </h3>
          <span className="text-sm text-gray-500">{service.category.name}</span>
        </div>
        
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {service.shortDescription}
        </p>
        
        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
          <div className="flex items-center space-x-1">
            <MapPin className="h-4 w-4" />
            <span>{service.city.name}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Clock className="h-4 w-4" />
            <span>{service.duration} мин</span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-1">
            <DollarSign className="h-4 w-4 text-green-600" />
            <span className="font-semibold text-green-600">
              {getPriceText(service)}
            </span>
          </div>
          <button 
            onClick={() => handleBookService(service.id)}
            className="btn btn-primary flex items-center space-x-1"
          >
            <ShoppingCart className="h-4 w-4" />
            <span>Заказать</span>
          </button>
        </div>
        
        <div className="mt-3 pt-3 border-t">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>{service.reviewsCount} отзывов</span>
            <span>{service.bookingsCount} заказов</span>
          </div>
        </div>
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
            <h1 className="text-2xl font-bold text-gray-900">Каталог услуг</h1>
            <p className="text-gray-600 mt-1">
              Найдите нужную услугу в вашем городе
            </p>
          </div>
          {user?.role === 'CONTRACTOR' && (
            <button className="btn btn-primary flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Добавить услугу</span>
            </button>
          )}
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
              placeholder="Поиск услуг..."
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
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-md ${viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'}`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-md ${viewMode === 'list' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'}`}
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>

        {showFilters && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 pt-4 border-t">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Категория
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="input w-full"
              >
                <option value="">Все категории</option>
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Город
              </label>
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="input w-full"
              >
                <option value="">Все города</option>
                {cities.map(city => (
                  <option key={city.id} value={city.id}>
                    {city.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Цена от
              </label>
              <input
                type="number"
                value={priceFrom}
                onChange={(e) => setPriceFrom(e.target.value)}
                className="input w-full"
                placeholder="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Цена до
              </label>
              <input
                type="number"
                value={priceTo}
                onChange={(e) => setPriceTo(e.target.value)}
                className="input w-full"
                placeholder="∞"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Сортировка
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="input w-full"
              >
                <option value="rating">По рейтингу</option>
                <option value="price_low">По цене (возр.)</option>
                <option value="price_high">По цене (убыв.)</option>
                <option value="popular">По популярности</option>
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Services Grid */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Найдено: {filteredServices.length} услуг
          </h2>
        </div>
        
        <div className="p-6">
          {filteredServices.length === 0 ? (
            <div className="text-center py-8">
              <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Услуги не найдены</p>
              <p className="text-sm text-gray-400">Попробуйте изменить параметры поиска</p>
            </div>
          ) : (
            <div className={`grid gap-6 ${
              viewMode === 'grid' 
                ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
                : 'grid-cols-1'
            }`}>
              {filteredServices.map(service => (
                <ServiceCard key={service.id} service={service} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};