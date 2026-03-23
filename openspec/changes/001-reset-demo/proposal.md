# Propuesta: Script de Utilidad reset_demo.py

## Objetivo
Crear un script de utilidad para restablecer el entorno de demostración del proyecto Smart CV Filter, permitiendo una limpieza rápida y controlada de los archivos de datos y salidas.

## Contexto
En el desarrollo y demostración de aplicaciones, es común necesitar un método sencillo para reiniciar el estado inicial de los archivos de trabajo.

## Alcance
- Borrar el archivo de base de datos `src/data/smart_cv.db`
- Vaciar (sin borrar) los directorios:
  * `src/backend/output/RECLUTADOS/`
  * `src/backend/output/DESCARTADOS/`

## Beneficios
- Facilita la reproducibilidad de demostraciones
- Permite reiniciar rápidamente el estado del proyecto
- Proporciona una herramienta de limpieza controlada

## Criterios de Aceptación
- Script implementado en `src/backend/reset_demo.py`
- Imprime mensajes claros de las acciones realizadas
- No requiere parámetros adicionales
- Seguro de ejecutar (no borra directorios, solo su contenido)

## Riesgos
- Pérdida accidental de datos si se ejecuta en entorno de producción
- Necesidad de confirmación antes de la limpieza

## Próximos Pasos
- Implementar el script
- Añadir pruebas unitarias
- Documentar su uso en README