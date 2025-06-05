# Feria_vlc - Informe Final del Proyecto
Sistema de gestión de eventos para Feria Valencia

## 1. Objetivos del Proyecto
- Desarrollar un sistema integral de gestión de eventos para Feria Valencia
- Implementar un sistema de comunicación efectivo con los asistentes
- Crear una plataforma de encuestas y feedback
- Automatizar procesos de envío de boletines informativos
- Facilitar la gestión de actividades y participantes
- Asegurar la calidad mediante pruebas automatizadas

## 2. Análisis y Público Objetivo

### 2.1 Segmentación del Público
- Rango de edad: 16-60 años
- Intereses: cómic, manga, ilustración, cultura pop, cosplay, juegos de mesa y rol
- Perfil: desde nuevos aficionados hasta seguidores consolidados

### 2.2 Análisis DAFO
![DAFO y competencia](./Imagenes/salon_comic/dafo.png)

## 3. Diseño y Justificación

### 3.1 Arquitectura del Sistema
El proyecto se estructura en varios componentes principales:
- Sistema de gestión de base de datos (SQL)
- Scripts de automatización (Python)
- Plantillas de correo (MJML/HTML)
- Interfaces de lanzamiento (PowerShell/Bash)

### 3.2 Diseño Visual
#### Boletín Informativo
![](./Imagenes/salon_comic/mockup.png)

#### Elementos de Diseño
- **Encabezado**: Identidad visual del evento
- **CTAs**: Botones verdes destacados
- **Contenido**: Estructura clara y escaneable
- **Imágenes**: Apoyo visual estratégico
- **Footer**: Información legal y enlaces de contacto

## 4. Solución Técnica

### 4.1 Estructura de Base de Datos
![](./Imagenes/salon_comic/Diagrama.png)

#### Entidades Principales
1. **Usuarios**: Gestión de participantes
2. **Encuesta**: Sistema de feedback
3. **Actividades**: Eventos y programación
4. **Invitados**: Gestión de ponentes/artistas

### 4.2 Componentes del Sistema
- **Correos.py**: Motor principal de envío de comunicaciones
- **test_correos.py**: Suite de pruebas automatizadas
- **Lanzador.ps1/sh**: Interfaces de control multiplataforma
- **Plantillas MJML**: Diseños responsivos de correo

## 5. Testing y Control de Calidad

### 5.1 Pruebas Automatizadas
- Test de creación de usuarios
- Validación de suscripción a actividades
- Verificación de creación de encuestas
- Pruebas de transacciones de base de datos
- Limpieza automática de datos de prueba

### 5.2 Gestión de Errores
- Sistema robusto de manejo de excepciones
- Logging detallado de operaciones
- Retroalimentación clara al usuario
- Transacciones seguras en base de datos

## 6. Integración con Redes y Sistemas

### 6.1 Comunicaciones
- Integración con servidores SMTP
- Sistema de plantillas HTML responsivas
- Conversión automática MJML a HTML
- Gestión de listas de distribución

### 6.2 Multiplataforma
- Soporte para Windows y Linux
- Scripts de lanzamiento adaptados
- Gestión de dependencias automatizada
- Compatibilidad con diferentes entornos

## 7. Conclusiones y Mejoras Futuras

### 7.1 Logros Alcanzados
- Sistema robusto de gestión de eventos
- Automatización efectiva de comunicaciones
- Testing comprehensivo
- Soporte multiplataforma

### 7.2 Áreas de Mejora
- Implementación de una interfaz web administrativa
- Integración con más plataformas de redes sociales
- Sistema de análisis de datos de encuestas
- Automatización adicional de procesos
- Expansión de la suite de pruebas
- Mejoras en la personalización de comunicaciones

### 7.3 Próximos Pasos
- Desarrollo de API REST
- Implementación de dashboard analítico
- Integración con sistemas de ticketing
- Mejoras en la seguridad y encriptación
- Optimización del rendimiento de la base de datos

