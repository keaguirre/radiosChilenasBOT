# Usar una imagen base de Python
FROM python:3.12-slim-bullseye

# Establecer un directorio de trabajo
WORKDIR /app

# Instalar git y otras dependencias necesarias
RUN apt-get update && apt-get install -y git python3-tk ffmpeg

# Clonar el repositorio de GitHub
RUN git clone https://github.com/keaguirre/radiosChilenasBOT .

# Copiar los archivos de requisitos e instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Definir el comando para iniciar la aplicación
CMD ["python", "bot.py"]