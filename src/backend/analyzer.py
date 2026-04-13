import requests
import json
import os

class CVAnalyzer:
    def __init__(self):
        self.url = "http://127.0.0.1:11434/api/generate"
        self.model = "gemma2:2b"
        self.headers = {"Content-Type": "application/json"}

    def analyze(self, cv_text, job_description):
        # Prompt equilibrado: Estricto con intrusos, justo con el sector
        prompt = f"""
        Actúa como un experto en selección de personal. Analiza el CV para el puesto de: {job_description}.

        MÉTODO DE EVALUACIÓN:
        1. Identifica habilidades y experiencia CLAVE para el puesto.
        2. Si el CV tiene experiencia REAL y DIRECTA en el sector, valora positivamente (Score > 70).
        3. Si el CV es de un sector totalmente ajeno (ej. programación para camarera), el score DEBE ser inferior a 15.
        4. No te inventes incompatibilidades. Si menciona el sector solicitado, puntúa según esa experiencia.

        Responde exclusivamente en formato JSON:
        {{
          "score": número del 0 al 100,
          "apto": "SI" o "NO",
          "motivo": "Explicación breve y coherente"
        }}

        TEXTO DEL CV A ANALIZAR:
        {cv_text}
        """

        try:
            response = requests.post(
                self.url, 
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }, 
                headers=self.headers,
                timeout=None
            )
            
            # Obtener respuesta de Ollama
            full_response = response.json()
            if 'response' in full_response:
                return json.loads(full_response['response'])
            else:
                return {"score": 0, "apto": "NO", "motivo": "Ollama devolvió una respuesta vacía"}

        except Exception as e:
            print(f"DEBUG - Error completo: {str(e)}") 
            # IMPORTANTE: Devolvemos 'score' (no puntuacion) para que cv_handler lo entienda
            return {
                "score": 0,
                "apto": "NO",
                "motivo": f"Error en análisis: {str(e)}"
            }