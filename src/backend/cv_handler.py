import os
from typing import List, Optional
from datetime import datetime
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.backend.logging_config import log_function_call

# Imports internos
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

    @log_function_call
    def process_cv(self, raw_text: str, user_job_desc: str = None, file_path: str = ""):
        try:
            # 1. Analizar con IA
            jd = user_job_desc if user_job_desc else "Perfil técnico general"
            decision = self.analyzer.analyze(raw_text, jd)
            
            # 2. Extraer y LIMPIAR los datos reales
            raw_score = decision.get('score', 0)
            try:
                # Limpiamos el score por si viene con % o espacios
                f_score = int(str(raw_score).replace('%', '').strip())
            except:
                f_score = 0

            f_status = decision.get('apto', 'NO')
            f_motivo = decision.get('motivo', 'Sin detalles')

            # 3. Asegurar ruta absoluta para el enlace
            ruta_para_db = os.path.abspath(file_path)

            # 4. Guardar en la base de datos (USANDO LAS VARIABLES)
            nuevo_registro = Candidate(
                firstName="Candidato",
                lastName="Ref_" + datetime.now().strftime('%H%M%S'),
                email=f"anon_{os.urandom(3).hex()}@local.com",
                score=f_score,       # ✅ Aquí se usa f_score
                address=ruta_para_db # ✅ Aquí se usa la ruta
            )
            
            self._session.add(nuevo_registro)
            self._session.commit()

            return {
                "status": "success",
                "decision": f_status,
                "reason": f_motivo,
                "score": f_score
            }
        except Exception as e:
            self._session.rollback()
            logger.error(f"❌ Error guardando candidato: {e}")
            return {"status": "error", "reason": str(e)}
    def get_top_candidates(self, limit=15):
        """Consulta los mejores candidatos ordenados por score"""
        try:
            return self._session.query(Candidate)\
                .order_by(Candidate.score.desc())\
                .limit(limit)\
                .all()
        except Exception as e:
            logger.error(f"Error SQL: {e}")
            return []