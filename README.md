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

- Run container:
    - docker run -p 5000:5000 --name radio-container radio-bot


# AZ Function

Flujo Revisado usando Azure Functions

    Web Estática:
        La página web estática envía una solicitud POST a una Azure Function con el comando (start o stop).

    Azure Function:
        Recibe la solicitud POST.
        Usa Azure SDK o Azure CLI para iniciar o detener el contenedor del bot de Discord.
        Obtiene el token de Discord desde Azure Key Vault.

Implementación de Azure Function
## 1.  Crear una Azure Function en Python

Puedes usar el siguiente código para crear una Azure Function que maneje el inicio y la detención del contenedor:

1.1 Instala las herramientas necesarias:
    Asegúrate de tener Azure CLI y las herramientas de Azure Functions instaladas.

1.2 Código de la Azure Function:
    Aquí hay un ejemplo de cómo podría verse el código de la Azure Function en Python: -> az-function.py

## 2. Configuración de Azure Function

Configura las Variables de Entorno:
    Configura las variables de entorno necesarias en tu Azure Function App para AZURE_SUBSCRIPTION_ID, RESOURCE_GROUP, y cualquier otra que necesites.

Despliega la Azure Function:
    Usa Azure CLI o Azure Portal para desplegar la Azure Function.

## 3. AZ CLI bash
### Crear una nueva Azure Function App
az functionapp create --resource-group <nombre_del_grupo_de_recursos> --consumption-plan-location eastus --runtime python --functions-version 3 --name <nombre_de_tu_funcion> --storage-account <nombre_de_tu_cuenta_de_almacenamiento>

### Desplegar el código a la Azure Function
func azure functionapp publish <nombre_de_tu_funcion>

### Resumen del Flujo

1. Web Estática: Envia solicitudes POST a Azure Function con los comandos start o stop.
2. Azure Function: Recibe el comando, obtiene el token de Discord desde Azure Key Vault, y maneja el inicio o la detención del contenedor usando Azure Container Instances.

Este enfoque mantiene toda la lógica dentro del ecosistema de Azure, lo que puede simplificar la configuración y el mantenimiento, además de aprovechar las capacidades serverless para reducir costos cuando el bot no está en uso.

- el function toma los tokens de discord y github desde keyvault y los usa para iniciar y detener el container
Run for docker dev
docker run -p 5000:5000 -i --name radiosChilenasBOT keaguirre/radiosChilenasBOT:latest docker /bin/bash

pip freeze > requirements.txt is a command used in the context of Python programming to generate a file called requirements.txt. This file contains a list of all the installed packages in your Python environment, along with their corresponding versions.