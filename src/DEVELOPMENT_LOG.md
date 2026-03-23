# DEVELOPMENT_LOG

## Estado del Proyecto
Fase actual: Implementación de Interfaz de Usuario de Escritorio (Módulo 4)

## Especificaciones Técnicas
- **Soporte multiformato**: Extracción de texto desde archivos `.pdf`, `.docx`, `.doc`, `.txt`, `.rtf`. Se debe priorizar el uso de `pdfplumber` para mantener el flujo de lectura adecuado en diseños complejos, especialmente en CVs con formato de 2 columnas.
- **Privacidad y Anonimización (GDPR)**: Antes de enviar o procesar cualquier texto con análisis externo (LLM), el contenido debe ser anonimizado localmente. Esto implica sustituir Nombres, Emails y Números de Teléfono por IDs representativos utilizando librerías locales de NLP como `spacy`.
- **Evaluación Semántica (LLM)**: El motor de análisis no se basará en la búsqueda de palabras clave exactas. Deberá realizar un razonamiento semántico para entender equivalencias profesionales (ej. entender que "Vendedor" es equivalente funcionalmente a "Account Executive").
- **Clasificación y Enrutamiento**: El resultado del sistema debe ser físico. Tras la evaluación, los archivos originales deberán copiarse físicamente a los directorios `./RECLUTADOS/` o `./DESCARTADOS/` según corresponda.

## Registro de Cambios (Changelog)
- [2026-03-20] Documento DEVELOPMENT_LOG.md inicializado.
- [2026-03-20] Módulo 1: UniversalExtractor completado y validad.
- [2026-03-20] Inicio de desarrollo del Módulo 2: LocalAnonymizer.
- [2026-03-20] Módulo 2: LocalAnonymizer completado.
- [2026-03-20] Inicio de Fase de Orquestación (main.py).
- [2026-03-20] Módulo 3: Evaluación Semántica (LLM) añadido e integrado en orquestación.
- [2026-03-23] Mejoras en Módulo de Análisis de CV (v0.5):
  * Implementación de rúbrica de evaluación más precisa
- [2026-03-23] Herramienta de Utilidad Añadida:
  * Script `reset_demo.py` para limpiar entorno de demostración
  * Implementación de función para borrar base de datos
  * Vaciado de directorios de salida RECLUTADOS y DESCARTADOS
  * Añadidas pruebas unitarias para validar funcionamiento
- [2026-03-23] Módulo 4: Interfaz de Usuario de Escritorio (v0.6):
  * Implementación de GUI con customtkinter
  * Soporte para selección de carpeta de CVs
  * Botón de ejecución de análisis
  * Área de logging en tiempo real
  * Botón de reset de demo
  * Soporte de modo oscuro/claro
  * Integración con backend existente

## Detalles de Implementación de GUI
- **Framework**: customtkinter para diseño moderno
- **Arquitectura**: Separación clara entre frontend y backend
- **Funcionalidades**:
  * Selector de carpeta de CVs
  * Ejecución de análisis en thread separado
  * Logging en tiempo real
  * Barra de progreso
  * Botón de reset de demo
- **Consideraciones de Diseño**:
  * Modo oscuro/claro automático
  * Manejo de excepciones
  * Logging detallado
  * Interfaz responsiva

## Próximos Pasos
- Refinamiento de la interfaz de usuario
- Añadir más opciones de configuración
- Implementar exportación de resultados
- Optimizar rendimiento de la GUI
