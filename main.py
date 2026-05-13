from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import tempfile

app = FastAPI(title="Repo TTS API")

ESPEAK = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
VOZ_IDIOMA = "en"
VOZ_VELOCIDAD = 175
VOZ_TONO = 30


class TTSRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Repo TTS API funcionando correctamente"}


@app.post("/tts")
def generate_tts(request: TTSRequest):
    output_file = os.path.join(tempfile.gettempdir(), "repo_api_tts.wav")

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
            output_file,
            request.text,
        ],
        check=True,
    )

    return FileResponse(output_file, media_type="audio/wav", filename="repo_tts.wav")
