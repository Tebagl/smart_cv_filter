import os
import shutil
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_demo(base_path: str = None) -> None:
    """
    Resetea el entorno de demostración del proyecto Smart CV Filter.
    
    Args:
        base_path (str, optional): Ruta base para los directorios. 
                                   Si no se proporciona, usa el directorio del proyecto.
    
    Acciones:
    - Elimina el archivo de base de datos smart_cv.db
    - Vacía los directorios de salida RECLUTADOS y DESCARTADOS
    
    Imprime mensajes de log sobre las acciones realizadas.
    
    Raises:
        PermissionError: Si no se tienen permisos para eliminar archivos
        OSError: Si hay problemas con operaciones de archivos
    """
    try:
        # Establecer ruta base
        if base_path is None:
            base_path = os.getcwd()
        
        # Rutas de archivos y directorios
        db_path = os.path.join(base_path, 'src', 'data', 'smart_cv.db')
        reclutados_path = os.path.join(base_path, 'src', 'backend', 'output', 'RECLUTADOS')
        descartados_path = os.path.join(base_path, 'src', 'backend', 'output', 'DESCARTADOS')

        # Eliminar base de datos
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                logger.info(f'Base de datos eliminada: {db_path}')
            except PermissionError:
                logger.error(f'Error de permisos al eliminar base de datos: {db_path}')
                raise
        else:
            logger.warning(f'Base de datos no encontrada: {db_path}')

        # Vaciar directorio RECLUTADOS
        if os.path.exists(reclutados_path):
            for filename in os.listdir(reclutados_path):
                file_path = os.path.join(reclutados_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logger.error(f'Error al limpiar {file_path}: {e}')
                    raise
            logger.info(f'Directorio RECLUTADOS vaciado: {reclutados_path}')
        else:
            logger.warning(f'Directorio RECLUTADOS no encontrado: {reclutados_path}')

        # Vaciar directorio DESCARTADOS
        if os.path.exists(descartados_path):
            for filename in os.listdir(descartados_path):
                file_path = os.path.join(descartados_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logger.error(f'Error al limpiar {file_path}: {e}')
                    raise
            logger.info(f'Directorio DESCARTADOS vaciado: {descartados_path}')
        else:
            logger.warning(f'Directorio DESCARTADOS no encontrado: {descartados_path}')

        logger.info('Reseteo de demo completado exitosamente.')

    except (PermissionError, OSError) as e:
        logger.error(f'Error durante el reseteo de demo: {e}')
        raise

def main():
    """Punto de entrada para ejecutar el script de reset de demo."""
    reset_demo()

if __name__ == '__main__':
    main()