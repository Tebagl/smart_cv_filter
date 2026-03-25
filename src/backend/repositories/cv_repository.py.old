from src.backend.anonymizer import Anonymizer
from src.backend.vector_store import VectorStore
from src.backend.database import DatabaseManager
from src.backend.embeddings_engine import LocalEmbeddings

class CVRepository:
    def __init__(self):
        self.anonymizer = Anonymizer()
        self.embeddings_engine = LocalEmbeddings()
        self.vector_store = VectorStore(dimension=384)
        self.database = DatabaseManager()

    def process_cv(self, cv_text):
        anon_text = self.anonymizer.anonymize(cv_text)
        vector = self.embeddings_engine.get_embedding(anon_text)
        metadata = {"original_text": cv_text, "anonymized_text": anon_text}
        unique_id = "cv_001"  # Esto debería ser generado dinámicamente
        self.vector_store.add_cv(id=unique_id, embedding=vector, metadata=metadata)
        self.database.save_cv(anon_text)
        return anon_text