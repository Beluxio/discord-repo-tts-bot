from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="R.E.P.O. TTS API",
    description="""
# 🤖 R.E.P.O. TTS API

API para generar audio con voz robótica inspirada en el juego R.E.P.O.

## ✨ Funcionalidades

- 🔊 Generación de audio TTS
- ⚡ API rápida con FastAPI
- 🐳 Despliegue con Docker
- ☁️ Hospedada en Render
- 🔒 HTTPS automático

## 📌 Endpoints principales

- `/` → Estado del servicio
- `/status` → Información del sistema
- `/docs` → Documentación interactiva
- `/redoc` → Documentación alternativa
- `/saludo/{nombre}` → Endpoint de ejemplo
- `/tts` → Generación de voz (próximamente)
""",
    version="1.0.0",
    contact={
        "name": "Beluxio",
        "url": "https://github.com/Beluxio",
    },
    license_info={
        "name": "MIT License",
    },
)


# Documentación Swagger personalizada
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


# Endpoint raíz
@app.get("/", tags=["General"])
def root():
    return {
        "message": "🚀 API funcionando correctamente",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Estado del servicio
@app.get("/status", tags=["General"])
def status():
    return {
        "status": "online",
        "service": "R.E.P.O. TTS API",
        "version": "1.0.0",
    }


# Endpoint de ejemplo
@app.get("/saludo/{nombre}", tags=["Ejemplos"])
def saludo(nombre: str):
    return {"mensaje": f"Hola {nombre}"}


@app.get("/tts", tags=["TTS"])
def tts(texto: str):
    """
    Genera un archivo WAV con voz robótica estilo R.E.P.O.

    Ejemplo de uso:
    /tts?texto=Hola mundo
    """

    # Ruta del ejecutable de eSpeak NG.
    # En Render/Linux normalmente basta con usar "espeak-ng".
    ESPEAK = os.getenv("ESPEAK_PATH", "espeak-ng")

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        output_path = tmp.name

    try:
        # Generar audio
        subprocess.run(
            [
                ESPEAK,
                "-v",
                "en-us",
                "-s",
                "175",  # velocidad
                "-p",
                "30",  # tono
                "-w",
                output_path,
                texto,
            ],
            check=True,
            capture_output=True,
        )

        # Devolver el archivo al cliente
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="repo_tts.wav",
        )

    except subprocess.CalledProcessError as e:
        return {
            "error": "No se pudo generar el audio",
            "details": e.stderr.decode(errors="ignore"),
        }

    except Exception as e:
        return {
            "error": str(e),
        }
