# Radios Chilenas Discord BOT

## Descripción

Este repositorio contiene el código fuente de un bot de Discord desarrollado en Python utilizando la biblioteca `discord.py`. El bot está diseñado para proporcionar funcionalidades específicas dentro de un servidor de Discord, como reproducir audio, administrar mensajes y ejecutar comandos personalizados.

### Características principales

- **Reproducción de audio desde URLs:** El bot puede unirse a un canal de voz y reproducir audio desde URLs proporcionadas por los usuarios.

## Tecnologías utilizadas

- **Python:** El bot está desarrollado principalmente en Python, aprovechando las capacidades de la biblioteca `discord.py` para interactuar con la API de Discord usando ffmpeg.

- **discord.py:** Biblioteca de Python utilizada para interactuar con la API de Discord y desarrollar bots de Discord.

## Instalación y Uso
- python3 -m venv env
- pip install -r requirements.txt
- Adicional deberás instalar el paquete ffmpeg
    - Windows: Descarga el paquete de ffmpeg desde el sitio web oficial: [https://ffmpeg.org/](https://ffmpeg.org/).
    - Linux: https://ffmpeg.org/download.html#build-linux o <code>sudo apt install ffmpeg</code> para debian

### Setting the env
- python -m venv env
- win: env\Scripts\activate linux: source/bin/activate
- pip install -r requirements.txt
- Update req.txt:
    - pip freeze > requirements.txt

- Build a docker image:
    - docker build -t radio-bot .
    
- Run container:
    - docker run -p 5000:5000 --name radio-container radio-bot
    
- Test container:
    - docker run --name [container-name] -a stdin -a stdout -t -i python:3.12-slim-bullseye /bin/bash