# 📂 PATH MANAGEMENT - Smart CV Filter

## 🌍 Visión General
El sistema utiliza un motor de resolución de rutas dinámicas para asegurar la portabilidad del software. Se ha migrado de un modelo de carpetas estáticas a un modelo de **Gestión por Proyectos**, donde las rutas de salida se generan bajo demanda según el puesto y la fecha.

## 📍 Ubicación de Componentes Clave

### 🏗️ Carpeta Raíz de Procesos
- **Ruta**: `procesos_seleccion/`
- **Descripción**: Directorio principal en la raíz del proyecto que agrupa todos los procesos de filtrado realizados.
- **Estructura Interna**: 
  `procesos_seleccion/{AAAA-MM-DD}_{Nombre_del_Puesto}/output/`

### 🗄️ Base de Datos (`smart_cv.db`)
- **Ruta**: `src/data/smart_cv.db`
- **Gestión**: Centralizada para mantener el historial de análisis y scores independientemente del proceso de selección activo.

### 📁 Directorios de Salida Dinámicos (Output)
Dentro de cada carpeta de proceso, el sistema crea:
- **RECLUTADOS**: Para perfiles aptos (Score ≥ 70% o Apto IA).
- **DUDAS**: Para perfiles en zona gris (Score 50-69%).
- **DESCARTADOS**: Para perfiles no aptos (Score < 50%).

## 💻 Implementación Técnica (Lógica de Rutas)

### 1. Resolución de Base para Ejecutables
Para garantizar que el programa funcione tras ser empaquetado con PyInstaller, implementamos una función de detección de entorno:

```python
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Entorno de Ejecutable (.exe)
        return Path(sys._MEIPASS)
    else:
        # Entorno de Desarrollo (.py)
        return Path(__file__).resolve().parent.parent.parent