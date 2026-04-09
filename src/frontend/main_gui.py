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
# --- Configuración de Rutas ---
def get_resource_path():
    """Ruta para archivos internos (modelos, código empaquetado)"""
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        return sys._MEIPASS
    except Exception:
        # Si ejecutamos el .py normalmente
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_executable_path():
    """Ruta donde reside el archivo .exe o el binario (para carpetas de salida)"""
    if getattr(sys, 'frozen', False):
        # Si es el ejecutable, queremos la carpeta donde está el archivo físico
        return os.path.dirname(sys.executable)
    # Si es modo desarrollo, usamos la raíz del proyecto
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Definimos las dos rutas críticas
resource_path = get_resource_path()    # Para buscar 'models'
executable_path = get_executable_path() # Para crear 'procesos_seleccion'

# Importante: los imports del backend deben buscarse en resource_path
sys.path.insert(0, resource_path)

# Importar el backend
from src.backend.cv_handler import CVHandler
from src.backend.analyzer import CVAnalyzer
from src.backend.process_manager import ProcessManager

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SmartCVFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 🚀 Inicialización de Backend
        self.analyzer = CVAnalyzer() 
        self.cv_handler = CVHandler(self.analyzer)
        self.process_manager = ProcessManager(executable_path, self.cv_handler)
        
        self.results_dir = "" # Se llenará al dar a Clasificar
        
        # Ruta de resultados (Asegúrate de que coincida con RECLUTADOS en mayúsculas)
        #self.results_dir = os.path.join(base_path, "src", "backend", "output", "RECLUTADOS")

        # Configuración de la ventana
        self.title("Smart CV Filter")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Colas de comunicación
        self.log_queue = queue.Queue()
        
       # Variables de ruta inicializadas vacías
        self.input_folder = ctk.StringVar(value="")

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
            # 1. Obtenemos la lista de archivos
            archivos = [f for f in os.listdir(self.results_dir) 
                       if f.lower().endswith(('.txt', '.pdf', '.docx'))]
            
            # 2. ORDENAR: Al tener el score al principio (ej: "95_cv..."), 
            # sort(reverse=True) pondrá los más altos arriba automáticamente.
            archivos.sort(reverse=True)
            
            for nombre in archivos:
                ruta_completa = os.path.join(self.results_dir, nombre)
                
                # Opcional: Limpiar el nombre para la interfaz (quitar el prefijo del score)
                # si quieres que se vea más limpio, aunque dejarlo ayuda a confirmar el orden.
                display_name = nombre 

                btn = ctk.CTkButton(
                    self.candidates_list, 
                    text=f"⭐ {display_name}",
                    fg_color="#34495e",
                    hover_color="#1f538d",
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
            elif platform.system() == "Darwin": # macOS
                subprocess.call(("open", file_path))
            else: # 🐧 Linux (Aquí es donde estaba el problema)
                # 🛡️ "Limpiamos" las librerías internas antes de llamar al sistema
                env = dict(os.environ)
                # Eliminamos la ruta de librerías de PyInstaller para este proceso
                if "LD_LIBRARY_PATH" in env:
                    del env["LD_LIBRARY_PATH"]
                
                # Ejecutamos xdg-open con el entorno limpio
                subprocess.Popen(["xdg-open", file_path], env=env)
                
        except Exception as e:
            self.log_text.insert("end", f"❌ Error al abrir: {e}\n")
    def select_input_folder(self):
        from tkinter import filedialog
        import os
        
        # 1. Localizamos la ruta del Escritorio de forma dinámica
        # Esto funciona en Windows, macOS y Linux
        desktop_path = os.path.join(os.path.expanduser("~"), "Documents")
        
        # 2. Verificamos si existe (por si el SO tiene un nombre distinto)
        if not os.path.exists(desktop_path):
            desktop_path = os.path.expanduser("~") # Si no hay escritorio, abre su carpeta personal

        # 3. Abrimos el buscador empezando en el escritorio (initialdir)
        path = filedialog.askdirectory(
            initialdir=desktop_path,
            title="Selecciona la carpeta con los CVs"
        )
        
        if path:
            self.input_folder.set(path)


    def run_analysis(self):
        puesto = self.entry_puesto.get().strip()
        fecha = self.entry_fecha.get().strip()
        folder_path = self.input_folder.get().strip()
        user_description = self.jd_textbox.get("0.0", "end").strip() # Obtenemos la JD

        # Validaciones simples de UI
        if not folder_path or not puesto or not user_description:
            self.log_text.insert("end", "⚠️ ERROR: Faltan datos obligatorios (Carpeta, Puesto o Descripción).\n")
            return

        # 🎯 CAPTURAMOS AMBAS RUTAS
        main_folder, self.results_dir = self.process_manager.configure_process(puesto, fecha)

        # 💾 GUARDAMOS LA DESCRIPCIÓN en la carpeta raíz
        self.process_manager.save_job_description(main_folder, user_description)

        # Bloquear botón e iniciar hilo
        self.btn_analyze.configure(state="disabled")
        threading.Thread(target=self.analysis_worker, args=(user_description,), daemon=True).start()
        

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