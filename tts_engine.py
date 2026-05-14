import os
import subprocess
import tempfile

ESPEAK = os.getenv("ESPEAK_PATH", "espeak-ng")

# eSpeak params ajustados para Klattersynth / R.E.P.O.
_VOICE     = "en"
_SPEED     = 155
_PITCH     = 28
_AMPLITUDE = 80

# Pipeline FFmpeg para la calidad robótica/digital:
# - highpass: elimina ruido grave < 250 Hz
# - equalizer: +5 dB a 1200 Hz (presencia de voz)
# - aecho: eco cortísimo de 10 ms = "buzz" digital sin reverb audible
_FILTER = "highpass=f=250,equalizer=f=1200:width_type=o:width=2:g=5,aecho=0.6:0.6:10:0.25"


def synthesize(text: str, output_path: str) -> bool:
    """
    Genera un WAV procesado replicando la voz Klattersynth de R.E.P.O.
    Paso 1: eSpeak genera la síntesis formante base (ya robótica).
    Paso 2: FFmpeg aplica filtrado de presencia + eco digital.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        raw_path = tmp.name

    try:
        subprocess.run(
            [ESPEAK, "-v", _VOICE, "-s", str(_SPEED), "-p", str(_PITCH),
             "-a", str(_AMPLITUDE), "-w", raw_path, text],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-i", raw_path, "-af", _FILTER, output_path],
            check=True, capture_output=True,
        )
        return True

    except subprocess.CalledProcessError:
        return False

    finally:
        if os.path.exists(raw_path):
            os.unlink(raw_path)
