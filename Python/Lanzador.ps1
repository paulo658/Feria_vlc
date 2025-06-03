# Configuración inicial
$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "Gestor de Correos Feria VLC"

# Obtener la ruta del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $scriptPath "Scripts\activate.ps1"

# Función para convertir MJML a HTML
function Convert-MjmlToHtml {
    param (
        [string]$mjmlFile,
        [string]$htmlFile
    )
    
    try {
        Write-Host "🔄 Convirtiendo $mjmlFile a HTML..." -ForegroundColor Yellow
        mjml $mjmlFile -o $htmlFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Conversión exitosa: $htmlFile" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Error en la conversión de MJML" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
        return $false
    }
}

# Función para verificar y convertir archivos si es necesario
function Verify-AndConvertFiles {
    $mjmlPath = Join-Path $scriptPath "..\MJML"
    $htmlPath = Join-Path $scriptPath "..\HTML"
    
    # Crear directorio HTML si no existe
    if (-not (Test-Path $htmlPath)) {
        New-Item -ItemType Directory -Path $htmlPath | Out-Null
    }
    
    # Verificar cada supuesto
    $supuestos = @("supuesto1.mjml", "supuesto2.mjml")
    foreach ($supuesto in $supuestos) {
        $mjmlFile = Join-Path $mjmlPath $supuesto
        $htmlFile = Join-Path $htmlPath ($supuesto -replace "\.mjml$", ".html")
        
        # Si el archivo HTML no existe o es más antiguo que el MJML
        if (-not (Test-Path $htmlFile) -or 
            (Test-Path $mjmlFile -and (Get-Item $mjmlFile).LastWriteTime -gt (Get-Item $htmlFile).LastWriteTime)) {
            if (Test-Path $mjmlFile) {
                if (-not (Convert-MjmlToHtml -mjmlFile $mjmlFile -htmlFile $htmlFile)) {
                    Write-Host "⚠️ No se pudo convertir $supuesto" -ForegroundColor Yellow
                    continue
                }
            }
            else {
                Write-Host "⚠️ No se encontró el archivo MJML: $supuesto" -ForegroundColor Yellow
            }
        }
    }
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
        $process = Start-Process python -ArgumentList "$pythonPath $Arguments" -NoNewWindow -Wait -PassThru
        if ($process.ExitCode -ne 0) {
            Write-Host "❌ Error ejecutando el script Python" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
}

# Activar entorno virtual
try {
    if (Test-Path $venvPath) {
        . $venvPath
        Write-Host "✅ Entorno virtual activado correctamente" -ForegroundColor Green
    }
    else {
        Write-Host "❌ No se encontró el entorno virtual en: $venvPath" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error activando el entorno virtual: $_" -ForegroundColor Red
    exit 1
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
            deactivate
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