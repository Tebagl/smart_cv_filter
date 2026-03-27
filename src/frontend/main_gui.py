import os
import sys
import threading
import logging
import tkinter
import customtkinter as ctk
from pathlib import Path
import queue

# Añadir el directorio raíz del proyecto al path de Python
def get_base_path():
    """
    Obtener la ruta base para recursos, compatible con PyInstaller
    """
    try:
        # Ruta base para recursos en ejecutable empaquetado
        base_path = sys._MEIPASS
    except Exception:
        # Ruta base para ejecución normal (desarrollo)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    return base_path

# Añadir ruta base al sys.path
base_path = get_base_path()
sys.path.insert(0, base_path)

# Importar módulos del backend
from src.backend.cv_handler import CandidateRepository
# Configuración de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartCVFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # 🚀 CONEXIÓN CON EL MOTOR REAL
        # Importante: Recuerda que CandidateRepository necesita la sesión de la DB
      # 🚀 CONEXIÓN CON TU DATABASE MANAGER REAL
        from src.backend.database import DatabaseManager

        # 1. Inicializamos el Manager (esto crea las tablas y el motor)
        self.db_manager = DatabaseManager()
        
        # 2. Le pedimos una sesión activa
        self.db_session = self.db_manager.get_session()
        
        # 3. Se la pasamos al repositorio (tu archivo cv_handler.py)
        self.repo = CandidateRepository(self.db_session)

        # Configuración de la ventana
        self.title("Smart CV Filter")
        self.geometry("800x600")

        # Configuración del tema
        ctk.set_appearance_mode("system")  # Modo oscuro/claro automático
        ctk.set_default_color_theme("blue")

        # Cola para comunicación entre threads
        self.log_queue = queue.Queue()
        self.progress_queue = queue.Queue()

        # Variables
        default_inputs_path = os.path.join(base_path, 'src', 'backend', 'inputs')
        self.input_folder = ctk.StringVar(value=default_inputs_path)

        # Crear componentes de la interfaz
        self.create_widgets()

        # Configurar actualización de logs y progreso
        self.after(100, self.check_queues)

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

        # --- SECCIÓN JOB DESCRIPTION ---
        self.jd_label = ctk.CTkLabel(self, text="Descripción del Puesto (Job Description):", font=("Arial", 12, "bold"))
        self.jd_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.jd_textbox = ctk.CTkTextbox(self, height=150, width=560)
        self.jd_textbox.pack(pady=(5, 10), padx=20)
        self.jd_textbox.insert("0.0", "Pegue aquí los requisitos de la vacante...")

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
        # 1. Limpiar logs anteriores
        self.log_text.delete("1.0", "end")
        
        # 2. Capturar el texto del usuario ANTES de lanzar el hilo
        user_description = self.jd_textbox.get("0.0", "end").strip()
        
        # Si el usuario no escribió nada o dejó el texto por defecto, enviamos None
        if not user_description or "Pegue aquí" in user_description:
            user_description = None
            self.log_text.insert("end", "ℹ️ Usando descripción por defecto (job_description.txt)\n")
        else:
            self.log_text.insert("end", "✅ Usando descripción personalizada del cuadro de texto.\n")

        # 3. Iniciar análisis pasando la descripción como argumento al worker
        analysis_thread = threading.Thread(
            target=self.analysis_worker, 
            args=(user_description,), # <-- Pasamos el texto aquí
            daemon=True
        )
        analysis_thread.start()
        
    def analysis_worker(self, user_job_desc):
        """Worker que analiza y MUEVE los archivos con descripción dinámica"""
        try:
            folder_path = self.input_folder.get()
            self.log_queue.put(f"📂 Escaneando carpeta: {folder_path}...")
            
            # 1. Buscar archivos .txt
            files = list(Path(folder_path).glob("*.txt"))
            
            if not files:
                self.log_queue.put("⚠️ No se encontraron archivos .txt.")
                self.progress_queue.put(0)
                return

            # --- CONFIGURAR CARPETAS DE SALIDA ---
            # Usamos base_path definido globalmente en tu archivo
            output_dir = Path(base_path) / 'src' / 'backend' / 'output'
            reclutados_dir = output_dir / 'RECLUTADOS'
            descartados_dir = output_dir / 'DESCARTADOS'
            
            reclutados_dir.mkdir(parents=True, exist_ok=True)
            descartados_dir.mkdir(parents=True, exist_ok=True)

            self.log_queue.put(f"📑 Encontrados {len(files)} archivos. Iniciando...")

            for i, file_path in enumerate(files):
                self.log_queue.put(f"🔍 Procesando: {file_path.name}")
                
                # Leer el contenido del CV
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                except Exception as read_error:
                    self.log_queue.put(f"❌ Error al leer {file_path.name}: {read_error}")
                    continue

                # 🚀 ANALIZAR (Pasamos el contenido y la descripción personalizada)
                # IMPORTANTE: Tu cv_handler.py debe aceptar (contenido, user_job_desc)
                resultado = self.repo.process_cv(contenido, user_job_desc)
                
                if resultado.get("status") == "success":
                    estado = resultado.get('decision', 'ANALIZADO')
                    motivo = resultado.get('reason', 'Sin detalles')
                    
                    self.log_queue.put(f"   📢 ESTADO: {estado}")
                    self.log_queue.put(f"   📝 MOTIVO: {motivo}")

                    # --- LÓGICA DE MOVIMIENTO ---
                    # Clasificamos según la decisión de la IA
                    if estado == "SI":
                        destino = reclutados_dir / file_path.name
                    else:
                        destino = descartados_dir / file_path.name

                    # Movemos el archivo físico (operación atómica)
                    try:
                        # Usamos replace en lugar de rename para evitar errores si el archivo ya existe
                        file_path.replace(destino)
                        self.log_queue.put(f"   📂 Clasificado en: {destino.parent.name}")
                    except Exception as move_error:
                        self.log_queue.put(f"   ⚠️ Error al mover archivo: {move_error}")

                    self.log_queue.put("-" * 45)
                else:
                    self.log_queue.put(f"❌ Error en {file_path.name}: {resultado.get('reason')}")
                
                # Actualizar progreso en la GUI
                progress = (i + 1) / len(files)
                self.progress_queue.put(progress)

            self.log_queue.put("\n🎊 ¡Procesamiento masivo completado con éxito!")

        except Exception as e:
            self.log_queue.put(f"❌ Error crítico en el worker: {str(e)}")
            self.progress_queue.put(0)          

    def check_queues(self):
        """Revisar colas de logs y progreso de forma segura"""
        try:
            # Procesar logs
            while not self.log_queue.empty():
                message = self.log_queue.get_nowait()
                self.log_text.insert("end", message + "\n")
                self.log_text.see("end")

            # Procesar progreso
            while not self.progress_queue.empty():
                value = self.progress_queue.get_nowait()
                self.progress_bar.set(value)

        except queue.Empty:
            pass

        # Programar la próxima revisión de colas
        self.after(100, self.check_queues)

    def reset_demo(self):
        """Resetear entorno de demostración"""
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", "Logs limpiados. Listo para nuevo análisis.\n")
        self.progress_bar.set(0)


def main():
    """Punto de entrada de la aplicación"""
    app = SmartCVFilterApp()
    app.mainloop()

if __name__ == "__main__":
    main()