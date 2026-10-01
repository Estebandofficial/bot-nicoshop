# Usamos una versión de Python 100% compatible y estable
FROM python:3.11-slim

# Instala herramientas básicas del sistema
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Configura la carpeta de trabajo interna
WORKDIR /app

# Copia los requerimientos e instala las librerías necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del bot al contenedor
COPY . .

# Expone el puerto de red que exige Render
EXPOSE 10000

# Comando para ejecutar el bot de forma directa
CMD ["python", "main.py"]
