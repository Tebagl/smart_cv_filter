import os
import sys
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from .models import Base

class DatabaseManager:
    """
    Manages database connection and session handling for the Smart CV Filter application.
    Supports multiple database backends with configurable connection strategies.
    """
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        """
        Singleton pattern implementation to ensure a single database connection.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, 
        db_url: Optional[str] = None, 
        echo: bool = False, 
        pool_recycle: int = 3600
    ):
        """
        Initialize database connection and session factory.

        :param db_url: Database connection URL. Defaults to SQLite in executable directory.
        :param echo: Enable SQLAlchemy query logging
        :param pool_recycle: Connection pool recycle time in seconds
        """
        # Prevent re-initialization if already configured
        if self._engine is not None:
            return
        
        # Determine database URL
        if db_url is None:
            # Usamos resolve() para obtener la ruta real completa
            current_file = Path(__file__).resolve()
            
            # Subimos hasta la carpeta 'src' de forma segura
            # Si el archivo está en /home/usuario/proyectos/smart_cv_filter/src/backend/database.py
            # backend_dir = /home/usuario/proyectos/smart_cv_filter/src/backend
            # src_dir = /home/usuario/proyectos/smart_cv_filter/src
            src_dir = current_file.parent.parent
            
            data_dir = src_dir / 'data'
            
            # ¡CRÍTICO! Forzamos la creación y verificamos la ruta
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = data_dir / 'smart_cv.db'
            
            
            db_url = f'sqlite:///{db_path}'
            
            # Mensaje de confirmación en consola
            if not db_path.exists():
                db_path.touch()
                print(f"[INFO] Nueva base de datos creada en: {db_path}")
            else:
                print(f"[INFO] Usando base de datos existente en: {db_path}")

        # Create engine with specific configuration
        self._engine = create_engine(
            db_url, 
            echo=echo,
            poolclass=NullPool,  # Disable connection pooling for simplicity
            pool_recycle=pool_recycle
        )

        # Create all tables defined in models
        Base.metadata.create_all(self._engine)

        # Create session factory
        self._session_factory = sessionmaker(bind=self._engine)

    def create_tables(self, drop_existing: bool = False):
        """
        Create all database tables defined in models.

        :param drop_existing: Drop existing tables before creation
        """
        if drop_existing:
            Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def get_session(self) -> Session:
        """
        Obtain a new database session.

        :return: SQLAlchemy Session object
        """
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call __init__ first.")
        return self._session_factory()

    def close_session(self, session: Session):
        """
        Close and clean up a database session.

        :param session: SQLAlchemy Session to close
        """
        if session:
            session.close()