import os
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

        :param db_url: Database connection URL. Defaults to SQLite in project root.
        :param echo: Enable SQLAlchemy query logging
        :param pool_recycle: Connection pool recycle time in seconds
        """
        # Prevent re-initialization if already configured
        if self._engine is not None:
            return

        # Determine database URL
        if db_url is None:
            # Create data directory if it doesn't exist
            import os
            
            # Ensure data directory exists
            data_dir = Path(__file__).resolve().parent.parent / 'data'
            os.makedirs(data_dir, exist_ok=True)
            
            # Set database path
            db_path = data_dir / 'smart_cv.db'
            db_url = f'sqlite:///{db_path}'
            
            # Ensure the database file is created
            if not db_path.exists():
                db_path.touch()
                print(f"[INFO] Created new database file: {db_path}")

        # Create engine with specific configuration
        self._engine = create_engine(
            db_url, 
            echo=echo,
            poolclass=NullPool,  # Disable connection pooling for simplicity
            pool_recycle=pool_recycle
        )

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

    def execute_transaction(self, transaction_func):
        """
        Execute a database transaction with automatic commit/rollback.

        :param transaction_func: Function containing database operations
        :return: Result of the transaction function
        """
        session = self.get_session()
        try:
            result = transaction_func(session)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise
        finally:
            self.close_session(session)

# Global database manager instance
db_manager = DatabaseManager()

def init_database(drop_existing: bool = False):
    """
    Initialize the database with optional table recreation.

    :param drop_existing: Drop and recreate all tables
    """
    db_manager.create_tables(drop_existing)