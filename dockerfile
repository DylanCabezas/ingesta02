FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios para el contenedor
COPY requirements.txt . 

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente del microservicio de ingesta
COPY . .

# Expone el puerto que la aplicación FastAPI va a usar
EXPOSE 8000

# Ejecuta el contenedor
CMD ["python3", "ingesta.py"]
