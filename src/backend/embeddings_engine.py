import os
import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class LocalEmbeddings:
    """
    Módulo de Almacenamiento Vectorial:
    Convierte texto en embeddings (vectores) para permitir 
    búsquedas semánticas en la base de datos.
    """
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
        logger.info(f"Cargando modelo de embeddings: {model_name}")
        # Este modelo es multilingüe y muy ligero, ideal para CVs en español
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, text):
        """Genera un vector numérico a partir de un texto"""
        if not text:
            return None
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()  # Lo convertimos a lista para guardarlo en la DB
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return None