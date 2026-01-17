# Usamos Debian 11 (Bullseye), que tiene mejor compatibilidad con los drivers actuales
FROM python:3.10-slim-bullseye

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalación paso a paso para identificar fallos
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install -y unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Render usa el puerto 10000 por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]