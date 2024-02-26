# Radios Chilenas Discord BOT

## Descripción

Este repositorio contiene el código fuente de un bot de Discord desarrollado en Python utilizando la biblioteca `discord.py`. El bot está diseñado para proporcionar funcionalidades específicas dentro de un servidor de Discord, como reproducir audio, administrar mensajes y ejecutar comandos personalizados.

### Características principales

- **Reproducción de audio desde URLs:** El bot puede unirse a un canal de voz y reproducir audio desde URLs proporcionadas por los usuarios.

## Tecnologías utilizadas

- **Python:** El bot está desarrollado principalmente en Python, aprovechando las capacidades de la biblioteca `discord.py` para interactuar con la API de Discord.

- **discord.py:** Biblioteca de Python utilizada para interactuar con la API de Discord y desarrollar bots de Discord.

## Instalación y Uso
- python3 -m venv env
- pip install -r requirements.txt
- Adicional deberás instalar el paquete ffmpeg
    - Windows: Descarga el paquete de ffmpeg desde el sitio web oficial: [https://ffmpeg.org/](https://ffmpeg.org/).
    - Linux: https://ffmpeg.org/download.html#build-linux o <code>sudo apt install ffmpeg</code> para debian

# To do's
- idea: limit 15 psswd tries, 15+ added to blacklist microservice flask with sqlite3
- Add sleep-time to read the msg before the cli exit cuz password failed
- Agregar GH Actions para que compile en cada push (pyinstaller -F -n bot.exe -c bot.py desde win)
- Falta fixear que ponga la img en el embed
- Agregar boton desconectar al embed de transmitiendo
- Sugerencias al escribir los comandos - debo cambiarme del '!' al '/'?
- Falta afinar las pruebas unitarias para que el proceso termine exitosamente.

### Setting the env
- python -m venv env
- win: env\Scripts\activate linux: source/bin/activate
- pip install -r requirements.txt
- Update req.txt:
    - pip freeze > requirements.txt
- Compile .exe:
    - pyinstaller -F -n bot.exe -c bot.py
    - pyinstaller --onefile --add-binary "Assets/ffmpeg.exe:." --name "radiosChilenas BOT" --icon "Assets/icon.ico" bot.py
    - pyinstaller --onefile --name "radiosChilenasBOT" --icon "Assets/icon.ico" bot.py