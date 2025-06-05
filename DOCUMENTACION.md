# Feria_vlc - Documentación del Proyecto
Sistema de Gestión de Correos para Ferias de Valencia

## 1. Estructura del Proyecto

```
Feria_vlc/
├── Python/           # Scripts y lanzadores principales
├── MJML/            # Plantillas de correo electrónico
├── HTML/            # Plantillas HTML generadas
├── SQL/             # Scripts de base de datos
├── Imagenes/        # Recursos visuales
├── Docker/          # Configuración de contenedores
└── Bash/            # Scripts de shell adicionales
```

## 2. Componentes Principales

### 2.1 Sistema de Gestión de Correos (Python/)
- **Correos.py**: Script principal para el envío de correos y gestión de usuarios
  - Funcionalidades:
    - Envío de correos para Salón del Cómic
    - Envío de correos para 2Ruedas
    - Gestión de usuarios
    - Integración con base de datos MySQL

- **Lanzadores**:
  - `Lanzador.ps1`: Script PowerShell para Windows
  - `Lanzador.sh`: Script Bash para sistemas Unix
  - Características:
    - Menú interactivo con colores
    - Conversión automática MJML a HTML
    - Gestión de entorno virtual Python
    - Ejecución de tests

- **Tests**:
  - `test_correos.py`: Suite de pruebas automatizadas
    - test_01_crear_usuario
    - test_02_suscribir_usuario_actividad
    - test_03_crear_encuesta

### 2.2 Plantillas de Correo (MJML/)
- **supuesto1.mjml**: Plantilla para Salón del Cómic
  - Diseño responsivo
  - Elementos visuales optimizados
  - Llamadas a la acción (CTA)

- **supuesto2.mjml**: Plantilla para 2Ruedas
  - Diseño tipo folleto
  - Ancho fijo de 800px
  - Efectos visuales mejorados

### 2.3 Base de Datos (SQL/)
- **Tablas.sql**: Definición de la estructura
  - Usuarios
  - Encuestas
  - Actividades
  - Invitados
  - Relaciones entre tablas

- **Datos.sql**: Datos de ejemplo y prueba
  - Registros iniciales
  - Datos de prueba para desarrollo

## 3. Características Principales

### 3.1 Sistema Multi-plataforma
- Compatibilidad con Windows y Unix
- Scripts de lanzamiento específicos por plataforma
- Gestión automática de dependencias

### 3.2 Gestión de Correos
- Envío automatizado de boletines
- Plantillas personalizables
- Seguimiento de suscripciones

### 3.3 Base de Datos
- Modelo relacional completo
- Gestión de usuarios y actividades
- Sistema de encuestas integrado

### 3.4 Testing
- Suite de pruebas automatizadas
- Verificación de funcionalidades críticas
- Limpieza automática de datos de prueba

## 4. Requisitos Técnicos

### 4.1 Dependencias
- Python 3.x
- MySQL
- MJML
- PowerShell (Windows) o Bash (Unix)

### 4.2 Configuración
- Archivo `pass.inf` para credenciales
- Entorno virtual Python
- Conexión a base de datos MySQL

## 5. Guía de Uso

### 5.1 Instalación
1. Clonar el repositorio
2. Configurar credenciales en `pass.inf`
3. Ejecutar el lanzador correspondiente al sistema

### 5.2 Operaciones Principales
1. Envío de correos
2. Gestión de usuarios
3. Ejecución de tests
4. Conversión de plantillas MJML

### 5.3 Mantenimiento
- Actualización de plantillas
- Gestión de la base de datos
- Ejecución de pruebas periódicas

# Guía de Usuario - Sistema Feria VLC

