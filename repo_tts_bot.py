import discord
import subprocess
import os
import tempfile

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================
#   CONFIGURACIÓN — edita solo esta sección
# ============================================
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("ERROR: DISCORD_TOKEN no encontrado. Verifica el .env o las variables de entorno.")
    exit(1)
PREFIJO = "!"  # Comando: !tts hola mundo
ESPEAK = os.getenv("ESPEAK_PATH", "espeak-ng")
AUDIO_TMP = os.path.join(tempfile.gettempdir(), "repo_tts.wav")
# Parámetros de voz (igual que R.E.P.O. / Klattersynth)
VOZ_VELOCIDAD = 160   # velocidad
VOZ_TONO = 25         # pitch más bajo = más robótico
VOZ_AMPLITUD = 80     # volumen
VOZ_IDIOMA = "en"     # en = inglés exacto del juego
# ============================================

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def generar_audio(texto: str) -> bool:
    """Genera WAV con eSpeak NG replicando la voz Klattersynth de R.E.P.O."""
    try:
        subprocess.run(
            [
                ESPEAK,
                "-v", VOZ_IDIOMA,
                "-s", str(VOZ_VELOCIDAD),
                "-p", str(VOZ_TONO),
                "-a", str(VOZ_AMPLITUD),
                "-w", AUDIO_TMP,
                texto,
            ],
            check=True,
            capture_output=True,
        )
        return True
    except Exception as e:
        print(f"Error generando audio: {e}")
        return False


@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    print(f"  Servidores: {[g.name for g in client.guilds]}")
    print(f"  Usa {PREFIJO}tts <texto> en cualquier canal de texto")
    print(f"  Usa {PREFIJO}unirse para que el bot entre a tu canal de voz")
    print(f"  Usa {PREFIJO}salir para que el bot se desconecte")


@client.event
async def on_message(message):
    print(f"Mensaje recibido: '{message.content}' de {message.author} en #{message.channel}")

    if message.author == client.user:
        return

    # !unirse — entra al canal de voz del usuario
    if message.content.strip() == f"{PREFIJO}unirse":
        if message.author.voice:
            canal = message.author.voice.channel
            await canal.connect()
            await message.channel.send(f"Conectado a **{canal.name}**")
        else:
            await message.channel.send("Debes estar en un canal de voz primero.")

    # !salir — sale del canal de voz
    elif message.content.strip() == f"{PREFIJO}salir":
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send("Desconectado.")

    # !tts <texto> — genera y reproduce la voz de R.E.P.O.
    elif message.content.startswith(f"{PREFIJO}tts "):
        texto = message.content[len(f"{PREFIJO}tts "):]
        vc = message.guild.voice_client

        if not vc:
            if message.author.voice:
                vc = await message.author.voice.channel.connect()
            else:
                await message.channel.send(
                    f"Únete a un canal de voz primero o usa `{PREFIJO}unirse`."
                )
                return

        if vc.is_playing():
            vc.stop()

        if generar_audio(texto):
            vc.play(discord.FFmpegPCMAudio(AUDIO_TMP))
            await message.add_reaction("🤖")
        else:
            await message.channel.send("Error generando audio.")


client.run(TOKEN)
