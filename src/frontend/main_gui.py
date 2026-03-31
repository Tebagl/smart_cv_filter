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

    def update_top_candidates(self):
        """Limpia y rellena la lista de mejores candidatos desde la DB"""
        for widget in self.candidates_list.winfo_children():
            widget.destroy()

        try:
            limit = int(self.top_n_var.get())
            # Consultar la DB (Ordenado por score de mayor a menor)
            top_list = self.repo.get_top_candidates(limit=limit) 

            for person in top_list:
                # Mostramos el score guardado en la DB
                texto_boton = f"⭐ {person.lastName} | {person.score}%"
                
                btn = ctk.CTkButton(
                    self.candidates_list, 
                    text=texto_boton,
                    fg_color="#34495e",
                    hover_color="#1abc9c",
                    anchor="w",
                    # Al clickar, usamos person.address para abrir el archivo
                    command=lambda p=person: self.open_candidate_cv(p.address)
                )
                btn.pack(fill="x", pady=2, padx=5)
        except Exception as e:
            print(f"Error actualizando Top visual: {e}")

    def open_candidate_cv(self, file_path):
        """Intenta abrir el CV y avisa si el archivo ya no está ahí"""
        import os, subprocess, platform
        
        if not file_path or not os.path.exists(file_path):
            self.log_text.insert("end", "⚠️ El archivo original no se encuentra (¿Se quitó el pendrive o se movió?)\n")
            # Opcional: podrías abrir la carpeta de 'RECLUTADOS' como plan B
            return

        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.call(("open", file_path))
            else:
                subprocess.call(("xdg-open", file_path))
            
            self.log_text.insert("end", f"📂 Abriendo CV: {os.path.basename(file_path)}\n")
        except Exception as e:
            self.log_text.insert("end", f"❌ Error al abrir el archivo: {e}\n")

    def create_widgets(self):
        # Frame principal con un poco más de margen
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 1. SECTOR SUPERIOR: Configuración de la búsqueda
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        # Selector de carpeta (Ahora más compacto)
        folder_frame = ctk.CTkFrame(top_frame)
        folder_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(folder_frame, text="Carpeta de CVs:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        folder_entry = ctk.CTkEntry(folder_frame, textvariable=self.input_folder, width=350)
        folder_entry.pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(folder_frame, text="Seleccionar", width=100, command=self.select_input_folder).pack(side="right", padx=10)
    
        # --- SECCIÓN JOB DESCRIPTION (Ahora arriba y prioritaria) ---
        self.jd_label = ctk.CTkLabel(top_frame, text="📝 Requisitos de la Vacante (Job Description):", font=("Arial", 13, "bold"))
        self.jd_label.pack(anchor="w", padx=5)

        self.jd_textbox = ctk.CTkTextbox(top_frame, height=180, border_width=2) # Más alto
        self.jd_textbox.pack(fill="x", pady=5, padx=5)
        self.jd_textbox.insert("0.0", "Pegue aquí los requisitos de la vacante...")

        # 2. SECTOR CENTRAL: Botones de Acción
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)

        self.btn_analyze = ctk.CTkButton(
            button_frame, 
            text="🚀 INICIAR ANÁLISIS DE CVS", 
            font=("Arial", 14, "bold"),
            height=40,
            command=self.run_analysis
        )
        self.btn_analyze.pack(side="left", expand=True, fill="x", padx=(0, 5))

        ctk.CTkButton(
            button_frame, 
            text="Limpiar", 
            width=100,
            height=40,
            fg_color="#555555",
            command=self.reset_demo
        ).pack(side="right")

        # 3. SECTOR INFERIOR: Consola y Top Candidatos (Lado a lado)
        bottom_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        bottom_container.pack(fill="both", expand=True, padx=10, pady=10)

        # COLUMNA IZQUIERDA: Consola de logs
        console_frame = ctk.CTkFrame(bottom_container)
        console_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(console_frame, text="📊 Log de Procesamiento:", font=("Arial", 11, "italic")).pack(anchor="w", padx=10)
        self.log_text = ctk.CTkTextbox(console_frame, fg_color="#1a1a1a", text_color="#00ff00")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        

        # COLUMNA DERECHA: Top Selección
        top_candidates_frame = ctk.CTkFrame(bottom_container, width=250)
        top_candidates_frame.pack(side="right", fill="both", expand=False, padx=(5, 0))
        
        # Control del número de candidatos
        settings_frame = ctk.CTkFrame(top_candidates_frame, fg_color="transparent")
        settings_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(settings_frame, text="🏆 Top:", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        self.top_n_var = ctk.StringVar(value="15")
        self.top_n_entry = ctk.CTkEntry(settings_frame, textvariable=self.top_n_var, width=45)
        self.top_n_entry.pack(side="left")

        # Lista de candidatos (Scrollable)
        self.candidates_list = ctk.CTkScrollableFrame(top_candidates_frame, label_text="Mejores Candidatos")
        self.candidates_list.pack(fill="both", expand=True, padx=5, pady=5)

    def select_input_folder(self):
        """Usa plyer para un diálogo realmente nativo y moderno"""
        try:
            from plyer import filechooser
            
            # Abrir el selector de carpetas nativo del sistema
            path = filechooser.choose_dir(
                title="📂 Seleccionar Carpeta de Candidatos",
                initial_path=self.input_folder.get()
            )
            
            if path:
                # Path devuelve una lista, tomamos el primer elemento
                folder_selected = path[0]
                from pathlib import Path
                clean_path = str(Path(folder_selected).resolve())
                
                self.input_folder.set(clean_path)
                self.log_text.insert("end", f"📂 Carpeta actualizada: {clean_path}\n")
                self.log_text.see("end")
        except Exception as e:
            # Si plyer falla, usamos el de tkinter como respaldo (fallback)
            from tkinter import filedialog
            folder_selected = filedialog.askdirectory(parent=self)
            if folder_selected:
                self.input_folder.set(folder_selected)

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
            output_dir = Path(base_path) / 'src' / 'backend' / 'output'
            reclutados_dir = output_dir / 'RECLUTADOS'
            descartados_dir = output_dir / 'DESCARTADOS'
            
            reclutados_dir.mkdir(parents=True, exist_ok=True)
            descartados_dir.mkdir(parents=True, exist_ok=True)

            self.log_queue.put(f"📑 Encontrados {len(files)} archivos. Iniciando...")

            for i, file_path in enumerate(files):
                self.log_queue.put(f"🔍 Procesando: {file_path.name}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                except Exception as read_error:
                    self.log_queue.put(f"❌ Error al leer {file_path.name}: {read_error}")
                    continue

                # 🚀 ANALIZAR
                resultado = self.repo.process_cv(contenido, user_job_desc, file_path=str(file_path))
                
                if resultado.get("status") == "success":
                    estado = resultado.get('decision', 'ANALIZADO')
                    motivo = resultado.get('reason', 'Sin detalles')
                    
                    self.log_queue.put(f"   📢 ESTADO: {estado}")
                    self.log_queue.put(f"   📝 MOTIVO: {motivo}")

                    # LÓGICA DE MOVIMIENTO
                    if estado == "SI":
                        destino = reclutados_dir / file_path.name
                    else:
                        destino = descartados_dir / file_path.name

                    try:
                        file_path.replace(destino)
                        self.log_queue.put(f"   📂 Clasificado en: {destino.parent.name}")
                    except Exception as move_error:
                        self.log_queue.put(f"   ⚠️ Error al mover archivo: {move_error}")

                    self.log_queue.put("-" * 45)
                else:
                    self.log_queue.put(f"❌ Error en {file_path.name}: {resultado.get('reason')}")
                
                # Actualizar progreso
                progress = (i + 1) / len(files)
                self.progress_queue.put(progress)

            # ✨ ESTO VA FUERA DEL BUCLE FOR (Al terminar todo)
            self.log_queue.put("\n🎊 ¡Procesamiento masivo completado con éxito!")
            self.log_queue.put("COMMAND_UPDATE_TOP")

        except Exception as e:
            self.log_queue.put(f"❌ Error crítico en el worker: {str(e)}")
            self.progress_queue.put(0)          

    def check_queues(self):
        """Revisar colas de logs y progreso de forma segura"""
        try:
            # Procesar logs y comandos
            while not self.log_queue.empty():
                message = self.log_queue.get_nowait()
                
                if message == "COMMAND_UPDATE_TOP":
                    self.update_top_candidates()
                else:
                    self.log_text.insert("end", str(message) + "\n")
                    self.log_text.see("end")

            # Procesar progreso
            while not self.progress_queue.empty():
                value = self.progress_queue.get_nowait()
                self.progress_bar.set(value)

        except Exception as e:
            # Capturar cualquier error silencioso para que la App no muera
            print(f"Error en check_queues: {e}")

        # Programar la próxima revisión
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