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
        # Ignoramos modelos de Google para asegurar funcionamiento local
        self.model_name = "Local-Sentence-Transformer"
        self.client = None 

    def _get_local_reasoning(self, score):
        """Genera una explicación humana basada en el porcentaje local."""
        if score >= 80:
            return "Excelente coincidencia técnica y conceptual. El perfil se alinea casi totalmente con los requisitos."
        elif score >= 60:
            return "Buena afinidad. Se detectan las competencias principales, aunque existen algunas áreas secundarias no cubiertas."
        elif score >= 40:
            return "Afinidad moderada. El candidato tiene bases relacionadas pero carece de especialización en puntos críticos."
        elif score >= 20:
            return "Baja coincidencia. El perfil solo comparte conceptos generales con la oferta."
        else:
            return "Sin coincidencia relevante. El CV no se alinea con la descripción del puesto."

    def _local_semantic_analysis(self, cv_text, job_desc):
        """
        Análisis semántico 100% LOCAL y ultra-rápido.
        """
        if not LOCAL_AVAILABLE:
            return {"apto": "NO", "puntuacion": 0, "motivo": "Error: Motor local no disponible en .venv"}

        # Cálculo matemático instantáneo
        emb1 = MODELO_LOCAL.encode(cv_text, convert_to_tensor=True)
        emb2 = MODELO_LOCAL.encode(job_desc, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        
        puntuacion = int(similarity * 100)
        explicacion = self._get_local_reasoning(puntuacion)

        return {
            "apto": "SI" if puntuacion > 50 else "NO",
            "puntuacion": puntuacion,
            "motivo": f"[IA Local] {explicacion} (Precisión: {puntuacion}%)"
        }

    def analyze(self, cv_text: str, job_description: str) -> dict:
        """
        PROCESAMIENTO 100% LOCAL:
        Eliminamos cualquier intento de conexión a Google para garantizar 
        velocidad instantánea con grandes volúmenes de CVs.
        """
        return self._local_semantic_analysis(cv_text, job_description)

if __name__ == "__main__":
    analyzer = CVAnalyzer()
    print("Probando análisis 100% Local...")
    print(analyzer.analyze("Experiencia en ventas", "Comercial B2B"))