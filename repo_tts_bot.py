import discord
import subprocess
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================
#   CONFIGURACIÓN — edita solo esta sección
# ============================================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIJO = "!"  # Comando: !tts hola mundo
ESPEAK = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
AUDIO_TMP = os.path.join(os.environ["TEMP"], "repo_tts.wav")

# Parámetros de voz (igual que R.E.P.O.)
VOZ_VELOCIDAD = 175  # velocidad
VOZ_TONO = 30  # pitch
VOZ_IDIOMA = "en"  # en = inglés como el juego, es = español
# ============================================

intents = discord.Intents.all()  # <-- CAMBIADO: todos los intents activados
client = discord.Client(intents=intents)


def generar_audio(texto: str) -> bool:
    """Genera WAV con eSpeak igual que Klattersynth"""
    try:
        subprocess.run(
            [
                ESPEAK,
                "-v",
                VOZ_IDIOMA,
                "-s",
                str(VOZ_VELOCIDAD),
                "-p",
                str(VOZ_TONO),
                "-w",
                AUDIO_TMP,
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
    print(f"✅ Bot conectado como {client.user}")
    print(f"   Servidores: {[g.name for g in client.guilds]}")
    print(f"   Usa {PREFIJO}tts <texto> en cualquier canal de texto")
    print(f"   Usa {PREFIJO}unirse para que el bot entre a tu canal de voz")
    print(f"   Usa {PREFIJO}salir para que el bot se desconecte")


@client.event
async def on_message(message):
    print(
        f"📨 Mensaje recibido: '{message.content}' de {message.author} en #{message.channel}"
    )

    if message.author == client.user:
        return

    # !unirse — entra al canal de voz del usuario
    if message.content.strip() == f"{PREFIJO}unirse":
        if message.author.voice:
            canal = message.author.voice.channel
            await canal.connect()
            await message.channel.send(f"🔊 Conectado a **{canal.name}**")
        else:
            await message.channel.send("❌ Debes estar en un canal de voz primero.")

    # !salir — sale del canal de voz
    elif message.content.strip() == f"{PREFIJO}salir":
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send("👋 Desconectado.")

    # !tts <texto> — genera y reproduce la voz de R.E.P.O.
    elif message.content.startswith(f"{PREFIJO}tts "):
        texto = message.content[len(f"{PREFIJO}tts ") :]
        vc = message.guild.voice_client

        if not vc:
            if message.author.voice:
                vc = await message.author.voice.channel.connect()
            else:
                await message.channel.send(
                    "❌ Únete a un canal de voz primero o usa `!unirse`."
                )
                return

        if vc.is_playing():
            vc.stop()

        if generar_audio(texto):
            vc.play(discord.FFmpegPCMAudio(AUDIO_TMP))
            await message.add_reaction("🤖")
        else:
            await message.channel.send("❌ Error generando audio.")


client.run(TOKEN)
