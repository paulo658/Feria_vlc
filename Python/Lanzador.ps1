# Configuración inicial
$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "Gestor de Correos Feria VLC"

# Obtener la ruta del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Función para convertir MJML a HTML
function Convertir-MjmlAHtml {
    
    $CarpetaMjml = "../mjml/"
    $CarpetaHtml = "../html/"

    # comprobación de carpeta de destino (../html/)
    if (-not (Test-Path $CarpetaHtml)) {
        New-Item -ItemType Directory -Path $CarpetaHtml | Out-Null
    }

    # se listan los .mjml
    Get-ChildItem -Path $CarpetaMjml -Filter *.mjml | ForEach-Object {
        $ArchivoMjml = $_.FullName
        $ArchivoMjmlSinExt = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        $ArchivoHtml = Join-Path $CarpetaHtml "$ArchivoMjmlSinExt.html"

        # Verificar si necesitamos convertir el archivo
        $NecesitaConversion = $true
        if (Test-Path $ArchivoHtml) {
            $FechaMjml = (Get-Item $ArchivoMjml).LastWriteTime
            $FechaHtml = (Get-Item $ArchivoHtml).LastWriteTime
            if ($FechaMjml -le $FechaHtml) {
                $NecesitaConversion = $false
                Write-Host "El archivo $($_.Name) ya está actualizado" -ForegroundColor Green
            }
        }

        # se convierte el archivo a .html solo si es necesario
        if ($NecesitaConversion) {
            Write-Host "Convirtiendo $($_.Name) a HTML..." -ForegroundColor Cyan
            mjml $ArchivoMjml -o $ArchivoHtml
        }
    }
}

# Función para verificar y convertir archivos si es necesario
function Verify-AndConvertFiles {
    # Ejecutar la conversión de archivos MJML
    Convertir-MjmlAHtml
}

# Función para mostrar el menú con colores
function Show-Menu {
    Clear-Host
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "🎪 Gestor de Correos Feria VLC 🎪" -ForegroundColor Yellow
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "1. Enviar correos Salón del Cómic" -ForegroundColor White
    Write-Host "2. Enviar correos 2Ruedas" -ForegroundColor White
    Write-Host "3. Añadir nuevo usuario" -ForegroundColor White
    Write-Host "4. Ejecutar tests" -ForegroundColor White
    Write-Host "5. Salir" -ForegroundColor White
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "Por favor, seleccione una opción:" -ForegroundColor Green
}

# Función para ejecutar Python con manejo de errores
function Invoke-PythonScript {
    param (
        [string]$Script,
        [string]$Arguments
    )
    
    try {
        $pythonPath = Join-Path $scriptPath $Script
        Write-Host "`nEjecutando: python $Script $Arguments" -ForegroundColor Cyan
        $process = Start-Process python -ArgumentList "$pythonPath $Arguments" -NoNewWindow -Wait -PassThru
        if ($process.ExitCode -ne 0) {
            Write-Host "❌ El script Python terminó con errores (código: $($process.ExitCode))" -ForegroundColor Red
            Write-Host "Presiona Enter para continuar..." -ForegroundColor Yellow
            $null = Read-Host
        }
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
        Write-Host "Presiona Enter para continuar..." -ForegroundColor Yellow
        $null = Read-Host
    }
}

# Bucle principal del menú
while ($true) {
    # Verificar y convertir archivos MJML antes de mostrar el menú
    Verify-AndConvertFiles
    
    Show-Menu
    $opcion = Read-Host ">"

    switch ($opcion) {
        "1" {
            Write-Host "📧 Enviando correos para el Salón del Cómic..." -ForegroundColor Yellow
            Invoke-PythonScript -Script "Correos.py" -Arguments "1"
        }
        "2" {
            Write-Host "📧 Enviando correos para 2Ruedas..." -ForegroundColor Yellow
            Invoke-PythonScript -Script "Correos.py" -Arguments "2"
        }
        "3" {
            Write-Host "👤 Añadiendo nuevo usuario..." -ForegroundColor Yellow
            Invoke-PythonScript -Script "Correos.py" -Arguments "3"
        }
        "4" {
            Write-Host "🧪 Ejecutando tests..." -ForegroundColor Yellow
            Invoke-PythonScript -Script "test_correos.py" -Arguments "-v"
        }
        "5" {
            Write-Host "👋 ¡Hasta luego!" -ForegroundColor Green
            exit 0
        }
        default {
            Write-Host "❌ Opción no válida" -ForegroundColor Red
            Start-Sleep -Seconds 2
            continue
        }
    }

    Write-Host "`nPresione cualquier tecla para continuar..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 