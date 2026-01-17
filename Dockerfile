# Usamos una versión estable de Python en Debian Bookworm
FROM python:3.10-bookworm

# Evita que apt-get haga preguntas interactivas
ENV DEBIAN_FRONTEND=noninteractive

# Instalamos el Driver de SQL Server usando el método recomendado actual
RUN apt-get update && apt-get install -y curl gnupg2 apt-utils \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install -y unixodbc-dev \
    && apt-get clean

# Directorio de trabajo
WORKDIR /app

# Copiamos archivos e instalamos dependencias de Python
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]