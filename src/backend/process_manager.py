import os
from datetime import datetime

class ProcessManager:
    def __init__(self, base_path, cv_handler):
        self.base_path = base_path
        self.cv_handler = cv_handler

    def configure_process(self, puesto, fecha):
        """Configura las rutas físicas para un nuevo proceso de selección."""
        nombre_carpeta = f"{fecha}_{puesto.replace(' ', '_')}"
        ruta_proceso = os.path.join(self.base_path, "procesos_seleccion", nombre_carpeta)
        
        # Inyectar rutas en el handler
        output_dir = os.path.join(ruta_proceso, "output")
        self.cv_handler.base_output = output_dir
        self.cv_handler._ensure_folders()
        
        return os.path.join(output_dir, "RECLUTADOS")