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
            # 1. Leer Job Description
            jd_path = "src/backend/job_description.txt" 
            try:
                with open(jd_path, 'r', encoding='utf-8') as f:
                    job_desc = f.read()
            except FileNotFoundError:
                job_desc = "Perfil técnico general"
                logger.warning("No se encontró job_description.txt")

            # 2. Procesamiento
            clean_text = self.anonymizer.anonymize(raw_text)
            
            # 3. 🧠 LLAMADA AL ANALIZADOR
            decision = self.analyzer.analyze(raw_text, job_desc) 
            
            # 4. TRADUCCIÓN DE LLAVES PARA LA GUI
            final_status = decision.get('apto') or "ANALIZADO"
            final_reason = decision.get('motivo') or "Sin detalles disponibles."

            # --- SECCIÓN DE GUARDADO SINCRONIZADA CON MODELS.PY ---
            # Generamos un email único para evitar errores de duplicidad (unique=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_email = f"candidato_{timestamp}@local.com"

            nuevo_registro = Candidate(
                firstName="Candidato", 
                lastName=f"Procesado_{timestamp}",
                email=unique_email,
                phone="000000000",
                address="Procesado localmente"
            )
            
            self._session.add(nuevo_registro)
            self._session.commit()

            return {
                "status": "success",
                "decision": final_status,
                "reason": final_reason,
                "text": clean_text
            }
       
        except Exception as e:
            self._session.rollback() # Evita que la DB se bloquee si hay error
            logger.error(f"Error en el motor de IA: {e}")
            return {"status": "error", "reason": str(e)}