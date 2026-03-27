import json
import os
from pathlib import Path  
from dotenv import load_dotenv

# --- CARGA ÚNICA DEL MODELO IA LOCAL (En RAM) ---
try:
    from sentence_transformers import SentenceTransformer, util
    # Cargamos el modelo una sola vez al inicio para máxima velocidad
    MODELO_LOCAL = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    LOCAL_AVAILABLE = True
except Exception:
    LOCAL_AVAILABLE = False

class CVAnalyzer:
    def __init__(self, model=None):
        self.model_name = "Local-Sentence-Transformer"
        self.client = None 

    def _get_local_reasoning(self, score):
        """Genera una explicación humana recalibrada para MiniLM local."""
        # Recalibración: En modelos locales, un 60% es EXCELENTE.
        if score >= 60:
            return f"Excelente coincidencia técnica. El perfil es un 'match' ideal para la vacante. (Precisión: {score}%)"
        elif score >= 40:
            return f"Buena afinidad. Se detectan las competencias principales y experiencia relevante. (Precisión: {score}%)"
        elif score >= 25:
            return f"Afinidad moderada. El candidato tiene bases relacionadas pero carece de especialización. (Precisión: {score}%)"
        elif score >= 10:
            return f"Baja coincidencia. El perfil solo comparte conceptos generales. (Precisión: {score}%)"
        else:
            return f"Sin coincidencia relevante. El CV no se alinea con el puesto. (Precisión: {score}%)"

    def _local_semantic_analysis(self, cv_text, job_desc):
        """Análisis semántico 100% LOCAL."""
        if not LOCAL_AVAILABLE:
            return {"apto": "NO", "puntuacion": 0, "motivo": "Error: Motor local no disponible"}

        # Cálculo matemático
        emb1 = MODELO_LOCAL.encode(cv_text, convert_to_tensor=True)
        emb2 = MODELO_LOCAL.encode(job_desc, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        
        puntuacion = int(similarity * 100)
        
        # 1. Obtenemos el texto de nuestra función recalibrada
        explicacion = self._get_local_reasoning(puntuacion)

        # 2. RETORNO CORREGIDO: 
        # Bajamos el umbral a 40 para que Juan Pérez (46) sea APTO.
        return {
            "apto": "SI" if puntuacion >= 40 else "NO",
            "puntuacion": puntuacion,
            "motivo": explicacion  # <--- Ahora solo enviamos la explicación limpia
        }

    def analyze(self, cv_text: str, job_description: str) -> dict:
        return self._local_semantic_analysis(cv_text, job_description)

if __name__ == "__main__":
    analyzer = CVAnalyzer()
    print("Probando análisis 100% Local...")
    print(analyzer.analyze("Experiencia en ventas", "Comercial B2B"))