## Índice
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación](#instalación)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Uso del Sistema](#uso-del-sistema)
5. [Personalización](#personalización)
6. [Solución de Problemas](#solución-de-problemas)

## Requisitos del Sistema

### Software Necesario
- Python 3.8 o superior
- Node.js (para MJML)
- PowerShell 7+ (Windows) o Bash (Linux)
- SQL Server o MySQL

### Dependencias Python
```bash
pip install -r requirements.txt
```

### Dependencias MJML
```bash
npm install -g mjml
```

## Instalación

1. **Clonar el Repositorio**
```bash
git clone [URL_del_repositorio]
cd Feria_vlc
```

2. **Configurar el Entorno**
- Copiar `.env.example` a `.env`
- Actualizar las credenciales de la base de datos y SMTP

3. **Inicializar la Base de Datos**
- Ejecutar los scripts en la carpeta `SQL/`
- Verificar la conexión con la base de datos

## Estructura del Proyecto

```
Feria_vlc/
├── Python/           # Scripts principales
│   ├── Correos.py   # Motor de envío de correos
│   └── test_*.py    # Tests automatizados
├── MJML/            # Plantillas de correo
├── HTML/            # Plantillas convertidas
├── SQL/             # Scripts de base de datos
├── Bash/            # Scripts de shell
└── Docker/          # Configuración de contenedores
```

## Uso del Sistema

### 1. Envío de Correos

#### Windows (PowerShell)
```powershell
./Python/Lanzador.ps1
```

#### Linux/macOS (Bash)
```bash
./Bash/Lanzador.sh
```

### 2. Gestión de Plantillas

#### Modificar Plantillas MJML
1. Editar archivos en `MJML/`
2. Los lanzadores convertirán automáticamente a HTML

#### Conversión Manual MJML a HTML
```bash
mjml MJML/plantilla.mjml -o HTML/plantilla.html
```

### 3. Base de Datos

#### Consultas Principales
- Usuarios: `SQL/usuarios.sql`
- Actividades: `SQL/actividades.sql`
- Encuestas: `SQL/encuestas.sql`

#### Respaldo de Datos
```bash
./Bash/backup.sh
```

## Personalización

### 1. Modificar Plantillas de Correo

#### Estructura MJML Básica
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <!-- Contenido aquí -->
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

#### Variables Disponibles
- `{{nombre}}`: Nombre del usuario
- `{{actividad}}`: Nombre de la actividad
- `{{fecha}}`: Fecha del evento
- `{{link}}`: Enlaces personalizados

### 2. Configurar Nuevas Actividades

1. Insertar en la base de datos:
```sql
INSERT INTO Actividades (nombre, fecha, descripcion)
VALUES ('Nueva Actividad', '2024-12-31', 'Descripción');
```

2. Crear plantilla MJML correspondiente
3. Actualizar configuración en `Python/config.py`

### 3. Personalizar Encuestas

1. Crear nueva encuesta en la base de datos
2. Modificar `Python/Correos.py` para incluir nuevo tipo
3. Actualizar plantillas relacionadas

## Solución de Problemas

### Errores Comunes

1. **Error de Conexión SMTP**
   - Verificar credenciales en `.env`
   - Comprobar configuración del servidor
   - Revisar firewall/puertos

2. **Fallos en Conversión MJML**
   - Verificar instalación de Node.js
   - Reinstalar MJML: `npm install -g mjml`
   - Validar sintaxis MJML

3. **Errores de Base de Datos**
   - Comprobar cadena de conexión
   - Verificar permisos de usuario
   - Revisar logs de SQL

### Logs y Diagnóstico

- Logs de aplicación: `Python/logs/`
- Logs de base de datos: `SQL/logs/`
- Logs de conversión MJML: `MJML/logs/`

### Contacto y Soporte

Para reportar problemas o solicitar ayuda:
1. Abrir un issue en el repositorio
2. Documentar el problema con logs relevantes
3. Describir pasos para reproducir el error

## Notas Adicionales

- Realizar copias de seguridad regularmente
- Mantener actualizadas las dependencias
- Revisar logs periódicamente
- Probar cambios en ambiente de desarrollo

## Actualizaciones y Mantenimiento

### Actualizar el Sistema
```bash
git pull origin main
pip install -r requirements.txt
npm update -g mjml
```

### Mantenimiento Preventivo
1. Limpiar logs antiguos
2. Optimizar base de datos
3. Actualizar plantillas según feedback
4. Revisar rendimiento del sistema 