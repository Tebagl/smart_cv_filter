# Diseño: Script reset_demo.py

## Arquitectura del Script

```python
def reset_demo():
    """
    Resetea el entorno de demostración del proyecto Smart CV Filter.
    
    Acciones:
    - Elimina el archivo de base de datos
    - Vacía los directorios de salida
    - Registra las acciones realizadas
    """
    pass
```

## Detalles de Implementación

### Requisitos de Implementación
- Usar `os` y `shutil` para manipulación de archivos
- Implementar logging para rastrear acciones
- Manejar casos de archivos/directorios no existentes
- Proporcionar mensajes claros de consola

### Flujo de Ejecución
1. Verificar existencia de archivos/directorios
2. Eliminar archivo de base de datos
3. Vaciar directorios de salida
4. Imprimir resumen de acciones

### Consideraciones de Seguridad
- Validar rutas antes de eliminar
- Manejar permisos de archivos
- Evitar eliminación de directorios padre

### Dependencias
- `os`: Manipulación de rutas y archivos
- `shutil`: Operaciones de alto nivel en archivos
- `logging`: Registro de acciones

## Decisiones de Diseño
- No borrar directorios, solo su contenido
- Proporcionar retroalimentación clara al usuario
- Mantener el script simple y enfocado

## Estructura de Directorios Objetivo
```
src/
├── backend/
│   └── reset_demo.py  # Nuevo script
├── data/
│   └── smart_cv.db    # Base de datos a eliminar
└── backend/output/
    ├── RECLUTADOS/    # Directorio a vaciar
    └── DESCARTADOS/   # Directorio a vaciar
```

## Casos de Prueba
- Ejecutar con directorios existentes
- Ejecutar con directorios vacíos
- Manejar permisos insuficientes
- Verificar mensajes de consola