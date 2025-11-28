FROM python:3.11.1-slim

WORKDIR /backend

# Отключаем буферизацию и байт-код
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV USE_PROXY "false"
ENV PROXY_URL "socks5://username:password@host.docker.internal:1080/"

# Копируем файл с зависимостями отдельно, чтобы кешировать этот шаг
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Копируем файл конфигурации для отладки
COPY config.py config.py

EXPOSE 7827