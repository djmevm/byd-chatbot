# Chatbot Concesionario BYD 🚗

Chatbot de ventas para Concesionario BYD construido con Rasa 3.6.

## Requisitos
- Python 3.10
- pip

## Instalación local

```bash
cd byd-chatbot
pip install -r requirements.txt
rasa train
```

## Ejecutar localmente

Terminal 1 - Servidor de acciones:
```bash
rasa run actions
```

Terminal 2 - Servidor Rasa:
```bash
rasa run --enable-api --cors "*"
```

O para probar en consola:
```bash
rasa shell
```

## Deploy en Railway

1. Conecta tu repo de GitHub en [railway.app](https://railway.app)
2. Agrega la variable de entorno `PORT` (Railway la asigna automáticamente)
3. El archivo `railway.toml` configura el build y deploy automáticamente

## Variables de entorno para GitHub Actions

Agrega en tu repo GitHub → Settings → Secrets:
- `RAILWAY_TOKEN`: tu token de Railway

## Capacidades del chatbot

- Mostrar catálogo completo de modelos BYD
- Información detallada por modelo (precio, autonomía, características)
- Cálculo de financiamiento estimado
- Agendar prueba de manejo
- Negociación y captura de leads
- Manejo de preguntas fuera de tema
