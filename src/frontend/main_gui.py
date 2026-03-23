import os
import sys
import threading
import logging
import tkinter
import customtkinter as ctk
from pathlib import Path

# Función para obtener rutas de recursos de forma compatible con PyInstaller
def get_resource_path(relative_path):
    """
    Obtener ruta absoluta de recursos para ejecutable empaquetado
    
    Args:
        relative_path (str): Ruta relativa al ejecutable
    
    Returns:
        str: Ruta absoluta del recurso
    """
    try:
        # Ruta base para recursos en ejecutable empaquetado
        base_path = sys._MEIPASS
    except Exception:
        # Ruta base para ejecución normal (desarrollo)
        base_path = os.path.abspath(".")
    
    return os.path.normpath(os.path.join(base_path, relative_path))

# Añadir el directorio raíz del proyecto al path de Python
try:
    project_root = sys._MEIPASS
except Exception:
    project_root = str(Path(__file__).resolve().parent.parent.parent)

sys.path.insert(0, project_root)

# Importar módulos del backend
from src.backend import main as backend_main
from src.backend.reset_demo import reset_demo

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartCVFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Smart CV Filter")
        self.geometry("800x600")

        # Configuración del tema
        ctk.set_appearance_mode("system")  # Modo oscuro/claro automático
        ctk.set_default_color_theme("blue")

        # Variables
        default_inputs_path = get_resource_path(os.path.join('src', 'backend', 'inputs'))
        self.input_folder = ctk.StringVar(value=default_inputs_path)

        # Crear componentes de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Selector de carpeta de CVs
        folder_frame = ctk.CTkFrame(main_frame)
        folder_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(folder_frame, text="Carpeta de CVs:").pack(side="left", padx=5)
        
        folder_entry = ctk.CTkEntry(
            folder_frame, 
            textvariable=self.input_folder, 
            width=400
        )
        folder_entry.pack(side="left", padx=5, expand=True, fill="x")

        folder_button = ctk.CTkButton(
            folder_frame, 
            text="Seleccionar", 
            command=self.select_input_folder
        )
        folder_button.pack(side="right", padx=5)

        # Área de botones de control
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(padx=10, pady=10, fill="x")

        analyze_button = ctk.CTkButton(
            control_frame, 
            text="Ejecutar Análisis", 
            command=self.run_analysis
        )
        analyze_button.pack(side="left", padx=5, expand=True, fill="x")

        reset_button = ctk.CTkButton(
            control_frame, 
            text="Reset Demo", 
            command=self.reset_demo,
            fg_color="red"
        )
        reset_button.pack(side="right", padx=5, expand=True, fill="x")

        # Área de logging
        self.log_text = ctk.CTkTextbox(main_frame, height=300)
        self.log_text.pack(padx=10, pady=10, expand=True, fill="both")

        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(padx=10, pady=10, fill="x")
        self.progress_bar.set(0)

    def select_input_folder(self):
        """Abrir diálogo para seleccionar carpeta de CVs"""
        folder_selected = ctk.filedialog.askdirectory(
            initialdir=self.input_folder.get(),
            title="Seleccionar Carpeta de CVs"
        )
        
        if folder_selected:
            self.input_folder.set(folder_selected)
            self.log_text.insert("end", f"Carpeta seleccionada: {folder_selected}\n")

    def run_analysis(self):
        """Ejecutar análisis de CVs en un thread separado"""
        # Limpiar logs anteriores
        self.log_text.delete("1.0", "end")
        
        # Configurar entorno para análisis
        os.environ['CV_INPUT_DIR'] = self.input_folder.get()
        
        # Iniciar análisis en thread separado
        analysis_thread = threading.Thread(target=self.analysis_worker)
        analysis_thread.start()

    def analysis_worker(self):
        """Worker para ejecutar análisis en background"""
        try:
            # Redirigir stdout para capturar logs
            import io
            import sys
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            # Ejecutar análisis
            backend_main.main()

            # Restaurar stdout
            sys.stdout = old_stdout

            # Mostrar logs en UI
            logs = redirected_output.getvalue()
            self.update_log(logs)
            
            # Actualizar progreso
            self.update_progress(1.0)

        except Exception as e:
            self.update_log(f"Error en análisis: {e}")
            self.update_progress(0)

    def update_log(self, message):
        """Actualizar área de logging de forma segura"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def update_progress(self, value):
        """Actualizar barra de progreso de forma segura"""
        self.progress_bar.set(value)

    def reset_demo(self):
        """Resetear entorno de demostración"""
        try:
            reset_demo()
            self.log_text.insert("end", "Entorno de demo reseteado exitosamente.\n")
        except Exception as e:
            self.log_text.insert("end", f"Error al resetear demo: {e}\n")

def main():
    """Punto de entrada de la aplicación"""
    app = SmartCVFilterApp()
    app.mainloop()

if __name__ == "__main__":
    main()