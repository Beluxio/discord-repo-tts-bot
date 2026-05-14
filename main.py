import os
import pathlib
import tempfile
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from tts_engine import synthesize

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
    Genera un WAV con voz robótica estilo R.E.P.O. (Klattersynth + FFmpeg).

    Ejemplo: `/tts?texto=Hola mundo`
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        output_path = tmp.name

    if synthesize(texto, output_path):
        background_tasks.add_task(os.unlink, output_path)
        return FileResponse(output_path, media_type="audio/wav", filename="repo_tts.wav")

    os.unlink(output_path)
    return {"error": "No se pudo generar el audio"}


# Sirve el frontend React — debe ir al final para no pisar rutas de la API
_frontend_dist = pathlib.Path(__file__).parent / "frontend" / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="frontend")
