from fastapi import FastAPI

app = FastAPI(
    title="R.E.P.O. TTS API",
    description="""
# 🤖 R.E.P.O. TTS API

API para generar audio con voz robótica inspirada en el juego R.E.P.O.

## Funcionalidades

- 🔊 Generación de audio TTS
- ⚡ API rápida con FastAPI
- 🐳 Despliegue con Docker
- ☁️ Hospedada en Render
- 🔒 HTTPS automático

## Endpoints principales

- `/` → Estado del servicio
- `/docs` → Documentación interactiva
- `/redoc` → Documentación alternativa
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


@app.get("/", tags=["General"])
def root():
    return {"message": "API funcionando correctamente"}


@app.get("/status", tags=["General"])
def status():
    return {
        "status": "online",
        "service": "R.E.P.O. TTS API",
        "version": "1.0.0",
    }


@app.get("/saludo/{nombre}", tags=["Ejemplos"])
def saludo(nombre: str):
    return {"mensaje": f"Hola {nombre}"}
