import re
import spacy
import subprocess
import sys

class Anonymizer:
    """
    Módulo 2: LocalAnonymizer
    Se encarga de detectar y reemplazar Datos de Identificación Personal (PII)
    en el texto extraído (Nombres, Correos, Teléfonos) utilizando Expresiones
    Regulares y la librería de NLP spaCy, para garantizar la privacidad y
    conformidad con el GDPR.
    """
    
    def __init__(self, model="es_core_news_md"):
        """
        Inicializa el modelo de spaCy. Si el modelo no está descargado, 
        lo descarga automáticamente.
        """
        self.model = model
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"El modelo de spaCy '{model}' no se encontró. Intentando descargar...")
            subprocess.run([sys.executable, "-m", "spacy", "download", model], check=True)
            self.nlp = spacy.load(model)

    def anonymize(self, text: str) -> str:
        """
        Reemplaza posibles emails, teléfonos y nombres de personas por identificadores.
        """
        if not text:
            return text

        # 1. Ocultar Emails usando regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        anon_text = re.sub(email_pattern, '[EMAIL]', text)

        # 2. Ocultar Teléfonos usando regex
        # Detecta formatos comunes de números (opcional código de país, espacios, guiones)
        phone_pattern = r'\b(?:\+?\d{1,3}[ -]?)?\(?\d{2,4}\)?[ -]?\d{3,4}[ -]?\d{3,4}\b'
        # Aplicamos una función callback para asegurarnos de que la coincidencia tenga suficientes dígitos
        def replace_phone(match):
            digits = re.sub(r'\D', '', match.group(0))
            if len(digits) >= 8:
                return '[TELEFONO]'
            return match.group(0)

        anon_text = re.sub(phone_pattern, replace_phone, anon_text)

        # 3. Ocultar Nombres de personas usando spaCy
        doc = self.nlp(anon_text)
        
        # Guardamos las entidades de tipo persona (PER para español, PERSON para inglés)
        ents = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents if ent.label_ in ("PER", "PERSON")]
        
        # Reemplazamos en orden inverso (de atrás hacia adelante) para evitar desajuste de índices
        for start, end, label in sorted(ents, reverse=True):
            # Solo reemplazamos la palabra, asegurando no alterar formato.
            anon_text = anon_text[:start] + "[NOMBRE]" + anon_text[end:]

        return anon_text

if __name__ == "__main__":
    # Prueba rápida aislada si se ejecuta directamente el archivo
    anonymizer = Anonymizer()
    sample_text = "El candidato Juan Perez, con email jperez@mail.com y teléfono +34 600 123 456, solicita el puesto."
    print("Original:", sample_text)
    print("Anonimizado:", anonymizer.anonymize(sample_text))
