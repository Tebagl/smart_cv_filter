# HISTORY & ROADMAP - Smart CV Filter

Este documento es la memoria central del proyecto bajo el modelo **Spec-Driven Development**. Aquí se registran las decisiones arquitectónicas de las primeras versiones, el estado actual del flujo de datos, los tests completados y los hitos futuros.

---

## Log de Versiones (v0.1 a v0.4)

* **v0.1 - UniversalExtractor (`extractor.py`)**:
  * **Propósito**: Extraer texto limpio de múltiples formatos de CVs (PDF, DOCX, TXT), sentando las bases de la lectura de documentos.
  * **Elección de Librerías**: Se priorizó `pdfplumber` sobre otras opciones (como PyPDF2) como la solución idónea para mantener el flujo de lectura adecuado, específicamente porque nos permite operar visualmente con bounding boxes y manejar los problemáticos formatos de CVs a **2 columnas**. Se empleó `python-docx` por ser el estándar más robusto.
  * **Lógica**: Utiliza métodos estáticos que identifican la extensión del archivo y delegan la extracción a la función especializada correspondiente.

* **v0.2 - LocalAnonymizer (`anonymizer.py`)**:
  * **Propósito**: Anonimizar Datos de Identificación Personal (PII) localmente antes de enviar información a LLMs, cumpliendo estrictamente con la normativa de privacidad (GDPR).
  * **Elección de Librerías**: Se emplearon Expresiones Regulares nativas (`re`) para patrones lógicos estructurales como Emails y Teléfonos. Para la Detección de Nombres (NER) se escogió **`spaCy`** (modelo `es_core_news_sm`) porque se ejecuta de forma rápida y 100% en local, preservando la seguridad del dato.
  * **Lógica**: La clase `LocalAnonymizer` procesa el texto en fases. Si el modelo NLP en español no está instalado en el sistema, el script fuerza la descarga mediante subprocesamiento en el entorno de inicialización. Reemplaza los strings de forma estructurada para no corromper índices en el flujo de la frase.

* **v0.3 - Script de Pruebas Unitarias** (`test_module.py` y `test_anonymizer.py`):
  * **Propósito**: Proveer tests funcionales automatizados. Emplean la librería `unittest` e incluyen módulos sofisticados como `patch` y `MagicMock` para simular PDFs (ej. emulando coords de rectángulos limitadores) sin arrastrar la dependencia de documentos reales.

* **v0.4 - Orquestador Central (`main.py`)**:
  * **Propósito**: Punto de entrada asíncrono y centralizador de la aplicación.
  * **Lógica**: Integra de forma condicional la carga de las variables de entorno (`dotenv`), inicializa la estructura de rutas (`inputs/`, `output/RECLUTADOS/`, `output/DESCARTADOS/`), las clases de los módulos en cascada y elabora la iteración base para analizar los archivos hallados.

---

## Estado del Sistema

### Arquitectura de Flujo de Datos
El proyecto cuenta con una arquitectura de tubería procesal (pipeline process):
1. **Punto de Ingestión**: Todos los archivos originales (`inputs/`) son recolectados al instanciar `main.py`.
2. **Ciclo Iterativo**: El orquestador entra en un loop donde:
   * **Invocación a `UniversalExtractor`**: Transforma la estructura física en un simple *string* de texto plano.
   * **Invocación a `LocalAnonymizer`**: Recibe el string expuesto y devuelve un nuevo iterado *string* sanitizado de PII (anonimizado), dejando los datos limpios para evaluación.
3. El output actual retorna estas métricas a consola sin mover el archivo ni conectar a servicios paralelos.

### Tests Superados
Durante la presente fase:
* **Extractor (`test_module.py`)**: Pasó con éxito el control de excepciones de formato, lectura cruda en TXT y su emulador Mock superó la detección de bloques izquierda-derecha para 2 columnas PDF.
* **Anonimizador (`test_anonymizer.py`)**: Pasó satisfactoriamente. Detecta y sustituye exitosamente correos, números telefónicos (sintaxis de guiones y paréntesis) y Nombres apoyándose en los motores del modelo estadístico de NER (`PER`).

---

## Roadmap de Implementación

Actualmente entramos en la etapa de Integración y Reglas de Negocio Inteligentes.

### 🚀 Hito Alcanzado: Módulo 3 Integrado (End-to-End Testeado)
- **Estado actual**: El sistema ya opera de manera **End-to-End** empleando Google Gemini.
- **Detalle Táctico**: El orquestador lee los documentos PDF/DOCX/TXT base, el módulo `anonymizer` extrae información y el módulo `analyzer.py` evalúa los perfiles conectando dinámicamente con Gemini, validándolos contra `job_description.txt`. Le exigimos al LLM responder en JSON:
  ```json
  {"apto": "SI/NO", "puntuacion": 0-100, "motivo": "Explicación breve"}
  ```

### 🚀 Siguiente Hito: Módulo de Clasificación Física
- **Tarea Prioritaria**: Mover los archivos procesados a sus carpetas finales correspondientes.
- **Detalle Táctico**: Implementar la integración en `main.py` mediante `shutil.move` u `os.rename` para migrar logísticamente el documento base evaluado del directorio `inputs/` a `/output/RECLUTADOS/` (si `"apto": "SI"`) o a `/output/DESCARTADOS/` (si `"apto": "NO"`).

