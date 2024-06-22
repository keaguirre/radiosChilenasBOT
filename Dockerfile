# Usar una imagen base de Python
FROM python:3.12-slim-bullseye

# Establecer un directorio de trabajo
WORKDIR /app

# Instalar git
RUN apt-get update && apt-get install -y git

# Clonar el repositorio de GitHub
RUN git clone https://github.com/keaguirre/radiosChilenasBOT.git .

# Copiar los archivos de requisitos e instalar las dependencias
# Instalar las dependencias directamente desde el repositorio clonado
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Definir el comando para iniciar la aplicación
CMD ["python", "bot.py"]