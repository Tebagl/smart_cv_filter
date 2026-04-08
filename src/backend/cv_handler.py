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
        Analiza el CV y lo mueve físicamente según el score y guarda la razón.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()

            jd = user_job_desc if user_job_desc else "Perfil técnico general"
            decision = self.analyzer.analyze(raw_text, jd)
            
            # --- NUEVA LÓGICA DE EXTRACCIÓN (Score + Razón) ---
            f_score = 0
            reason = "No se pudo extraer una explicación detallada."
            texto_ia = str(decision)

            # 1. Extraer el score (primer número 0-100 que encuentre)
            numeros = re.findall(r'\b(?:\d{1,2}|100)\b', texto_ia)
            if numeros:
                f_score = int(numeros[0])
            
            # 2. Limpiar el motivo (quitar el formato JSON feo para el log)
            reason = texto_ia
            if '"motivo":' in texto_ia or "'motivo':" in texto_ia:
                match = re.search(r"['\"]motivo['\"]\s*:\s*['\"](.*?)['\"]", texto_ia, re.DOTALL)
                if match:
                    reason = match.group(1)
            else:
                reason = re.sub(r'^\d+[%]?\s*[:-]?\s*', '', texto_ia).strip()

            # --- Lógica de carpetas (Se mantiene igual) ---
            nombre_archivo = os.path.basename(file_path)
            if f_score >= 50:
                destino = "RECLUTADOS"
            elif 30 <= f_score < 50:
                destino = "DUDAS"
            else:
                destino = "DESCARTADOS"

            ruta_final = os.path.join(self.base_output, destino, nombre_archivo)
            if os.path.exists(file_path):
                shutil.move(file_path, ruta_final)

            return {
                "status": "success",
                "decision": destino,
                "score": f_score,
                "reason": reason,  
                "dest_path": ruta_final
            }

        except Exception as e:
            logger.error(f"❌ Error procesando {file_path}: {str(e)}")
            return {"status": "error", "reason": str(e)}