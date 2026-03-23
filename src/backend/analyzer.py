import json
import os
import sys
import re
import time

# Attempt to import Gemini, with fallback
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class CVAnalyzer:
    """
    Módulo 3: Evaluación Semántica (LLM)
    Realiza una evaluación razonada del CV anonimizado contra la vacante
    utilizando la API de Google Gemini (modelos orientados a chat), devolviendo
    una estructura JSON predecible.
    """
    def __init__(self, model="gemini-2.5-flash"):
        self.model_name = model
        self.model = None
        
        # Check if Gemini is available and API key is set
        if GEMINI_AVAILABLE:
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
                try:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel(self.model_name)
                except Exception as e:
                    print(f"[WARNING] Could not initialize Gemini model: {e}")
            else:
                print("[WARNING] Gemini API key not configured. Using fallback evaluation.")
        else:
            print("[WARNING] Google Generative AI library not installed. Using fallback evaluation.")

    def _extract_keywords(self, text):
        """
        Extract meaningful keywords from text, removing common stop words.
        """
        # Basic list of stop words in Spanish and English
        stop_words = set(['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 
                          'de', 'del', 'al', 'con', 'por', 'para', 'en', 'y', 'o', 
                          'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'])
        
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Split into words and filter out stop words
        keywords = [word for word in text.split() if word not in stop_words and len(word) > 2]
        
        return keywords

    def analyze(self, cv_text: str, job_description: str) -> dict:
        """
        Perform semantic analysis of the CV against the job description.
        Falls back to a simple keyword-based matching if Gemini is not available.
        """
        # Add a small pause between analyses to respect API rate limits
        time.sleep(5)

        # If Gemini model is available, try to use it first
        if self.model:
            try:
                prompt = f"""
Eres un reclutador experto y analista de talento. Evalúa el CV contra la descripción de la vacante usando una rúbrica estricta de 3 criterios:

1. Experiencia en Ventas B2B / Account Executive (40%):
   - Mínimo 3 años de experiencia directa
   - Historial demostrable en ventas B2B
   - Roles específicos en Account Executive o equivalentes

2. Habilidades de Comunicación y Cierre de Contratos (30%):
   - Capacidad de comunicación efectiva
   - Historial de negociación y cierre de contratos
   - Métricas o logros en ventas

3. Conocimiento del Mercado Tecnológico (30%):
   - Comprensión del ecosistema tecnológico
   - Familiaridad con tendencias de la industria
   - Adaptabilidad a cambios tecnológicos

Descripción de la Vacante:
{job_description}

CV del Candidato (Anonimizado para predecir sesgos):
{cv_text}

Debes retornar tu evaluación de forma estricta. Tu única respuesta DEBE SER EXACTAMENTE un objeto JSON válido con la siguiente estructura y formato:
{{
    "apto": "SI" o "NO",
    "puntuacion": un número entero del 0 al 100,
    "motivo": "Justificación detallada basada en los 3 criterios"
}}
"""
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.0,  # Deterministic mode
                    )
                )
                content = response.text
                return json.loads(content)
            except genai.types.generation_types.BlockedPromptException as blocked_error:
                print(f"[ERROR] Prompt blocked: {blocked_error}")
                return {
                    "apto": "NO",
                    "puntuacion": 0,
                    "motivo": "Evaluación bloqueada por contenido inapropiado"
                }
            except Exception as e:
                # Specific handling for quota exceeded
                if "429" in str(e) or "quota" in str(e).lower():
                    print(f"[CRITICAL ERROR] API Quota Exceeded: {e}")
                    return {
                        "apto": "NO",
                        "puntuacion": 0,
                        "motivo": "Error de cuota de API. Por favor, reintente más tarde o verifique la configuración de la API."
                    }
                print(f"[WARNING] Gemini analysis failed: {e}")
                return {
                    "apto": "NO",
                    "puntuacion": 0,
                    "motivo": "Error en el análisis del CV"
                }
        
        # Fallback evaluation using keyword matching
        job_keywords = self._extract_keywords(job_description)
        cv_keywords = self._extract_keywords(cv_text)
        
        # Calculate keyword match percentage
        matches = [kw for kw in job_keywords if kw in cv_keywords]
        match_percentage = min(int((len(matches) / max(len(job_keywords), 1)) * 100), 100)
        
        # Basic suitability determination
        is_suitable = match_percentage > 50
        
        return {
            "apto": "SI" if is_suitable else "NO",
            "puntuacion": match_percentage,
            "motivo": f"Evaluación básica basada en coincidencia de palabras clave. Porcentaje de coincidencia: {match_percentage}%. Palabras clave coincidentes: {', '.join(matches)}"
        }

if __name__ == "__main__":
    # Test directo para mostrar cómo funcionaría
    print("Módulo CVAnalyzer listo.")
    
    # Demostración de evaluación de respaldo
    analyzer = CVAnalyzer()
    job_desc = "Buscamos un Account Executive con experiencia en ventas B2B"
    cv_text = "Profesional con 4 años de experiencia en ventas de software"
    
    resultado = analyzer.analyze(cv_text, job_desc)
    print("Resultado de evaluación de respaldo:")
    print(json.dumps(resultado, indent=2))
