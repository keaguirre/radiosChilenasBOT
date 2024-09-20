#pip install discord.py
#pip install python-dotenv
#pip install PyNaCl
#sudo apt install ffmpeg
#pyinstaller bot.spec para generar el portable
import subprocess
import sys
import time
import discord
from discord.ext import commands
intents = discord.Intents.all()  # Obtiene los intentos predeterminados
intents.typing = False
intents.presences = False
intents.messages = True  # Agrega el intento de mensajes

from typing import Final
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

permissions_integer=4947805613120
bot = commands.Bot(command_prefix='!', intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Definir función para instalar ffmpeg
def install_ffmpeg():
    try:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)
        print('FFmpeg installed successfully')
        return True  # ffmpeg is installed
    except subprocess.CalledProcessError:
        print("Failed to install FFmpeg")
        return False  # Failed to install ffmpeg

if DISCORD_TOKEN and install_ffmpeg():
    # Diccionario de nombres de URLs
    URLs = {
        'adn': 'https://15723.live.streamtheworld.com/ADN_SC',
        '40-principales': 'https://21223.live.streamtheworld.com/LOS40_SC',
        'activa': 'https://playerservices.streamtheworld.com/api/livestream-redirect/ACTIVA_SC',
        'biobio': 'http://unlimited3-cl.dps.live/biobiovalparaiso/mp3/icecast.audio',
        'cooperativa': 'http://redirector.dps.live/cooperativafm/mp3/icecast.audio',
        'corazon': 'https://27443.live.streamtheworld.com/CORAZON_SC',
        'futuro': 'http://uplink.duplexfx.com:8008',
        'ok': 'http://streaming.fmokey.cl/FmOkLS.mp3',
        'futuro2': 'https://playerservices.streamtheworld.com/api/livestream-redirect/FUTURO_SC',
        'imagina': 'https://playerservices.streamtheworld.com/api/livestream-redirect/IMAGINA_SC',
        'la-retro': 'https://s2.radio.co/s9ecef4f68/',
        '40-Principales2': 'https://playerservices.streamtheworld.com/api/livestream-redirect/LOS40_CHILE_SC',
        'puduwel': 'https://playerservices.streamtheworld.com/api/livestream-redirect/PUDAHUEL_SC',
        'rockandpop': 'https://playerservices.streamtheworld.com/api/livestream-redirect/ROCK_AND_POP_SC',
    }
    comandos_conocidos = '!transmitir\n!listar_radios\n!desconectar\n!listar_comandos'

    @bot.event
    async def on_ready():
        print(f'Bot conectado como {bot.user}')

    @bot.command()
    async def transmitir(ctx, nombre_url: str):
        url = URLs.get(nombre_url.lower())
        if url is None:
            embed = discord.Embed(title="Nombre de la radio no válido.❌", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        voice_channel = ctx.author.voice.channel
        if not voice_channel:
            embed = discord.Embed(title="Debes estar en un canal de voz para usar este comando.🗿", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Obtener el cliente de voz asociado al servidor donde se emitió el comando
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected() and voice_client.channel == voice_channel:
            # El bot ya está en el canal de voz solicitado, no es necesario conectar de nuevo
            voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(url))
            embed = discord.Embed(title=f"Transmitiendo radio {nombre_url} 📻", color=discord.Color.random())
            button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Desconectar radio📻", custom_id="desconectar")
            view = discord.ui.View()
            view.add_item(button)
            await ctx.send(embed=embed, view=view)
            return
        # El bot no está en el canal de voz solicitado o está en otro canal, conectarse al nuevo canal
        if voice_client:
            await voice_client.disconnect()

        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(url))
        file = discord.File("Assets/radio.png", filename="radio.png")
        embed = discord.Embed(title=f"Transmitiendo radio {nombre_url} 📻", color=discord.Color.random())
        embed.set_image(url="attachment://radio.png")
        embed.set_footer(text="Web illustrations by Storyset", icon_url=None)
        button = discord.Button(style=discord.ButtonStyle.red, label="Desconectar radio📻")
        # Enviar el mensaje con el embed
        message = await ctx.send(embed=embed)
        await ctx.send(embed=embed, file=file)
        # # Agregar el botón al mensaje
        # await message.add_components(button)
        # # Esperar la interacción del usuario con el botón
        # interaction = await bot.wait_for("button_click", check=lambda i: i.component == button)
        # # Verificar si la interacción se refiere al botón correcto
        # if interaction.component == button:
        #     # Insertar aquí la lógica para desconectar al bot del canal de voz
        #     await interaction.response.send_message("Ejecutando comando !desconectar")


    @bot.command()
    async def listar_radios(ctx):
        embed_content = ""
        for nombre, url in URLs.items():
            embed_content += f"• {nombre}\n"
        embed = discord.Embed(title="Lista de Radios:", description=embed_content, color=discord.Color.random())
        await ctx.send(embed=embed)

    @bot.command()
    async def desconectar(ctx):
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client:
            embed = discord.Embed(title="Bai", color=discord.Color.random())
            await ctx.send(embed=embed)
            await voice_client.disconnect()
        else:
            embed = discord.Embed(title="El bot no está conectado a un canal de voz. 🟡", color=discord.Color.random())
            await ctx.send(embed=embed)

    #Events
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title=f"No se encontró el comando.", description=f"¿Quisiste decir alguno de estos?\n\n{comandos_conocidos}", color=discord.Color.random())
            await ctx.send(embed=embed)

    @bot.command()
    async def listar_comandos(ctx):
        embed = discord.Embed(title="Lista de Comandos:", description=comandos_conocidos, color=discord.Color.random())
        await ctx.send(embed=embed)

    async def detener_bot(bot):
        await bot.close()

    bot.run(DISCORD_TOKEN)

else:
    if DISCORD_TOKEN is None:
        def mostrar_mensaje():
            print("Error\n", "No se pudo encontrar el token. Verifica la clave secreta.")
            time.sleep(5)
            sys.exit()

        mostrar_mensaje()
