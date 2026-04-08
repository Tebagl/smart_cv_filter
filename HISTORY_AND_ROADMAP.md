# 📑 Smart CV Filter - Historia y Hoja de Ruta

## 🎯 Visión General
Sistema profesional de filtrado y evaluación semántica de CVs que prioriza la **privacidad por diseño** y el **procesamiento local**. Utiliza técnicas avanzadas de NLP y Embeddings para emparejar perfiles candidatos con descripciones de puestos (Job Descriptions) sin enviar datos sensibles a la nube.

---

## 🕒 Historial de Desarrollo y Log de Versiones

### **Fase 1: Cimientos y Extracción (v0.1 - v0.3)**
* **v0.1 - UniversalExtractor**: Soporte para PDF (pdfplumber), DOCX y TXT.
* **v0.2 - LocalAnonymizer**: Anonimización local mediante spaCy (NER) para cumplimiento de GDPR.
* **v0.3 - Calidad**: Suite de tests unitarios y validación de extracción.

### **Fase 2: Orquestación y Transición a la Nube (v0.4 - v0.6)**
* **v0.5 - Era Gemini**: Integración temporal con Google Gemini API para validación de rúbricas.
* **v0.6 - Utilidades**: Scripts de limpieza de entorno y gestión de base de datos SQL.

### **Fase 3: IA Local y Gestión de Procesos (v0.7 - v1.3.0) [ESTADO ACTUAL]**
* **v1.1.0 - Privacy & Local Update**: 
    * Eliminación total de APIs externas. 
    * Integración de `sentence-transformers` (`MiniLM-L12-v2`) para análisis 100% local.
* **v1.2.0 - The Organizer Update**:
    * Clasificación física automatizada en carpetas `RECLUTADOS`, `DUDAS` y `DESCARTADOS`.
* **v1.3.0 - The Precision & Project Update (Actual)**:
    * **Parche de Negaciones**: Implementación de lógica Regex para ignorar tecnologías que el candidato menciona explícitamente no poseer.
    * **Gestión por Proyectos**: Reubicación de la salida a la carpeta `procesos_seleccion/`, organizando los resultados por puesto y fecha.
    * **Orden Físico Profesional**: Renombrado de archivos con índice invertido para que el explorador de archivos del sistema operativo muestre los mejores perfiles al inicio.
    * **UX Enhancement**: El diálogo de búsqueda de carpetas ahora inicializa en Documentos/Escritorio y cuenta con validación de campos obligatorios.

---

## 🏗️ Arquitectura del Sistema (Pipeline)
1.  **Ingestión**: Selección de carpeta externa de CVs (Desktop/Documents).
2.  **Limpieza Semántica**: Detección de negaciones y limpieza de "ruido" técnico.
3.  **Evaluación Local**: Cálculo de similitud del coseno mediante Embeddings locales.
4.  **Decisión**: Clasificación en tres niveles (Apto/Duda/No Apto) basada en umbrales calibrados.
5.  **Logística Documental**: Renombrado (índice invertido) y movimiento físico a la estructura de `procesos_seleccion`.

---

## 🚀 Hoja de Ruta Futura (Roadmap)

### **Próximos Hitos (v1.4 - v1.5)**
- [ ] **Refactorización (ProcessManager)**: Separar completamente la lógica de creación de carpetas de la interfaz de usuario.
- [ ] **Empaquetado Final**: Generación de ejecutable `.exe` único incluyendo los pesos del modelo de IA.
- [ ] **Exportación de Reportes**: Generar un archivo CSV resumen con el ranking y motivos dentro de cada carpeta de proceso.
- [ ] **Lazy Loading**: Carga asíncrona del modelo de IA para que la ventana abra instantáneamente.

### **Objetivos a Largo Plazo**
- [ ] **Soporte Multi-idioma**: Adaptar el motor de negaciones para CVs en inglés.
- [ ] **Feedback Loop**: Permitir que el reclutador ajuste los umbrales de puntuación desde la GUI.
- [ ] **Pre-visualización**: Abrir el CV analizado directamente desde la lista de la interfaz.

---

## 🛠️ Stack Tecnológico Actual
* **Lenguaje**: Python 3.10+
* **GUI**: CustomTkinter (Modern Dark Theme).
* **NLP/AI**: spaCy, sentence-transformers, PyTorch (All Local).
* **Documentos**: PyMuPDF (fitz), python-docx.
* **Logística**: Shutil, Pathlib.

---

## 📝 Principios de Diseño
* **Privacidad**: El dato nunca sale del ordenador del usuario.
* **Orden**: El sistema no solo analiza, sino que organiza el caos documental.
* **Transparencia**: El "Motivo" de la IA siempre es visible para el reclutador.