### 🔨 Mejoras Pendientes
* **Manejo de errores de API**: Implementar bloques robustos de reintentos (`Tenacity` o `try-catch` anidados) para asegurar resiliencia en casos de *Rate Limits* o cortes de Gemini (timeout).
* **Sistema de logs de errores**: Reemplazar reportajes nativos `print()` con arquitecturas de `logging` en disco (ej. archivo `app.log`) para persistir la trazabilidad y problemas a nivel de sistema de cara a producción.

---

## Incidencias Solucionadas

* **Saneamiento de Entorno y Dependencias**:  
  Se detectaron errores del tipo `ModuleNotFoundError` por falta de correlación entre el código y el entorno local. Se realizó una auditoría y las siguientes acciones correctivas resultaron exitosas:
  * Instalación de paquetes obligatorios: `pdfplumber`, `python-docx`, `spacy`, `python-dotenv`, `openai`.
  * Descarga y configuración del modelo lingüístico avanzado **`es_core_news_lg`** (mejorando la exactitud del modelo `sm` anterior) en `anonymizer.py`.
  * Generación del manifiesto `requirements.txt` extrayendo las dependencias consolidadas.
  * Revalidación en verde de las pruebas unitarias (`test_module.py` en 0.025s y `test_anonymizer.py` en 3.44s). El entorno es reportado como totalmente estable.

* **Migración a Google Gemini**:
  * Se reemplazó el uso de OpenAI por la API de Google Gemini (modelo `gemini-1.5-flash` y `gemini-2.5-flash`) en el `analyzer.py` por temas de compatibilidad de claves proporcionadas.
  * Se instaló la dependencia `google-generativeai` y el orquestador fue actualizado para cargar `GEMINI_API_KEY`.
  * Se actualizó `requirements.txt` eliminando `openai` e incorporando `google-generativeai==0.8.6` para reflejar el estado correcto de las dependencias.

* **Prueba de Validación V1.0 (End-to-End)**:
  * El sistema ya es End-to-End. Se probaron exitosamente 3 currículums reales frente al perfil de la vacante docente descrita en `job_description.txt`, validando los retornos estrictos JSON y la abstracción semántica de Gemini:
    * `cv_pablo_docente.txt` -> 97/100, Apto: SI (Cumple enseñanza e inglés nivel C1).
    * `cv_carlos_ingeniero.txt` -> 10/100, Apto: NO (Ingeniero sin perfil ni titulación docente).
    * `cv_test.txt` -> 5/100, Apto: NO (Vendedor Account Executive B2B puro).

### 🔧 Mejoras Recientes en Análisis de CV (v0.5)
* **Optimización del Modelo de Evaluación**:
  * Implementación de una rúbrica de evaluación más precisa y estructurada en `analyzer.py`:
    - Criterios de evaluación divididos en 3 categorías con pesos específicos:
      1. Experiencia en Ventas B2B / Account Executive (40%)
      2. Habilidades de Comunicación y Cierre de Contratos (30%)
      3. Conocimiento del Mercado Tecnológico (30%)
  * Configuración de temperatura del modelo a 0.0 para garantizar respuestas determinísticas
  * Mejora en el manejo de errores de API, especialmente para casos de cuota excedida
  * Adición de un tiempo de espera de 5 segundos entre análisis para respetar límites de la API

### Próximos Pasos y Objetivos a Corto/Medio Plazo:

* **Optimización de Flujo de Archivos (Prioridad Inmediata)**:

* Restaurar la automatización de movimiento de archivos .txt analizados hacia las carpetas de salida según el flag apto generado por la IA local.

* **Refinamiento del Motor Local**:

* Ajustar los umbrales de puntuación (Thresholds) para mejorar la precisión del filtrado automático.

* Implementar un "Análisis por Pilares" local para desglosar la nota en: Experiencia, Habilidades Técnicas y Formación.

* **Mejora de la Interfaz de Usuario (GUI)**:

* Añadir indicadores visuales del estado del modelo local (Cargado/Listo).

* Implementar una vista de "Resumen Estadístico" tras procesar grandes lotes (ej. % de candidatos aptos vs descartados).

* **Exportación de Resultados**:

* Generar reportes automáticos en formato CSV o Excel con el ranking de los 150+ CVs procesados para facilitar la toma de decisiones.

## Versión Actual: v1.2.0 - "The Organizer Update"
# Novedades:

* **Clasificación Automática: ¡Adiós al ordenamiento manual!**  Ahora el filtro mueve los archivos analizados a sus carpetas correspondientes en tiempo real.

* Interfaz Sincronizada: Mejora en la comunicación entre el hilo de análisis y la GUI para mostrar estados precisos (✅ RECLUTADO / ❌ DESCARTADO) junto a sus respectivos motivos técnicos.

* Robustez en Lotes: Optimización del motor para manejar grandes volúmenes de archivos (150+ CVs) sin interrupciones por errores de acceso a disco.

* **Próximos Pasos:**

* Limpieza de Directorios: Añadir una función para limpiar las carpetas de salida desde la interfaz (botón "Reset Output").

* Resumen Final: Generar un reporte consolidado al finalizar el análisis de un lote grande.

* Pre-visualización: Permitir abrir el archivo .txt directamente desde el log de la GUI haciendo doble clic.