#!/bin/bash

set -e  # Corta si algo falla

# ------------------- 🔧 CONFIGURACIÓN -------------------

readonly RUTA_SCRIPT="$(dirname "$(readlink -f "$0")")"
readonly VENV_DIR="$(dirname "$RUTA_SCRIPT")/Python"

echo "🔍 Verificando entorno..."

# ------------------- 🐍 PYTHON & VENV -------------------

# Instalar venv si hace falta
if ! dpkg -s python3.12-venv >/dev/null 2>&1; then
    echo "📦 Instalando python3.12-venv..."
    sudo apt update
    sudo apt install -y python3.12-venv
fi

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creando entorno virtual en $VENV_DIR..."
    python3.12 -m venv "$VENV_DIR"
fi

# Activar entorno virtual temporalmente en subshell
(
    echo "✅ Activando entorno virtual temporalmente..."
    source "$VENV_DIR/bin/activate"

    # Instalar conector MySQL si no está
    if ! pip show mysql-connector-python >/dev/null 2>&1; then
        echo "🔌 Instalando mysql-connector-python..."
        pip install --upgrade pip
        pip install mysql-connector-python
    fi
)

# ------------------- 🧪 NODE + MJML -------------------

echo "🌐 Instalando Node.js LTS y MJML..."

# Instalar Node.js LTS
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Instalar compilador MJML globalmente
sudo npm install -g mjml

# ------------------- ✅ FIN -------------------

echo "🚀 Entorno completo y listo"
echo "🐍 Python listo en: $VENV_DIR"
echo "📧 MJML disponible con el comando: mjml"

