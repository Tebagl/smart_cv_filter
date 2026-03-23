# Smart CV Filter - Filtrado de Talento con IA

Este repositorio contiene una solución de arquitectura avanzada diseñada para automatizar el filtrado de talento mediante la IA de **Google Gemini**, garantizando la privacidad de los datos y la objetividad mediante el desarrollo basado en especificaciones (**SDD**).

## 🚀 Visión General
**Smart CV Filter** realiza un **Análisis Semántico Profundo** para entender la experiencia real del candidato, yendo más allá de la simple coincidencia de palabras clave. Está construido para ser portable, fuertemente tipado y compatible con agentes de IA.

## 🛡️ Pilares del Sistema
* **Privacidad Primero (GDPR):** Integra un **Anonimizador Local** que sanitiza PII (nombres, correos, teléfonos) localmente antes de cualquier procesamiento en la nube.
* **Evaluación Objetiva (Rúbrica 40/30/30):** Elimina sesgos de la IA con una rúbrica de puntuación estricta y determinista (Temp 0.0):
    * **40%**: Experiencia directa (Ventas B2B/Account Executive).
    * **30%**: Habilidades de comunicación y cierre.
    * **30%**: Conocimiento del mercado tecnológico.
* **Trazabilidad Total:** Cada decisión se registra en una **Base de Datos SQL** física (`smart_cv.db`), permitiendo auditorías posteriores del proceso de selección.
* **Estándares Gestionados por IA:** Cumple con reglas estrictas definidas en `ai-specs/` para asegurar un código consistente y de alta calidad en diferentes Copilots (Gemini, Claude, Cursor).

## 📁 Estructura del Repositorio
```text
.
├── ai-specs/                # Reglas de Agentes IA y estándares de desarrollo
├── src/
│   ├── backend/             # Lógica central (Extractor, Anonymizer, Analyzer)
│   │   ├── inputs/          # Ingesta de CVs (PDF, DOCX, TXT)
│   │   └── output/          # CVs Clasificados (RECLUTADOS/DESCARTADOS)
│   └── data/                # Persistencia SQL (smart_cv.db)
├── DEVELOPMENT_LOG.md       # Bitácora técnica y corrección de errores
└── HISTORY_AND_ROADMAP.md   # Hitos funcionales y visión de futuro
🛠️ Uso: Flujo Basado en Comandos
Este proyecto sigue el flujo OPSX definido en nuestras AI Specifications:

Explorar: /opsx:explore [Tarea] para analizar el impacto.

Planificar: /opsx:propose [Funcionalidad] para crear el plan en ai-specs/changes/.

Ejecutar: /opsx:apply [Plan] para implementar con TDD y seguridad de tipos.

Archivar: /opsx:archive para verificar la Definition of Done (DoD) y actualizar logs.