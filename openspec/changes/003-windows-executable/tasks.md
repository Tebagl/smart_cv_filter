# Tareas para Empaquetado de Ejecutable de Smart CV Filter

## Preparación del Entorno
- [ ] Instalar dependencias de empaquetado
  * `pip install pyinstaller`
  * `pip install setuptools`
- [ ] Verificar versiones de dependencias
- [ ] Configurar entorno virtual para construcción

## Modificaciones de Código
### 1. Gestión de Rutas
- [ ] Implementar función `get_resource_path()` en `main_gui.py`
- [ ] Modificar importaciones para usar rutas relativas
- [ ] Añadir soporte para `sys._MEIPASS`

### 2. Configuración de Rutas Dinámicas
- [ ] Actualizar `main.py` para usar rutas flexibles
- [ ] Modificar configuración de directorios de entrada/salida
- [ ] Añadir fallback para rutas de recursos

## Empaquetado
### 1. Configuración de PyInstaller
- [ ] Crear archivo de especificación de PyInstaller
- [ ] Configurar parámetros de construcción
  * `--onefile`
  * `--noconsole`
  * Inclusión de recursos adicionales
- [ ] Añadir hidden imports para dependencias
- [ ] Configurar exclusión de módulos no necesarios

### 2. Gestión de Dependencias
- [ ] Verificar inclusión de:
  * customtkinter
  * google-generativeai
  * sqlalchemy
  * spacy
  * pillow
  * python-dotenv
- [ ] Añadir archivos de modelo de spaCy
- [ ] Gestionar dependencias binarias

## Pruebas
### 1. Pruebas de Empaquetado
- [ ] Construir ejecutable
- [ ] Probar en diferentes versiones de Windows
- [ ] Verificar funcionamiento de GUI
- [ ] Probar reset de demo
- [ ] Validar gestión de rutas de archivos
- [ ] Comprobar rendimiento del ejecutable

### 2. Pruebas de Compatibilidad
- [ ] Probar en Windows 10
- [ ] Probar en Windows 11
- [ ] Verificar en diferentes configuraciones de sistema

## Documentación
- [ ] Actualizar README con instrucciones de instalación
- [ ] Añadir notas de versión
- [ ] Documentar requisitos del sistema

## Distribución
- [ ] Crear directorio de distribución
- [ ] Generar ejecutable final
- [ ] Comprimir ejecutable
- [ ] Preparar documentación de instalación

## Criterios de Finalización
- [ ] Ejecutable funcional
- [ ] Todas las funcionalidades operativas
- [ ] Pruebas de compatibilidad completadas
- [ ] Documentación actualizada

## Estimación de Esfuerzo
- Preparación del entorno: 1 hora
- Modificaciones de código: 2-3 horas
- Empaquetado y configuración: 2 horas
- Pruebas: 3-4 horas
- Documentación: 1 hora

## Dependencias Externas
- PyInstaller
- Dependencias del proyecto
- Entorno Windows

## Notas Adicionales
- Mantener compatibilidad con versiones anteriores
- Minimizar tamaño del ejecutable
- Asegurar rendimiento óptimo