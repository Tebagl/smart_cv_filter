from typing import List, Optional
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# Imports internos
from src.backend.models import Candidate, Resume
from src.backend.anonymizer import Anonymizer
from src.backend.embeddings_engine import LocalEmbeddings
from src.backend.analyzer import CVAnalyzer

logger = logging.getLogger(__name__)

class CandidateRepository:
    def __init__(self, session: Session):
        self._session = session
        self.anonymizer = Anonymizer()
        self.embeddings_engine = LocalEmbeddings()
        self.analyzer = CVAnalyzer() # <--- Lo inicializamos aquí una sola vez

    def get_candidate_by_email(self, email: str) -> Optional[Candidate]:
        return self._session.query(Candidate).filter_by(email=email).first()

    # --- MÉTODO DE PROCESAMIENTO CON IA ---

    def process_cv(self, raw_text: str):
        try:
            # 1. Intentar leer la descripción del puesto (Job Description)
            # Ajusta la ruta si tu archivo está en otro sitio
            jd_path = "src/backend/job_description.txt" 
            try:
                with open(jd_path, 'r', encoding='utf-8') as f:
                    job_desc = f.read()
            except FileNotFoundError:
                job_desc = "Perfil técnico general" # Fallback si no hay archivo
                logger.warning("No se encontró job_description.txt, usando perfil general.")

            # 2. Procesamiento que ya funcionaba
            clean_text = self.anonymizer.anonymize(raw_text)
            vector = self.embeddings_engine.get_embeddings(clean_text)
            
           # 3. 🧠 LLAMADA AL ANALIZADOR
            decision = self.analyzer.analyze(raw_text, job_desc) 
            
            # 4. TRADUCCIÓN DE LLAVES (Aquí estaba el fallo)
            # El analyzer usa "apto" y "motivo", la GUI espera "decision" y "reason"
            final_status = decision.get('apto') or "ANALIZADO"
            final_reason = decision.get('motivo') or "Sin detalles disponibles."

            return {
                "status": "success",
                "decision": final_status,
                "reason": final_reason,
                "text": clean_text
            }
       
        except Exception as e:
            self._session.rollback()
            logger.error(f"Error en el motor de IA: {e}")
            return {"status": "error", "reason": str(e)}