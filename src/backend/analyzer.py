import requests
import json
import os

class CVAnalyzer:
    def __init__(self):
        # Usamos la IP numérica que confirmó el comando 'ss'
        self.url = "http://127.0.0.1:11434/api/generate"
        self.model = "gemma2:2b"
        # Añadimos cabeceras para asegurar la comunicación
        self.headers = {"Content-Type": "application/json"}


    def analyze(self, cv_text, job_description):
        # Creamos el "Cerebro" del análisis
        prompt = f"""
        Eres un experto en Selección de Personal. Analiza la afinidad entre el CV y la OFERTA.
        
        OFERTA: {job_description}
        CV: {cv_text}
        
        INSTRUCCIONES:
        - Si los sectores no coinciden (ej. IT vs Hostelería), el score debe ser muy bajo (<20).
        - Identifica habilidades reales (PDA, SQL, C, Barra) sin importar su longitud.
        
        RESPONDE SOLO EN JSON:
        {{
            "apto": "SI" o "NO",
            "puntuacion": int,
            "motivo": "Explicación breve de por qué encaja o no",
            "coincidencias": ["habilidad1", "habilidad2"]
        }}
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
                headers=self.headers, # <--- Añade esto
                timeout=None #60            # Subimos a 60 por si tu PC va lento
        )
            # La IA nos devuelve directamente el JSON procesado
            data = json.loads(response.json()['response'])
            return data

        except Exception as e:
            # Esto nos imprimirá el error real en la terminal donde lanzas el programa
            print(f"DEBUG - Error completo: {str(e)}") 
            return {
                "apto": "NO",
                "puntuacion": 0,
                "motivo": f"Error de conexión: {type(e).__name__}",
                "coincidencias": []
            }
        '''
        except Exception as e:
            return {
                "apto": "NO",
                "puntuacion": 0,
                "motivo": f"Gemma 2:2b no responde. ¿Está Ollama activo? Error: {e}",
                "coincidencias": []
            }
        '''