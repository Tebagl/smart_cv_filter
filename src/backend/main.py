import os
import sys
from pathlib import Path

# Import necessary modules
from .database import DatabaseManager
from .extractor import CVExtractor
from .anonymizer import Anonymizer
from .keyword_matcher import KeywordMatcher

# Determine base directory dynamically
try:
    # For PyInstaller bundled applications
    BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
except Exception:
    BASE_DIR = Path(__file__).resolve().parent

# Define directory paths relative to the executable
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "output"
RECLUTADOS_DIR = OUTPUT_DIR / "RECLUTADOS"
DESCARTADOS_DIR = OUTPUT_DIR / "DISCARDED"

def main():
    # Initialize database
    db_manager = DatabaseManager()
    
    # Ensure database tables are created
    db_manager.create_tables()

    # Create necessary output directories
    for directory in [RECLUTADOS_DIR, DESCARTADOS_DIR]:
        os.makedirs(directory, exist_ok=True)

    # Rest of the existing main function remains the same
    try:
        # CV extraction and processing logic
        extractor = CVExtractor(INPUTS_DIR)
        cvs = extractor.extract_cvs()

        # Anonymization
        anonymizer = Anonymizer()
        anonymized_cvs = [anonymizer.anonymize(cv) for cv in cvs]

        # Keyword matching
        matcher = KeywordMatcher()
        
        for cv in anonymized_cvs:
            # Perform matching and scoring
            score, apto = matcher.match(cv)

            # Copy CV to appropriate output folder based on score
            if apto and score >= 70:
                # Logic for handling recruited CVs
                pass
            else:
                # Logic for handling discarded CVs
                pass

    except Exception as e:
        print(f"Error processing CVs: {e}")

if __name__ == "__main__":
    main()
