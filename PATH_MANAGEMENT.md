# 📂 PATH MANAGEMENT - Smart CV Filter

## 🌍 Visión General
Para garantizar la estabilidad del sistema tanto en desarrollo como en el ejecutable final (`.exe`), se ha implementado un sistema de rutas relativas dinámicas basadas en la ubicación del proceso.

## 📍 Ubicación de Componentes Clave

### 🗄️ Base de Datos (`smart_cv.db`)
- **Ruta**: `src/data/smart_cv.db`
- **Persistencia**: La base de datos se mantiene fija en esta ubicación para asegurar que los registros de candidatos no se pierdan entre sesiones.
- **Inicialización**: El sistema verifica la existencia de la carpeta `src/data/` y la crea automáticamente si no existe.

### 📁 Directorios de Salida (Output)
El sistema clasifica físicamente los archivos tras el análisis:
- **Reclutados**: `src/backend/output/RECLUTADOS/`
- **Descartados**: `src/backend/output/DESCARTADOS/`

### 📜 Registros (Logs)
- **Ruta**: `/logs/smart_cv_filter.log` (en la raíz del proyecto).
- **Gestión**: Implementa rotación automática (máx. 10MB) para no saturar el almacenamiento.

## 💻 Implementación Técnica (Lógica de Rutas)

Para evitar errores en entornos "congelados" (PyInstaller), utilizamos `pathlib` para detectar la raíz del proyecto de forma robusta:

```python
from pathlib import Path
import sys

# Detección de la Raíz del Proyecto
if getattr(sys, 'frozen', False):
    # Si es un ejecutable (.exe)
    BASE_DIR = Path(sys.executable).parent
else:
    # Si es entorno de desarrollo (.py)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent 
```