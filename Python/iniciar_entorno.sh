#!/bin/bash

set -e  # Corta si algo falla

# Ruta del proyecto y entorno
PROYECTO_DIR="/home/ubuntu/Feria_vlc/Python"
VENV_DIR="$PROYECTO_DIR/venv"

echo "🔍 Verificando entorno..."

# Instalar venv si hace falta
if ! dpkg -s python3.12-venv >/dev/null 2>&1; then
    echo "📦 Instalando python3.12-venv..."
    sudo apt update
    sudo apt install -y python3.12-venv
fi

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creando entorno virtual..."
    python3.12 -m venv "$VENV_DIR"
fi

# Activar entorno virtual
echo "✅ Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# Instalar conector MySQL si no está
if ! pip show mysql-connector-python >/dev/null 2>&1; then
    echo "🔌 Instalando mysql-connector-python..."
    pip install --upgrade pip
    pip install mysql-connector-python
fi

echo "🚀 Todo listo, socio."
echo "👉 Ya podés correr tu script con: python Correos.py"
