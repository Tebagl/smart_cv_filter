import re
import os
import sys

def get_model_path():
    """Determina la ruta del modelo tanto en desarrollo como en ejecutable."""
    if getattr(sys, 'frozen', False):
        # Si es el ejecutable de PyInstaller, busca dentro de _internal
        return os.path.join(sys._MEIPASS, "models", "cv_model")
    else:
        # Si estás ejecutando desde VS Code
        return os.path.join(os.getcwd(), "models", "cv_model")

# Solo importamos lo que usamos para que el .exe sea ligero
try:
    from sentence_transformers import SentenceTransformer, util
    ruta_ia = get_model_path()
    
    # Intentamos cargar el modelo desde la carpeta física
    MODELO_LOCAL = SentenceTransformer(ruta_ia)
    LOCAL_AVAILABLE = True
    print(f"Motor IA cargado correctamente desde: {ruta_ia}")
except Exception as e:
    print(f"Error al cargar el motor IA: {e}")
    LOCAL_AVAILABLE = False

class CVAnalyzer:
    def __init__(self, model=None):
        self.model_name = "Local-Semantic-Keyword-Hybrid-V2"

    def extract_keywords_español(self, text):
        text_clean = text.lower().replace('\n', ' ')
        negaciones = [
            r"no tiene experiencia en", r"no conoce", r"sin experiencia en",
            r"falta de experiencia en", r"no domina", r"no tengo",
            r"ninguna experiencia con", r"no cuenta con"
        ]
        for neg in negaciones:
            patron = f"{neg}[^.,;]+"
            text_clean = re.sub(patron, " [NEGADO] ", text_clean)

        words = re.findall(r'\b\w{4,}\b', text_clean)
        return set([w for w in words if w != "negado"])

    def _get_dynamic_reason(self, coincidencias, score):
        top_matches = list(coincidencias)[:6] 
        if score >= 70:
            if top_matches:
                return f"Match sólido ({score}%). Coincidencias clave: {', '.join(top_matches)}."
            return f"Afinidad semántica alta ({score}%). Perfil alineado con los requisitos."
        if score >= 50:
            if top_matches:
                return f"Perfil con potencial ({score}%). Menciona términos como: {', '.join(top_matches)}."
            return f"Afinidad moderada ({score}%). El perfil no especifica suficientes términos clave del puesto."
        return f"Baja afinidad ({score}%). No se alinea con los requisitos del puesto."

    def _local_semantic_analysis(self, cv_text, job_desc):
        if not LOCAL_AVAILABLE:
            return {"apto": "NO", "puntuacion": 0, "motivo": "Error: Motor IA no disponible"}

        cv_words = self.extract_keywords_español(cv_text)
        jd_words = self.extract_keywords_español(job_desc)
        coincidencias = jd_words.intersection(cv_words)
        
        emb1 = MODELO_LOCAL.encode(cv_text, convert_to_tensor=True)
        emb2 = MODELO_LOCAL.encode(job_desc, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        puntuacion_base = int(similarity * 100)
        
        bonus = len(coincidencias) * 3
        penalizacion = 0
        if len(coincidencias) == 0 and puntuacion_base < 45:
            penalizacion = 15

        puntuacion_final = max(0, min(puntuacion_base + bonus - penalizacion, 99))
        
        return {
            "apto": "SI" if puntuacion_final >= 50 else "NO",
            "puntuacion": puntuacion_final,
            "motivo": self._get_dynamic_reason(coincidencias, puntuacion_final)
        }

    def analyze(self, cv_text: str, job_description: str) -> dict:
        return self._local_semantic_analysis(cv_text, job_description)