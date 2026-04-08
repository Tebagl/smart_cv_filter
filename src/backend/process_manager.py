import os
import platform
import ctypes

def hide_folder(path):
    """
    Oculta una carpeta en Windows añadiendo el atributo de sistema 'Hidden'.
    En otros sistemas operativos no realiza ninguna acción para evitar errores.
    """
    if platform.system() == "Windows":
        try:
            # Atributo 2 corresponde a FILE_ATTRIBUTE_HIDDEN
            ctypes.windll.kernel32.SetFileAttributesW(str(path), 2)
        except Exception:
            pass

class ProcessManager:
    def __init__(self, base_path, cv_handler):
        self.base_path = base_path
        self.cv_handler = cv_handler
        # 🛡️ Limpiamos la interfaz visual nada más arrancar
        self.cleanup_ui_folders()

    def cleanup_ui_folders(self):
        """Oculta las carpetas técnicas para que el usuario final no se abrume."""
        to_hide = [
            "src",
            "logs",
            "models",
            "build",
            "ai-specs",
            "openspec",
            "Procesos",  # Carpeta antigua por si acaso
            "__pycache__",
            ".cursor",
            ".roo"
        ]
        
        for folder_name in to_hide:
            folder_path = os.path.join(self.base_path, folder_name)
            if os.path.exists(folder_path):
                hide_folder(folder_path)

    def configure_process(self, puesto, fecha):
        """Configura las rutas físicas para un nuevo proceso de selección."""
        # Aseguramos que el nombre de la carpeta sea amigable para el SO
        nombre_carpeta = f"{fecha}_{puesto.replace(' ', '_')}"
        ruta_proceso = os.path.join(self.base_path, "procesos_seleccion", nombre_carpeta)
        
        # Inyectar rutas en el handler
        output_dir = os.path.join(ruta_proceso, "output")
        self.cv_handler.base_output = output_dir
        self.cv_handler._ensure_folders()
        
        # Ocultamos la carpeta técnica 'src' de nuevo por si se hubiera creado después
        self.cleanup_ui_folders()
        
        return os.path.join(output_dir, "RECLUTADOS")