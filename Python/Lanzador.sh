#!/bin/bash

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Obtener la ruta del script
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_PATH/venv"
REQUIREMENTS_FILE="$SCRIPT_PATH/requirements.txt"

# Función para crear el entorno virtual
setup_virtual_env() {
    echo -e "${YELLOW}🔄 Configurando entorno virtual...${NC}"
    
    # Verificar si python3-venv está instalado
    if ! dpkg -l | grep -q python3-venv; then
        echo -e "${YELLOW}⚠️ python3-venv no está instalado. Intentando instalar...${NC}"
        sudo apt-get update && sudo apt-get install -y python3-venv
    fi
    
    # Crear entorno virtual si no existe
    if [ ! -d "$VENV_PATH" ]; then
        echo -e "${YELLOW}🔄 Creando nuevo entorno virtual...${NC}"
        python3 -m venv "$VENV_PATH"
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Error creando el entorno virtual${NC}"
            return 1
        fi
    fi
    
    # Activar entorno virtual
    source "$VENV_PATH/bin/activate"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error activando el entorno virtual${NC}"
        return 1
    fi
    
    # Crear requirements.txt si no existe
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo -e "${YELLOW}📝 Creando requirements.txt...${NC}"
        cat > "$REQUIREMENTS_FILE" << EOF
mysql-connector-python==8.0.32
python-dotenv==1.0.0
EOF
    fi
    
    # Instalar dependencias
    echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
    pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error instalando dependencias${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Entorno virtual configurado correctamente${NC}"
    return 0
}

# Función para convertir MJML a HTML
convertir_mjml_a_html() {
    carpeta_mjml="../mjml/"
    carpeta_html="../html/"

    # comprobación de carpeta de destino (../html/)
    if [ ! -d "$carpeta_html" ]; then
        mkdir -p "$carpeta_html"
    fi

    # se listan los .mjml
    for archivo_mjml in "$carpeta_mjml"*.mjml; do
        if [ -f "$archivo_mjml" ]; then
            nombre_base=$(basename "$archivo_mjml" .mjml)
            archivo_html="$carpeta_html$nombre_base.html"

            # Verificar si necesitamos convertir el archivo
            necesita_conversion=true
            if [ -f "$archivo_html" ]; then
                fecha_mjml=$(stat -c %Y "$archivo_mjml")
                fecha_html=$(stat -c %Y "$archivo_html")
                if [ $fecha_mjml -le $fecha_html ]; then
                    necesita_conversion=false
                    echo -e "${GREEN}El archivo $(basename "$archivo_mjml") ya está actualizado${NC}"
                fi
            fi

            # se convierte el archivo a .html solo si es necesario
            if [ "$necesita_conversion" = true ]; then
                echo -e "${CYAN}Convirtiendo $(basename "$archivo_mjml") a HTML...${NC}"
                mjml "$archivo_mjml" -o "$archivo_html"
            fi
        fi
    done
}

# Función para verificar y convertir archivos si es necesario
verify_and_convert_files() {
    # Ejecutar la conversión de archivos MJML
    convertir_mjml_a_html
}

# Función para mostrar el menú
show_menu() {
    clear
    echo -e "${CYAN}================================${NC}"
    echo -e "${YELLOW}🎪 Gestor de Correos Feria VLC 🎪${NC}"
    echo -e "${CYAN}================================${NC}"
    echo -e "${WHITE}1. Enviar correos Salón del Cómic${NC}"
    echo -e "${WHITE}2. Enviar correos 2Ruedas${NC}"
    echo -e "${WHITE}3. Añadir nuevo usuario${NC}"
    echo -e "${WHITE}4. Ejecutar tests${NC}"
    echo -e "${WHITE}5. Salir${NC}"
    echo -e "${CYAN}================================${NC}"
    echo -e "${GREEN}Por favor, seleccione una opción:${NC}"
}

# Función para ejecutar Python con manejo de errores
invoke_python_script() {
    local script="$1"
    local arguments="$2"
    
    echo -e "\n${CYAN}Ejecutando: python $script $arguments${NC}"
    python "$SCRIPT_PATH/$script" "$arguments"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ El script Python terminó con errores (código: $?)${NC}"
        echo -e "${YELLOW}Presiona Enter para continuar...${NC}"
        read
    fi
}

# Configurar entorno virtual
setup_virtual_env
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error en la configuración del entorno virtual${NC}"
    exit 1
fi

# Bucle principal del menú
while true; do
    # Verificar y convertir archivos MJML antes de mostrar el menú
    verify_and_convert_files
    
    show_menu
    read -p ">" opcion

    case $opcion in
        1)
            echo -e "${YELLOW}📧 Enviando correos para el Salón del Cómic...${NC}"
            invoke_python_script "Correos.py" "1"
            ;;
        2)
            echo -e "${YELLOW}📧 Enviando correos para 2Ruedas...${NC}"
            invoke_python_script "Correos.py" "2"
            ;;
        3)
            echo -e "${YELLOW}👤 Añadiendo nuevo usuario...${NC}"
            invoke_python_script "Correos.py" "3"
            ;;
        4)
            echo -e "${YELLOW}🧪 Ejecutando tests...${NC}"
            invoke_python_script "test_correos.py" ""
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
    read
done 
