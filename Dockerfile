# Usar una imagen base de Python
FROM python:3.12-slim-bullseye

# Establecer un directorio de trabajo
WORKDIR /app

# Instalar git y otras dependencias necesarias
RUN apt-get update && apt-get install -y git ffmpeg

# Definir la variable de entorno para el token de GitHub
ARG GITHUB_TOKEN

# Clonar el repositorio de GitHub
RUN git clone https://${GITHUB_TOKEN}@github.com/keaguirre/radiosChilenasBOT.git .

# Eliminar el token después de usarlo para garantizar que no quede en la imagen
RUN unset GITHUB_TOKEN

# Copiar los archivos de requisitos e instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Definir el comando para iniciar la aplicación
CMD ["python", "bot.py"]