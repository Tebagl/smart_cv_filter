import os
import shutil
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class CVHandler:
    def __init__(self, analyzer):
        """
        Manejador de CVs para sistema de carpetas e IA Embebida.
        """
        self.analyzer = analyzer
        # Definimos la ruta base de salida relativa a este archivo
        self.base_output = os.path.join(os.path.dirname(__file__), "output")
        self._ensure_folders()

    def _ensure_folders(self):
        """Crea la estructura de carpetas física si no existe"""
        # IMPORTANTE: Estos nombres deben coincidir con los que busca la GUI
        folders = ["RECLUTADOS", "DUDAS", "DESCARTADOS"]
        for f in folders:
            path = os.path.join(self.base_output, f)
            os.makedirs(path, exist_ok=True)
            logger.info(f"📁 Carpeta verificada: {path}")

    def process_cv(self, file_path: str, user_job_desc: str = None):
        """
        Analiza el CV y lo mueve físicamente según el score de la IA.
        """
        try:
            # 1. Leer el contenido del archivo .txt
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()

            # 2. Analizar con la IA Embebida
            jd = user_job_desc if user_job_desc else "Perfil técnico general"
            decision = self.analyzer.analyze(raw_text, jd)
            
            # DEBUG: Esto aparecerá en tu terminal para ver qué responde la IA realmente
            print(f"\n--- DEBUG IA LOCAL ---")
            print(f"Archivo: {os.path.basename(file_path)}")
            print(f"Tipo respuesta: {type(decision)}")
            print(f"Contenido: {decision}")
            print(f"----------------------\n")

            # 3. Extraer puntuación (Score) de forma robusta
            import re
            f_score = 0
            # Convertimos la respuesta de la IA a string y buscamos números
            texto_ia = str(decision)
            numeros = re.findall(r'\d+', texto_ia)
            
            if numeros:
                # Buscamos un número que tenga sentido como score (0-100)
                for n in numeros:
                    val = int(n)
                    if 0 <= val <= 100:
                        f_score = val
                        break

            # 4. Lógica de clasificación por carpetas
            nombre_archivo = os.path.basename(file_path)
            
            if f_score >= 50:
                destino = "RECLUTADOS"
            elif 30 <= f_score < 50:
                destino = "DUDAS"
            else:
                destino = "DESCARTADOS"

            # 5. Mover el archivo físicamente (shutil.move limpia la entrada)
            ruta_final = os.path.join(self.base_output, destino, nombre_archivo)
            
            # Verificamos si el archivo existe antes de mover (evita errores)
            if os.path.exists(file_path):
                shutil.move(file_path, ruta_final)
                logger.info(f"✅ {nombre_archivo} movido a {destino} (Score: {f_score}%)")
            else:
                logger.warning(f"⚠️ El archivo ya no existe en la ruta: {file_path}")

            return {
                "status": "success",
                "decision": destino,
                "score": f_score,
                "dest_path": ruta_final
            }

        except Exception as e:
            logger.error(f"❌ Error procesando {file_path}: {str(e)}")
            return {"status": "error", "reason": str(e)}