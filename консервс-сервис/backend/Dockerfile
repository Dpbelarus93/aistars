FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci --only=production

# Копируем исходный код
COPY . .

# Генерируем Prisma клиент
RUN npx prisma generate

# Компилируем TypeScript
RUN npm run build

# Создаем пользователя для безопасности
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Переключаемся на пользователя
USER nodejs

# Открываем порт
EXPOSE 3001

# Запускаем приложение
CMD ["npm", "start"]