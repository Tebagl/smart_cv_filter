import os
import sys
import threading
import logging
import tkinter
import customtkinter as ctk
from pathlib import Path
import queue
import platform
import subprocess

# --- Configuración de Rutas ---
def get_base_path():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return base_path

base_path = get_base_path()
sys.path.insert(0, base_path)

# Importar el nuevo CVHandler (Sin base de datos)
from src.backend.cv_handler import CVHandler
from src.backend.analyzer import CVAnalyzer # Asegúrate de tenerlo importado

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartCVFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 🚀 NUEVA CONEXIÓN: Sistema de Carpetas
        # Inicializamos el analizador y el handler sin base de datos
        self.analyzer = CVAnalyzer() 
        self.cv_handler = CVHandler(self.analyzer)
        
        # Ruta donde la GUI leerá los candidatos destacados
        self.results_dir = os.path.join(base_path, "src", "backend", "output", "RECLUTADOS")

        # Configuración de la ventana
        self.title("Smart CV Filter - Folder Edition")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Colas de comunicación
        self.log_queue = queue.Queue()
        
        # Variables de ruta
        default_inputs_path = os.path.join(base_path,'src', 'backend', 'inputs')
        self.input_folder = ctk.StringVar(value=default_inputs_path)

        self.create_widgets()
        self.after(100, self.check_queues)
        
        # Cargar lista inicial si ya existen resultados
        self.update_top_candidates()

    def update_top_candidates(self):
        """Lee la carpeta física de 'reclutados' y genera los botones"""
        for widget in self.candidates_list.winfo_children():
            widget.destroy()

        if not os.path.exists(self.results_dir):
            return

        try:
            # Listamos los archivos en la carpeta de resultados
            archivos = [f for f in os.listdir(self.results_dir) if f.endswith('.txt')]
            
            # Limitamos según el número del "Top" en la GUI
            try:
                limit = int(self.top_n_var.get())
                archivos = archivos[:limit]
            except:
                pass

            for nombre in archivos:
                ruta_completa = os.path.join(self.results_dir, nombre)
                
                btn = ctk.CTkButton(
                    self.candidates_list, 
                    text=f"📄 {nombre}",
                    fg_color="#2c3e50",
                    hover_color="#1abc9c",
                    anchor="w",
                    command=lambda r=ruta_completa: self.open_candidate_cv(r)
                )
                btn.pack(fill="x", pady=2, padx=5)
        except Exception as e:
            logger.error(f"Error actualizando lista visual: {e}")

    def open_candidate_cv(self, file_path):
        """Abre el archivo con el visor predeterminado del sistema"""
        if not os.path.exists(file_path):
            self.log_text.insert("end", f"⚠️ Archivo no encontrado: {file_path}\n")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.call(("open", file_path))
            else:
                subprocess.call(("xdg-open", file_path))
        except Exception as e:
            self.log_text.insert("end", f"❌ Error al abrir: {e}\n")

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # SECTOR SUPERIOR
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        folder_frame = ctk.CTkFrame(top_frame)
        folder_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(folder_frame, text="Carpeta de entrada:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkEntry(folder_frame, textvariable=self.input_folder, width=350).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(folder_frame, text="Explorar", width=100, command=self.select_input_folder).pack(side="right", padx=10)
    
        ctk.CTkLabel(top_frame, text="📝 Job Description:", font=("Arial", 13, "bold")).pack(anchor="w", padx=5)
        self.jd_textbox = ctk.CTkTextbox(top_frame, height=150, border_width=2)
        self.jd_textbox.pack(fill="x", pady=5, padx=5)
        self.jd_textbox.insert("0.0", "Requisitos del puesto...")

        # BOTONES
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)

        self.btn_analyze = ctk.CTkButton(button_frame, text="🚀 CLASIFICAR CVS", font=("Arial", 14, "bold"), height=40, command=self.run_analysis)
        self.btn_analyze.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # INFERIOR: Consola y Lista
        bottom_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        bottom_container.pack(fill="both", expand=True, padx=10, pady=10)

        console_frame = ctk.CTkFrame(bottom_container)
        console_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.log_text = ctk.CTkTextbox(console_frame, fg_color="#1a1a1a", text_color="#00ff00")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        top_candidates_frame = ctk.CTkFrame(bottom_container, width=250)
        top_candidates_frame.pack(side="right", fill="both", expand=False, padx=(5, 0))
        
        self.top_n_var = ctk.StringVar(value="15")
        self.candidates_list = ctk.CTkScrollableFrame(top_candidates_frame, label_text="CVs Aceptados (Carpeta)")
        self.candidates_list.pack(fill="both", expand=True, padx=5, pady=5)

    def select_input_folder(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.input_folder.set(path)

    def run_analysis(self):
        self.log_text.delete("1.0", "end")
        user_description = self.jd_textbox.get("0.0", "end").strip()
        
        thread = threading.Thread(target=self.analysis_worker, args=(user_description,), daemon=True)
        thread.start()
        
    def analysis_worker(self, user_job_desc):
        """Usa el nuevo CVHandler para mover archivos físicamente"""
        try:
            folder_path = Path(self.input_folder.get())
            files = list(folder_path.glob("*.txt"))
            
            if not files:
                self.log_queue.put("⚠️ No hay archivos .txt en la carpeta seleccionada.")
                return

            self.log_queue.put(f"📑 Procesando {len(files)} candidatos...")

            for file_path in files:
                self.log_queue.put(f"🔍 Analizando: {file_path.name}")
                
                # Llamamos al handler (que ahora mueve el archivo)
                resultado = self.cv_handler.process_cv(str(file_path), user_job_desc)
                
                if resultado.get("status") == "success":
                    self.log_queue.put(f"   ✅ Score: {resultado['score']}% -> {resultado['decision']}")
                else:
                    self.log_queue.put(f"   ❌ Error: {resultado.get('reason')}")
                
                self.log_queue.put("-" * 30)

            self.log_queue.put("\n🎊 ¡Clasificación terminada!")
            self.log_queue.put("UPDATE_LIST")

        except Exception as e:
            self.log_queue.put(f"❌ Error crítico: {e}")

    def check_queues(self):
        try:
            while not self.log_queue.empty():
                msg = self.log_queue.get_nowait()
                if msg == "UPDATE_LIST":
                    self.update_top_candidates()
                else:
                    self.log_text.insert("end", f"{msg}\n")
                    self.log_text.see("end")
        except:
            pass
        self.after(100, self.check_queues)

if __name__ == "__main__":
    app = SmartCVFilterApp()
    app.mainloop()