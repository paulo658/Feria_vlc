#!/bin/bash

set -e  # Sal si algo falla

# Rutas relativas desde el script
readonly RUTA_SCRIPT="$(dirname "$(readlink -f "$0")")"
readonly MJML_FILE="$RUTA_SCRIPT/../MJML/supuesto1.mjml"
readonly HTML_FILE="$RUTA_SCRIPT/../HTML/supuesto1.html"
readonly VENV_DIR="$(dirname "$RUTA_SCRIPT")/Python"

# Compilar MJML a HTML
echo "🧪 Compilando MJML..."
mjml "$MJML_FILE" -o "$HTML_FILE"

# Activar entorno virtual y ejecutar script Python
echo "🚀 Activando entorno virtual y ejecutando Correos.py..."
source "$VENV_DIR/bin/activate"
python "$RUTA_SCRIPT/Correos.py"
