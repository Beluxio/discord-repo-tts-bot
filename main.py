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
