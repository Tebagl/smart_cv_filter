import json
import os
import re
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
        self.model_name = "Local-Semantic-Keyword-Hybrid"

    def _extract_keywords(self, text):
        """Extrae palabras importantes (más de 3 letras) para comparar."""
        # Limpiamos puntuación y pasamos a minúsculas
        words = re.findall(r'\b\w{4,}\b', text.lower())
        return set(words)

    def _get_dynamic_reason(self, cv_words, jd_words, score): # Cambiamos los argumentos
        # Encontramos qué palabras clave de la oferta están en el CV
        coincidencias = jd_words.intersection(cv_words)
        top_matches = list(coincidencias)[:6] 

        if score >= 50:
            msg = f"Match sólido ({score}%). Detectado: {', '.join(top_matches)}."
        elif score >= 30:
            msg = f"Perfil con potencial ({score}%). Tiene {', '.join(top_matches)} pero el texto global difiere."
        else:
            msg = f"Baja afinidad ({score}%). Faltan demasiadas tecnologías clave."
        
        return msg, coincidencias

    def _local_semantic_analysis(self, cv_text, job_desc):
        if not LOCAL_AVAILABLE:
            return {"apto": "NO", "puntuacion": 0, "motivo": "Error: Motor local disponible"}

        # 1. Extraer palabras para el "empujón" técnico
        cv_words = self._extract_keywords(cv_text)
        jd_words = self._extract_keywords(job_desc)
        
        # 2. Cálculo matemático base
        emb1 = MODELO_LOCAL.encode(cv_text, convert_to_tensor=True)
        emb2 = MODELO_LOCAL.encode(job_desc, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        puntuacion_base = int(similarity * 100)
        
        # 3. EL EMPUJÓN (Bonus por keywords técnicas)
        # Si tiene tecnologías clave, subimos el score para que pase el corte de 50
        coincidencias = jd_words.intersection(cv_words)
        bonus = len(coincidencias) * 3  # 3 puntos extra por cada palabra clave compartida
        puntuacion_final = min(puntuacion_base + bonus, 99) # Máximo 99
        
        # 4. Generación de motivo con la nueva puntuación
        explicacion, _ = self._get_dynamic_reason(cv_words, jd_words, puntuacion_final)

        return {
            "apto": "SI" if puntuacion_final >= 50 else "NO",
            "puntuacion": puntuacion_final,
            "motivo": explicacion 
        }

    def analyze(self, cv_text: str, job_description: str) -> dict:
        return self._local_semantic_analysis(cv_text, job_description)
    
if __name__ == "__main__":
    analyzer = CVAnalyzer()
    print("Probando análisis 100% Local...")
    print(analyzer.analyze("Experiencia en ventas", "Comercial B2B"))