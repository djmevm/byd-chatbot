#!/bin/sh
echo "=== Iniciando servidor de acciones ==="
python -m rasa_sdk --actions actions --port 5055 &
ACTIONS_PID=$!
echo "=== Actions PID: $ACTIONS_PID ==="

sleep 10

echo "=== Verificando si actions server esta corriendo ==="
kill -0 $ACTIONS_PID 2>/dev/null && echo "Actions server OK" || echo "Actions server FALLO"

echo "=== Iniciando Rasa server ==="
exec rasa run --enable-api --cors "*" --port ${PORT:-5005} --endpoints endpoints.yml --model models/byd-model.tar.gz
