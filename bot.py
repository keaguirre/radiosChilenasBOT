#pip install discord.py
#pip install python-dotenv
#pip install PyNaCl
#sudo apt install ffmpeg
import discord
from discord.ext import commands

intents = discord.Intents.all()  # Obtiene los intentos predeterminados
intents.typing = False
intents.presences = False
intents.messages = True  # Agrega el intento de mensajes

from typing import Final
import os
from dotenv import load_dotenv

permissions_integer=4947805613120
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv('TOKEN')

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
    'puduwel': 'https://playerservices.streamtheworld.com/api/livestream-redirect/PUDAHUEL_SCS',
    'rockandpop': 'https://playerservices.streamtheworld.com/api/livestream-redirect/ROCK_AND_POP_SC',
}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def transmitir(ctx, nombre_url: str):
    url = URLs.get(nombre_url.lower())
    if url is None:
        await ctx.send("Nombre de la radio no válido.❌")
        return
    
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(url))
    else:
        await ctx.send("Debes estar en un canal de voz para usar este comando.🗿")

@bot.command()
async def listar_radios(ctx):
    await ctx.send("Lista de Radios:")
    for nombre, url in URLs.items():
        await ctx.send(f"{nombre}")

@bot.command()
async def calabaza(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
    else:
        await ctx.send("El bot no está conectado a un canal de voz.🟡")

bot.run(TOKEN)