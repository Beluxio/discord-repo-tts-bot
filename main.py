import os
import pathlib
import subprocess
import tempfile
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="R.E.P.O. TTS API",
    description="""
# R.E.P.O. TTS API

API para generar audio con voz robótica inspirada en el juego R.E.P.O.

## Endpoints

- `/tts` → Genera WAV con voz estilo Klattersynth
- `/status` → Estado del servicio
- `/docs` → Documentación interactiva
""",
    version="1.0.0",
    contact={"name": "Beluxio", "url": "https://github.com/Beluxio"},
    license_info={"name": "MIT License"},
)

ESPEAK = os.getenv("ESPEAK_PATH", "espeak-ng")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="R.E.P.O. TTS API Docs",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "list",
            "displayRequestDuration": True,
            "filter": True,
            "syntaxHighlight.theme": "monokai",
        },
    )


@app.get("/status", tags=["General"])
def status():
    return {"status": "online", "service": "R.E.P.O. TTS API", "version": "1.0.0"}


@app.get("/saludo/{nombre}", tags=["Ejemplos"])
def saludo(nombre: str):
    return {"mensaje": f"Hola {nombre}"}


@app.get("/tts", tags=["TTS"])
def tts(texto: str, background_tasks: BackgroundTasks):
    """
    Genera un archivo WAV con voz robótica estilo R.E.P.O. (Klattersynth).

    Ejemplo: `/tts?texto=Hola mundo`
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        output_path = tmp.name

    try:
        subprocess.run(
            [ESPEAK, "-v", "en", "-s", "160", "-p", "25", "-a", "80", "-w", output_path, texto],
            check=True,
            capture_output=True,
        )
        background_tasks.add_task(os.unlink, output_path)
        return FileResponse(output_path, media_type="audio/wav", filename="repo_tts.wav")

    except subprocess.CalledProcessError as e:
        os.unlink(output_path)
        return {"error": "No se pudo generar el audio", "details": e.stderr.decode(errors="ignore")}

    except Exception as e:
        os.unlink(output_path)
        return {"error": str(e)}


# Serve the React frontend — must be mounted LAST so API routes take precedence
_frontend_dist = pathlib.Path(__file__).parent / "frontend" / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="frontend")
