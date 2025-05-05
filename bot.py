
import os
import sys
import discord
import threading
import tkinter as tk
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Determinar la ruta base
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Ruta al ejecutable de ffmpeg
ffmpeg_executable = 'ffmpeg'

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

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    print("No se proporcionó un token de Discord en el archivo .env.")
    sys.exit(1)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Esperando"))

# Definir la vista para el botón de desconexión
class DesconectarView(discord.ui.View):
    @discord.ui.button(label="Desconectar radio📻", style=discord.ButtonStyle.red)
    async def desconectar_radio(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await bot.change_presence(activity=discord.Game(name="Esperando"))
            await interaction.response.send_message("Radio desconectada.🔌", ephemeral=True)
        else:
            await interaction.response.send_message("El bot no está conectado a un canal de voz. 🟡", ephemeral=True)

@bot.command()
async def transmitir(ctx, nombre_url: str):
    url = URLs.get(nombre_url.lower())
    if url is None:
        embed = discord.Embed(title="Nombre de la radio no válido.❌", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if not ctx.author.voice or not ctx.author.voice.channel:
        embed = discord.Embed(title="Debes estar en un canal de voz para usar este comando.🗿", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(voice_channel)
        else:
            voice_client = await voice_channel.connect()

        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(url, executable=ffmpeg_executable), after=lambda e: print(f'Player error: {e}') if e else None)

        embed = discord.Embed(title=f"Transmitiendo radio {nombre_url} 📻", color=discord.Color.random())
        view = DesconectarView()
        await ctx.send(embed=embed, view=view)

        # Cambiar el estado del bot para reflejar que está transmitiendo la radio
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"Radio {nombre_url}"
        ))

    except discord.ClientException as e:
        print(f"Error de cliente de Discord al reproducir: {e}")
        embed = discord.Embed(title="Error al iniciar la transmisión de audio. ⚠️", description=f"Detalles: {e}", color=discord.Color.orange())
        await ctx.send(embed=embed)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await bot.change_presence(activity=discord.Game(name="Esperando"))
    except Exception as e:
        print(f"Otro error al reproducir audio: {e}")
        embed = discord.Embed(title="Ocurrió un error inesperado al transmitir. ❌", description=f"Detalles: {e}", color=discord.Color.red())
        await ctx.send(embed=embed)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await bot.change_presence(activity=discord.Game(name="Esperando"))

@bot.command()
async def listar_radios(ctx):
    embed_content = "\n".join(f"• {nombre}" for nombre in URLs.keys())
    embed = discord.Embed(title="Lista de Radios:", description=embed_content, color=discord.Color.random())
    await ctx.send(embed=embed)

@bot.command()
async def desconectar(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop() # Detener la reproducción antes de desconectar
    if voice_client and voice_client.is_connected():
        embed = discord.Embed(title="Desconectando...", color=discord.Color.random())
        await ctx.send(embed=embed)
        await bot.change_presence(activity=discord.Game(name="Esperando"))
        await voice_client.disconnect()
    else:
        embed = discord.Embed(title="El bot no está conectado a un canal de voz. 🟡", color=discord.Color.random())
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="No se encontró el comando.",
            description=f"¿Quisiste decir alguno de estos?\n\n{comandos_conocidos}",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

@bot.command()
async def listar_comandos(ctx):
    embed = discord.Embed(title="Lista de Comandos:", description=comandos_conocidos, color=discord.Color.random())
    await ctx.send(embed=embed)

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("Bot detenido manualmente")