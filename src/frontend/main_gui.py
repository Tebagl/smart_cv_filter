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
from src.backend.analyzer import CVAnalyzer

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartCVFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 🚀 Inicialización de Backend
        self.analyzer = CVAnalyzer() 
        self.cv_handler = CVHandler(self.analyzer)
        
        # Ruta de resultados (Asegúrate de que coincida con RECLUTADOS en mayúsculas)
        self.results_dir = os.path.join(base_path, "src", "backend", "output", "RECLUTADOS")

        # Configuración de la ventana
        self.title("Smart CV Filter - Folder Edition")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Colas de comunicación
        self.log_queue = queue.Queue()
        
        # Variables de ruta por defecto
        default_inputs_path = os.path.join(base_path, 'src', 'backend', 'inputs')
        self.input_folder = ctk.StringVar(value=default_inputs_path)

        # Crear Interfaz
        self.create_widgets()
        
        # Iniciar bucle de revisión de colas
        self.after(100, self.check_queues)
        
        # Cargar lista inicial
        self.update_top_candidates()

    def create_widgets(self):
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- NUEVA SECCIÓN: DATOS DEL PROCESO ---
        process_info_frame = ctk.CTkFrame(main_frame)
        process_info_frame.pack(fill="x", padx=10, pady=5)

        # Campo Título
        ctk.CTkLabel(process_info_frame, text="📌 Puesto:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.entry_puesto = ctk.CTkEntry(process_info_frame, placeholder_text="Ej: Senior Data Engineer", width=200)
        self.entry_puesto.pack(side="left", padx=5)

        # Campo Fecha (por defecto hoy)
        from datetime import datetime
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        ctk.CTkLabel(process_info_frame, text="📅 Fecha:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.entry_fecha = ctk.CTkEntry(process_info_frame, width=120)
        self.entry_fecha.insert(0, fecha_hoy)
        self.entry_fecha.pack(side="left", padx=5)

        # --- SECCIÓN 1: CARPETA DE ENTRADA (ARRIBA) ---
        folder_frame = ctk.CTkFrame(main_frame)
        folder_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(folder_frame, text="📂 Carpeta de entrada:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkEntry(folder_frame, textvariable=self.input_folder, width=350).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(folder_frame, text="Explorar", width=100, command=self.select_input_folder).pack(side="right", padx=10)

        # --- SECCIÓN 2: CONTENEDOR MEDIO (COLUMNAS) ---
        mid_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        mid_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configuramos el peso de las columnas (60% izquierda, 40% derecha)
        mid_container.columnconfigure(0, weight=6)
        mid_container.columnconfigure(1, weight=4)
        mid_container.rowconfigure(0, weight=1)

        # --- COLUMNA IZQUIERDA (JD + BOTÓN) ---
        left_column = ctk.CTkFrame(mid_container, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        ctk.CTkLabel(left_column, text="📝 Descripción del puesto:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 5))
        
        # Textbox de JD
        self.jd_textbox = ctk.CTkTextbox(left_column, border_width=2)
        self.jd_textbox.pack(fill="both", expand=True, pady=(0, 10))
        
        # Menú de clic derecho
        self.menu_pegar = tkinter.Menu(self, tearoff=0, bg="#2b2b2b", fg="white", activebackground="#1f538d", bd=0)
        self.menu_pegar.add_command(label="  📋 Pegar Texto  ", command=self.pegar_texto)
        self.jd_textbox.bind("<Button-3>", self.mostrar_menu)

        # Botón Clasificar (Debajo de la JD)
        self.btn_analyze = ctk.CTkButton(
            left_column, 
            text="🚀 CLASIFICAR CVS", 
            font=("Arial", 14, "bold"), 
            height=45, 
            command=self.run_analysis
        )
        self.btn_analyze.pack(fill="x")

        # --- COLUMNA DERECHA (CVS ACEPTADOS) ---
        right_column = ctk.CTkFrame(mid_container)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.candidates_list = ctk.CTkScrollableFrame(right_column, label_text="CVs Aceptados")
        self.candidates_list.pack(fill="both", expand=True, padx=5, pady=5)

        # --- SECCIÓN 3: CONSOLA DE LOGS (ABAJO) ---
        console_frame = ctk.CTkFrame(main_frame)
        console_frame.pack(fill="x", side="bottom", padx=10, pady=(5, 10))
        
        ctk.CTkLabel(console_frame, text="🖥️ Log de procesamiento:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        self.log_text = ctk.CTkTextbox(console_frame, height=120, fg_color="#1a1a1a", text_color="#00ff00", font=("Courier", 12))
        self.log_text.pack(fill="x", padx=10, pady=10)

    # --- Funciones de Soporte para Clic Derecho ---
    def mostrar_menu(self, event):
        """Muestra el menú con un pequeño margen para evitar clics accidentales"""
        try:
            # Añadimos +2 píxeles de margen en X e Y. 
            # Esto separa el cursor de la primera opción del menú.
            self.menu_pegar.tk_popup(event.x_root + 2, event.y_root + 2)
        finally:
            # Esto asegura que el menú libere el "foco" correctamente
            self.menu_pegar.grab_release()

    def pegar_texto(self):
        """Pega el texto asegurándose de limpiar el portapapeles de caracteres extra"""
        try:
            # Obtenemos el contenido del portapapeles
            texto = self.clipboard_get()
            if texto:
                # Insertamos en la posición actual del cursor ("insert")
                self.jd_textbox.insert("insert", texto)
                # Opcional: Desplazar la vista al final del texto pegado
                self.jd_textbox.see("end")
        except Exception as e:
            # Si el portapapeles no tiene texto (ej. una imagen), no hace nada
            pass

    # --- Lógica de la Aplicación ---
    def update_top_candidates(self):
        # Limpiamos la lista actual
        for widget in self.candidates_list.winfo_children():
            widget.destroy()

        if not os.path.exists(self.results_dir):
            return

        try:
            # CAMBIO CLAVE: Ahora aceptamos .txt y .pdf (ignorando mayúsculas/minúsculas)
            archivos = [f for f in os.listdir(self.results_dir) 
            if f.lower().endswith(('.txt', '.pdf', '.docx'))]
            
            for nombre in archivos:
                ruta_completa = os.path.join(self.results_dir, nombre)
                btn = ctk.CTkButton(
                    self.candidates_list, 
                    text=f"📄 {nombre}",
                    fg_color="#34495e", # Un tono grisáceo elegante
                    hover_color="#1f538d", # Azul al pasar el ratón
                    anchor="w",
                    command=lambda r=ruta_completa: self.open_candidate_cv(r)
                )
                btn.pack(fill="x", pady=2, padx=5)
                
        except Exception as e:
            logger.error(f"Error actualizando lista visual: {e}")

    def open_candidate_cv(self, file_path):
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

    def select_input_folder(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.input_folder.set(path)

    def run_analysis(self):
        puesto = self.entry_puesto.get().strip().replace(" ", "_")
        fecha = self.entry_fecha.get().strip()
        
        if not puesto:
            self.log_text.insert("end", "⚠️ Por favor, introduce el nombre del puesto.\n")
            return

        # Creamos la ruta dinámica
        nombre_carpeta = f"{fecha}_{puesto}"
        ruta_proceso = os.path.join(base_path, "Procesos", nombre_carpeta)
        
        # Actualizamos el handler con la nueva ruta de salida
        self.cv_handler.base_output = os.path.join(ruta_proceso, "output")
        self.cv_handler._ensure_folders() # Crea RECLUTADOS, DUDAS, etc.
        
        # Actualizamos donde la GUI mira los resultados
        self.results_dir = os.path.join(ruta_proceso, "output", "RECLUTADOS")

        # Ejecutamos el hilo como antes
        user_description = self.jd_textbox.get("0.0", "end").strip()
        self.btn_analyze.configure(state="disabled")
        
        thread = threading.Thread(target=self.analysis_worker, args=(user_description,), daemon=True)
        thread.start()
        
    def analysis_worker(self, user_job_desc):
        try:

            folder_path = Path(self.input_folder.get())
            extensiones = [".txt", ".pdf", ".docx"]
            files = [f for f in folder_path.iterdir() if f.suffix.lower() in extensiones]
           
            if not files:
                self.log_queue.put("⚠️ No se encontraron archivos (PDF, DOCX, TXT) en la carpeta seleccionada.")
                self.log_queue.put("FIN")
                return

            self.log_queue.put(f"📑 Procesando {len(files)} candidatos...")

            for file_path in files:
                self.log_queue.put(f"🔍 Analizando: {file_path.name}")
                
                resultado = self.cv_handler.process_cv(str(file_path), user_job_desc)
                
                if resultado.get("status") == "success":
                    self.log_queue.put(f"   ✅ Score: {resultado['score']}% -> {resultado['decision']}")
                    # --- AQUÍ SE MUESTRA EL MOTIVO ---
                    self.log_queue.put(f"   💡 Motivo: {resultado['reason']}")
                else:
                    self.log_queue.put(f"   ❌ Error: {resultado.get('reason')}")
                
                self.log_queue.put("-" * 40) # Una línea separadora un poco más larga

            self.log_queue.put("\n🎊 ¡Clasificación terminada!")
            self.log_queue.put("UPDATE_LIST")
            self.log_queue.put("FIN")

        except Exception as e:
            self.log_queue.put(f"❌ Error crítico: {e}")
            self.log_queue.put("FIN")
            
    def check_queues(self):
        try:
            while not self.log_queue.empty():
                msg = self.log_queue.get_nowait()
                if msg == "UPDATE_LIST":
                    self.update_top_candidates()
                elif msg == "FIN":
                    self.btn_analyze.configure(state="normal")
                else:
                    self.log_text.insert("end", f"{msg}\n")
                    self.log_text.see("end")
        except:
            pass
        self.after(100, self.check_queues)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_widget_scaling(1.0)  # Fuerza escala 1:1
    app = SmartCVFilterApp()
    app.mainloop()