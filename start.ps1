# Script de inicio del Chatbot BYD
# Libera puertos y levanta los dos servidores

Write-Host "Liberando puertos..." -ForegroundColor Yellow
@(5005, 5055) | ForEach-Object {
    $proc = netstat -ano | findstr ":$_ "
    if ($proc) {
        $pid = $proc.Trim().Split()[-1]
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "Puerto $_ liberado"
    }
}

Start-Sleep -Seconds 2

Write-Host "Iniciando servidor de acciones en puerto 5055..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe -m rasa run actions --port 5055" -WorkingDirectory $PSScriptRoot

Start-Sleep -Seconds 5

Write-Host "Iniciando servidor Rasa en puerto 5005..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe -m rasa run --enable-api --cors '*' --port 5005" -WorkingDirectory $PSScriptRoot

Write-Host ""
Write-Host "Bot iniciando... espera ~30 segundos" -ForegroundColor Green
Write-Host "API disponible en: http://localhost:5005/webhooks/rest/webhook" -ForegroundColor Green
