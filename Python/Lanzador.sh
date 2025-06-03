#!/bin/bash

# Configuración inicial
set -e  # Sal si algo falla

# Rutas relativas desde el script
readonly RUTA_SCRIPT="$(dirname "$(readlink -f "$0")")"
readonly VENV_DIR="$(dirname "$RUTA_SCRIPT")/Python"

# Activar entorno virtual
source "$VENV_DIR/bin/activate"

# Función para mostrar el menú
mostrar_menu() {
    clear
    echo "================================"
    echo "🎪 Gestor de Correos Feria VLC 🎪"
    echo "================================"
    echo "1. Enviar correos Salón del Cómic"
    echo "2. Enviar correos 2Ruedas"
    echo "3. Añadir nuevo usuario"
    echo "4. Ejecutar tests"
    echo "5. Salir"
    echo "================================"
    echo "Por favor, seleccione una opción:"
}

# Función para procesar la opción seleccionada
procesar_opcion() {
    case $1 in
        1)
            echo "📧 Enviando correos para el Salón del Cómic..."
            python "$RUTA_SCRIPT/Correos.py" 1
            ;;
        2)
            echo "📧 Enviando correos para 2Ruedas..."
            python "$RUTA_SCRIPT/Correos.py" 2
            ;;
        3)
            echo "👤 Añadiendo nuevo usuario..."
            python "$RUTA_SCRIPT/Correos.py" 3
            ;;
        4)
            echo "🧪 Ejecutando tests..."
            python "$RUTA_SCRIPT/test_correos.py" -v
            ;;
        5)
            echo "👋 ¡Hasta luego!"
            deactivate  # Desactivar el entorno virtual antes de salir
            exit 0
            ;;
        *)
            echo "❌ Opción no válida"
            ;;
    esac
    echo
    echo "Presione Enter para continuar..."
    read -r
}

# Bucle principal
while true; do
    mostrar_menu
    read -r opcion
    procesar_opcion "$opcion"
done 
