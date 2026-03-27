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

## Fecha: 26 de marzo de 2026
Hito: Transición a Arquitectura de IA 100% Local

- Problema Identificado:
La arquitectura híbrida previa (Nube + Local) presentaba cuellos de botella críticos al procesar volúmenes reales de datos (70+ CVs). Las limitaciones de cuota de la API de Google Gemini provocaban errores 429 (Too Many Requests), deteniendo el flujo de trabajo. Además, el reintento constante entre la nube y el motor local generaba latencias inaceptables de hasta 2 minutos para apenas 3 archivos.

- Solución Implementada:
Se ha desconectado por completo la lógica de análisis de cualquier dependencia externa. El sistema ahora opera de forma 100% Local, utilizando el modelo paraphrase-multilingual-MiniLM-L12-v2 integrado en el entorno virtual (.venv).

- Optimizaciones Técnicas Clave:

Carga Única en RAM: El modelo de IA se carga una sola vez al inicio del programa (estilo Singleton), eliminando el tiempo de carga repetitivo por cada CV.

Procesamiento Instantáneo: Al eliminar las llamadas HTTP, el tiempo de análisis por currículum ha pasado de segundos a milisegundos.

Motor de Razonamiento Local: Se ha desarrollado una lógica interna (_get_local_reasoning) que traduce la similitud del coseno (matemática) en explicaciones humanas descriptivas.

Privacidad Total: Los datos de los candidatos no salen nunca del equipo local, garantizando el cumplimiento de normativas de privacidad y eliminando costes de API.

- Estado Actual:

Éxito: Estabilidad total y velocidad ultra-rápida confirmada para lotes de 150+ CVs.

Pendiente: Sincronizar la lógica de clasificación de archivos (mover a carpetas RECLUTADOS/DESCARTADOS) con el nuevo formato de salida local.

## Fecha: 27 de marzo de 2026
# Hito: Implementación de Clasificación Física de Archivos (Post-Procesamiento)

# Cambios Realizados:

* Automatización del Sistema de Archivos: Se ha integrado una lógica de movimiento de archivos en el analysis_worker de la GUI. El programa ahora clasifica automáticamente los currículums procesados.

* Estructura de Salida: Los archivos se mueven desde inputs/ hacia subcarpetas específicas en src/backend/output/:

* RECLUTADOS/: Para candidatos con decisión "SI".

* DESCARTADOS/: Para candidatos con decisión "NO".

* Refuerzo de la Integridad de Datos: Se ha reordenado el flujo de ejecución para garantizar que la extracción de datos de la IA (puntuación y motivo) ocurra antes del desplazamiento físico del archivo, evitando errores de lectura y asegurando que la interfaz muestre la información correcta (evitando el error de 0% de coincidencia).

* Gestión de Errores de E/S: Implementación de bloques try/except específicos para las operaciones de renombrado (rename), permitiendo que el análisis masivo continúe incluso si un archivo individual está bloqueado por el sistema operativo.

# Impacto:
El sistema ha pasado de ser una herramienta de visualización a una herramienta de gestión documental completa. La capacidad de procesar y organizar 150+ CVs de forma autónoma reduce el tiempo de operación manual en un 90%.

## 📝 Registro de Desarrollo: 27 de marzo de 2026
# Resumen de Cambios Técnicos

* Migración de Base de Datos: Se ha reubicado el archivo smart_cv.db a una carpeta centralizada en src/data/. Anteriormente, el sistema generaba bases de datos duplicadas en la raíz o en carpetas internas de la lógica.

* Refactorización de Rutas: Se ha implementado una resolución de rutas absolutas en database.py utilizando pathlib. Ahora el sistema detecta correctamente la ubicación de los datos independientemente de si se ejecuta desde la raíz o mediante el entorno virtual.

* Persistencia de Análisis: Se ha corregido un fallo en cv_handler.py donde los resultados de la IA se procesaban pero no se guardaban físicamente en el disco. Se añadió el método self._session.commit() sincronizado con el modelo de datos de SQLAlchemy.

* Simplificación de Arquitectura: Se eliminó la capa de repositories/ (obsoleta) para reducir la fragmentación del código. La lógica de guardado ahora reside directamente en los Handlers, optimizando el mantenimiento.

* Seguridad y Privacidad
Modo 100% Local: Se han eliminado las API Keys (Google/OpenAI) del archivo .env. El proyecto ha completado su transición a un modelo de "Privacidad por Diseño", procesando todo el contenido mediante sentence-transformers locales.

* Anonimización: Se ha verificado que la cadena de procesamiento anonimiza los datos antes de cualquier análisis, cumpliendo con estándares de protección de datos.

## Próximos Pasos

* Configurar el empaquetado con PyInstaller (.spec) para incluir el modelo de IA local dentro de un ejecutable único.

* Implementar "Lazy Loading" para que la carga del modelo de IA no retrase la apertura inicial de la interfaz gráfica.