# Diseño de Interfaz de Usuario de Escritorio para Smart CV Filter

## Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│           Arquitectura GUI              │
├─────────────────────────────────────────┤
│                                         │
│   ┌───────────┐     ┌───────────┐       │
│   │  Frontend │────▶│  Backend  │       │
│   │(tkinter)  │◀────│  (main.py)│       │
│   └───────────┘     └───────────┘       │
│                                         │
│   Componentes:                          │
│   - Selección de Carpeta                │
│   - Botón de Ejecución                  │
│   - Área de Logging                     │
│   - Barra de Progreso                   │
│   - Botón de Reset                      │
└─────────────────────────────────────────┘
```

## Diseño de Interfaz de Usuario

### Componentes Principales
1. **Selector de Carpeta de CVs**
   - Botón "Seleccionar Carpeta"
   - Muestra ruta seleccionada
   - Valor por defecto: `src/backend/inputs/`

2. **Área de Control**
   - Botón "Ejecutar Análisis"
   - Botón "Reset Demo"
   - Barra de progreso/estado

3. **Área de Logging**
   - Texto scrollable
   - Muestra información en tiempo real
   - Soporte para diferentes niveles de log

## Especificaciones Técnicas

### Dependencias
- `customtkinter`: Framework de UI
- `threading`: Ejecución asíncrona
- Módulos existentes del backend

### Gestión de Eventos
- Selector de carpeta: Actualiza ruta de inputs
- Botón Ejecutar: 
  * Inicia análisis en thread separado
  * Actualiza UI en tiempo real
- Botón Reset: 
  * Llama a `reset_demo.py`
  * Limpia estado de la aplicación

### Manejo de Excepciones
- Captura y muestra errores en área de logging
- Previene bloqueo de UI
- Información detallada de errores

## Flujo de Ejecución

```python
def ejecutar_analisis():
    # Iniciar en thread separado
    thread = threading.Thread(target=main.main)
    thread.start()
    
    # Actualizar UI en tiempo real
    while thread.is_alive():
        actualizar_log()
        actualizar_progreso()
```

## Consideraciones de Diseño

### Modo Oscuro
- Soporte nativo de customtkinter
- Tema configurable
- Transición suave entre modos

### Responsividad
- Diseño adaptable
- Tamaños de componentes flexibles
- Soporte para diferentes resoluciones

## Seguridad y Privacidad
- No almacenar datos sensibles
- Respetar lógica de anonimización existente
- Logs temporales

## Mejoras Futuras
- Configuración de parámetros de análisis
- Exportación de resultados
- Integración con sistemas de gestión de RR.HH.