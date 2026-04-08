import re
# Solo importamos lo que usamos para que el .exe sea ligero
try:
    from sentence_transformers import SentenceTransformer, util
    MODELO_LOCAL = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    LOCAL_AVAILABLE = True
except Exception:
    LOCAL_AVAILABLE = False

class CVAnalyzer:
    def __init__(self, model=None):
        self.model_name = "Local-Semantic-Keyword-Hybrid-V2"

    
    def extract_keywords_español(self, text):
        """
        Limpia negaciones hasta el final de la frase
        para evitar falsos positivos en textos largos.
        """
        # 1. Normalización básica
        text_clean = text.lower().replace('\n', ' ')

        # 2. Disparadores de negación más amplios
        negaciones = [
            r"no tiene experiencia en", 
            r"no conoce", 
            r"sin experiencia en",
            r"falta de experiencia en",
            r"no domina",
            r"no tengo",
            r"ninguna experiencia con",
            r"no cuenta con"
        ]

        # 3. Borrado por bloques de frase:
        # Este regex busca la negación y TODO lo que sigue hasta encontrar 
        # un punto, una coma, un punto y coma o el final de la línea.
        for neg in negaciones:
            # patron: busca la negación + cualquier caracter que NO sea un signo de puntuación
            patron = f"{neg}[^.,;]+"
            text_clean = re.sub(patron, " [NEGADO] ", text_clean)

        # 4. Extraer palabras de más de 3 letras
        words = re.findall(r'\b\w{4,}\b', text_clean)
        return set([w for w in words if w != "negado"])

    def _get_dynamic_reason(self, coincidencias, score):
        """Genera el motivo basándose en las coincidencias encontradas."""
        top_matches = list(coincidencias)[:6] 

        if score >= 70:
            if top_matches:
                return f"Match sólido ({score}%). Coincidencias clave: {', '.join(top_matches)}."
            return f"Afinidad semántica alta ({score}%). Perfil alineado con los requisitos."
        
        if score >= 50:
            # CAMBIO AQUÍ: Si hay términos, los mostramos. Si no, damos un mensaje genérico profesional.
            if top_matches:
                return f"Perfil con potencial ({score}%). Menciona términos como: {', '.join(top_matches)}."
            return f"Afinidad moderada ({score}%). El perfil no especifica suficientes términos clave del puesto."
        
        return f"Baja afinidad ({score}%). No se alinea con los requisitos del puesto."

    def _local_semantic_analysis(self, cv_text, job_desc):
        if not LOCAL_AVAILABLE:
            return {"apto": "NO", "puntuacion": 0, "motivo": "Error: Motor IA no disponible"}

        # 1. Extraer palabras (Usando el nombre correcto de la función)
        cv_words = self.extract_keywords_español(cv_text)
        jd_words = self.extract_keywords_español(job_desc)
        coincidencias = jd_words.intersection(cv_words)
        
        # 2. IA Semántica
        emb1 = MODELO_LOCAL.encode(cv_text, convert_to_tensor=True)
        emb2 = MODELO_LOCAL.encode(job_desc, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        puntuacion_base = int(similarity * 100)
        
        # 3. Ajuste de precisión
        bonus = len(coincidencias) * 3
        
        # Penalización si no hay ni una palabra en común (filtro estricto)
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