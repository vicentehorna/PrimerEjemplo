# Usamos una imagen de Python un poco más completa para evitar instalar herramientas base
FROM python:3.10-slim-bookworm

# Evitar prompts
ENV DEBIAN_FRONTEND=noninteractive

# Instalación simplificada de drivers de SQL Server
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install -y unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# El puerto 10000 es el estándar de Render
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]