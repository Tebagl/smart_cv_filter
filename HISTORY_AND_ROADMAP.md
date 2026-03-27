# 📑 Smart CV Filter - Historia y Hoja de Ruta

## 🎯 Visión General
Sistema profesional de filtrado y evaluación semántica de CVs que prioriza la **privacidad por diseño** y el **procesamiento local**. Utiliza técnicas avanzadas de NLP y Embeddings para emparejar perfiles candidatos con descripciones de puestos (Job Descriptions) sin enviar datos sensibles a la nube.

---

## 🕒 Historial de Desarrollo y Log de Versiones

### **Fase 1: Cimientos y Extracción (v0.1 - v0.3)**
* **v0.1 - UniversalExtractor (`extractor.py`)**:
    * Implementación de `pdfplumber` para manejar CVs complejos a 2 columnas mediante *bounding boxes*.
    * Soporte para DOCX (`python-docx`) y TXT plano.
* **v0.2 - LocalAnonymizer (`anonymizer.py`)**:
    * Cumplimiento estricto de **GDPR**.
    * Uso híbrido de Regex para Emails/Teléfonos y **spaCy (NER)** para nombres de personas.
    * Migración del modelo `sm` al modelo medio `es_core_news_md` para mayor precisión.
* **v0.3 - Calidad y Pruebas**:
    * Creación de suite de tests unitarios (`unittest`) con `MagicMock` para simular PDFs sin archivos reales.

### **Fase 2: Orquestación y Transición a la Nube (v0.4 - v0.6)**
* **v0.4 - Primer Orquestador (`main.py`)**:
    * Punto de entrada asíncrono. Manejo de variables de entorno (`python-dotenv`).
* **v0.5 - Era de las APIs Externas (Gemini)**:
    * Integración de **Google Gemini** (v1.5/2.5 Flash) para análisis semántico.
    * Implementación de rúbrica de evaluación (Ventas B2B, Comunicación, Mercado IT).
    * Validación exitosa de perfiles (Docentes vs Ingenieros vs Ventas).
* **v0.6 - Utilidades de Sistema**:
    * Creación de scripts de limpieza y gestión de entorno.

### **Fase 3: Profesionalización e IA Local (v0.7 - v1.2.0) [ESTADO ACTUAL]**
* **v0.7 - Interfaz Gráfica Moderna**:
    * Desarrollo de GUI con `customtkinter` (Modo Oscuro/Claro).
    * Logging en tiempo real integrado en la ventana.
* **v1.1.0 - El Salto a lo Local (Privacy Update)**:
    * **Eliminación de APIs externas**: Sustitución de Gemini por `sentence-transformers` y `torch`.
    * Implementación de base de datos local **SQLite** con **SQLAlchemy** para persistencia.
    * Introducción de **Structured Logging** con `structlog` para trazabilidad profesional.
* **v1.2.0 - The Organizer Update**:
    * **Clasificación Física**: Automatización del movimiento de archivos a carpetas `RECLUTADOS` y `DESCARTADOS` mediante `shutil`.
    * Optimización de procesos por lotes (150+ CVs).
    * Refactorización de rutas robustas con `pathlib`.

---

## 🏗️ Arquitectura del Sistema (Pipeline)
1.  **Ingestión**: Recolección de archivos desde directorio configurado.
2.  **Extracción**: Normalización de PDF/DOCX a texto plano.
3.  **Sanitización**: Anonimización de PII (Datos personales) mediante spaCy.
4.  **Análisis Local**: Comparación semántica (*Cosine Similarity*) entre CV y `job_description.txt`.
5.  **Persistencia**: Registro en `smart_cv.db`.
6.  **Logística**: Clasificación física de documentos según el veredicto de la IA.

---

## 🚀 Hoja de Ruta Futura (Roadmap)

### **Próximos Hitos (v1.3 - v1.5)**
- [ ] **Empaquetado Final**: Generación de ejecutable `.exe` estable con PyInstaller incluyendo modelos de Torch/Spacy.
- [ ] **Análisis por Pilares**: Desglosar la puntuación en: Experiencia, Habilidades Técnicas y Formación.
- [ ] **Exportación de Reportes**: Generar archivos Excel/CSV con el ranking consolidado de candidatos.
- [ ] **Pre-visualización**: Abrir el CV analizado directamente desde la interfaz con doble clic.
- [ ] **Optimización de Carga**: Implementar *Lazy Loading* para que la App abra instantáneamente mientras el modelo de IA carga en segundo plano.

### **Objetivos a Largo Plazo**
- [ ] **Soporte Multi-idioma**: Adaptar el anonimizador y el análisis para CVs en inglés y francés.
- [ ] **Feedback Loop**: Permitir que el reclutador corrija a la IA para re-entrenar los umbrales de éxito.
- [ ] **Dashboard Estadístico**: Gráficas de embudo (Candidatos totales vs Aptos).
- [ ] **Versión Web**: Migración de la lógica a un entorno basado en navegador conservando la privacidad.

---

## 🛠️ Stack Tecnológico Actual
* **Lenguaje**: Python 3.10+
* **GUI**: CustomTkinter
* **NLP/AI**: spaCy (`es_core_news_md`), sentence-transformers, PyTorch.
* **Base de Datos**: SQLite + SQLAlchemy.
* **Logging**: Structlog + standard logging.
* **Empaquetado**: PyInstaller.

---

## 📝 Principios de Diseño
* **Privacidad**: El dato nunca sale del ordenador del usuario.
* **Determinismo**: Mismos datos, mismos resultados (Temperatura 0 en modelos).
* **Resiliencia**: Manejo de errores en lectura de archivos dañados o formatos extraños.