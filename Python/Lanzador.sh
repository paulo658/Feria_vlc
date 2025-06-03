#!/bin/bash

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Obtener la ruta del script
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_PATH/bin/activate"

# Función para convertir MJML a HTML
convert_mjml_to_html() {
    local mjml_file="$1"
    local html_file="$2"
    
    echo -e "${YELLOW}🔄 Convirtiendo $(basename "$mjml_file") a HTML...${NC}"
    if mjml "$mjml_file" -o "$html_file"; then
        echo -e "${GREEN}✅ Conversión exitosa: $(basename "$html_file")${NC}"
        return 0
    else
        echo -e "${RED}❌ Error en la conversión de MJML${NC}"
        return 1
    fi
}

# Función para verificar y convertir archivos si es necesario
verify_and_convert_files() {
    local mjml_path="$SCRIPT_PATH/../MJML"
    local html_path="$SCRIPT_PATH/../HTML"
    
    # Crear directorio HTML si no existe
    mkdir -p "$html_path"
    
    # Verificar cada supuesto
    for supuesto in "supuesto1.mjml" "supuesto2.mjml"; do
        mjml_file="$mjml_path/$supuesto"
        html_file="$html_path/${supuesto%.mjml}.html"
        
        # Si el archivo HTML no existe o es más antiguo que el MJML
        if [ ! -f "$html_file" ] || [ -f "$mjml_file" -a "$mjml_file" -nt "$html_file" ]; then
            if [ -f "$mjml_file" ]; then
                convert_mjml_to_html "$mjml_file" "$html_file" || \
                    echo -e "${YELLOW}⚠️ No se pudo convertir $supuesto${NC}"
            else
                echo -e "${YELLOW}⚠️ No se encontró el archivo MJML: $supuesto${NC}"
            fi
        fi
    done
}

# Función para mostrar el menú
show_menu() {
    clear
    echo -e "${CYAN}================================${NC}"
    echo -e "${YELLOW}🎪 Gestor de Correos Feria VLC 🎪${NC}"
    echo -e "${CYAN}================================${NC}"
    echo -e "1. Enviar correos Salón del Cómic"
    echo -e "2. Enviar correos 2Ruedas"
    echo -e "3. Añadir nuevo usuario"
    echo -e "4. Ejecutar tests"
    echo -e "5. Salir"
    echo -e "${CYAN}================================${NC}"
    echo -e "${GREEN}Por favor, seleccione una opción:${NC}"
}

# Activar entorno virtual
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo -e "${GREEN}✅ Entorno virtual activado correctamente${NC}"
else
    echo -e "${RED}❌ No se encontró el entorno virtual en: $VENV_PATH${NC}"
    exit 1
fi

# Bucle principal del menú
while true; do
    # Verificar y convertir archivos MJML antes de mostrar el menú
    verify_and_convert_files
    
    show_menu
    read -r opcion

    case $opcion in
        1)
            echo -e "${YELLOW}📧 Enviando correos para el Salón del Cómic...${NC}"
            python "$SCRIPT_PATH/Correos.py" 1
            ;;
        2)
            echo -e "${YELLOW}📧 Enviando correos para 2Ruedas...${NC}"
            python "$SCRIPT_PATH/Correos.py" 2
            ;;
        3)
            echo -e "${YELLOW}👤 Añadiendo nuevo usuario...${NC}"
            python "$SCRIPT_PATH/Correos.py" 3
            ;;
        4)
            echo -e "${YELLOW}🧪 Ejecutando tests...${NC}"
            python "$SCRIPT_PATH/test_correos.py" -v
            ;;
        5)
            echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
            deactivate
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción no válida${NC}"
            sleep 2
            continue
            ;;
    esac

    echo -e "\n${CYAN}Presione ENTER para continuar...${NC}"
    read -r
done 
