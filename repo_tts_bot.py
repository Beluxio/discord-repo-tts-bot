import discord
import os
import tempfile

from dotenv import load_dotenv
from tts_engine import synthesize

load_dotenv()

# ============================================
#   CONFIGURACIÓN — edita solo esta sección
# ============================================
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("ERROR: DISCORD_TOKEN no encontrado. Verifica el .env o las variables de entorno.")
    exit(1)

PREFIJO  = "!"
AUDIO_TMP = os.path.join(tempfile.gettempdir(), "repo_tts.wav")
# ============================================

intents = discord.Intents.all()
client  = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    print(f"  Servidores: {[g.name for g in client.guilds]}")
    print(f"  Comandos: {PREFIJO}tts  {PREFIJO}unirse  {PREFIJO}salir")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # !unirse
    if message.content.strip() == f"{PREFIJO}unirse":
        if message.author.voice:
            canal = message.author.voice.channel
            await canal.connect()
            await message.channel.send(f"Conectado a **{canal.name}**")
        else:
            await message.channel.send("Debes estar en un canal de voz primero.")

    # !salir
    elif message.content.strip() == f"{PREFIJO}salir":
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send("Desconectado.")

    # !tts <texto>
    elif message.content.startswith(f"{PREFIJO}tts "):
        texto = message.content[len(f"{PREFIJO}tts "):]
        vc = message.guild.voice_client

        if not vc:
            if message.author.voice:
                vc = await message.author.voice.channel.connect()
            else:
                await message.channel.send(f"Únete a un canal de voz primero o usa `{PREFIJO}unirse`.")
                return

        if vc.is_playing():
            vc.stop()

        if synthesize(texto, AUDIO_TMP):
            vc.play(discord.FFmpegPCMAudio(AUDIO_TMP))
            await message.add_reaction("🤖")
        else:
            await message.channel.send("Error generando audio.")


client.run(TOKEN)
