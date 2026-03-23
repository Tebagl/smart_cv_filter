import os
import sys
from pathlib import Path

# Add project root to Python path to ensure module imports work
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import dependencies
from dotenv import load_dotenv

# Import database initialization
from .database import init_database, db_manager
from .repositories import CandidateRepository

# Robust import strategy with explicit error handling
def import_module(module_path, class_name):
    """
    Attempt to import a specific class from a module with detailed error handling.
    
    :param module_path: Full import path for the module
    :param class_name: Name of the class to import
    :return: Imported class
    :raises ImportError: If module or class cannot be imported
    """
    try:
        # Dynamically import the module
        module = __import__(module_path, fromlist=[class_name])
        
        # Return the specific class
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        print(f"[CRITICAL] Failed to import {module_path}.{class_name}: {e}")
        print("Ensure all required modules are installed and the project structure is correct.")
        sys.exit(1)

# Import specific classes using the robust import method
UniversalExtractor = import_module('src.backend.extractor', 'UniversalExtractor')
LocalAnonymizer = import_module('src.backend.anonymizer', 'LocalAnonymizer')
CVAnalyzer = import_module('src.backend.analyzer', 'CVAnalyzer')

# Load environment variables
load_dotenv()

# Use Path.resolve() to get the absolute path of the current script's directory
# This ensures correct path resolution regardless of the current working directory
# - BASE_DIR: The directory containing the current script
# - INPUTS_DIR: Subdirectory for input files
# - OUTPUT_DIR: Subdirectory for output files
# - RECLUTADOS_DIR and DESCARTADOS_DIR: Specific output subdirectories
BASE_DIR = Path(__file__).resolve().parent
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "output"
RECLUTADOS_DIR = OUTPUT_DIR / "RECLUTADOS"
DESCARTADOS_DIR = OUTPUT_DIR / "DESCARTADOS"

def main():
    print("==============================================")
    print("Initiating Smart CV Filter - Orchestrator V1.0")
    print("==============================================\n")
    
    # Initialize database
    print("[INFO] Initializing Database...")
    init_database(drop_existing=True)  # Recreate tables for clean slate
    
    # Create necessary directories if they don't exist
    # Using Path.mkdir() with parents=True ensures nested directories are created
    # exist_ok=True prevents errors if directories already exist
    for directory in [INPUTS_DIR, RECLUTADOS_DIR, DESCARTADOS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Initialize Processing Modules
    print("[INFO] Initializing Auxiliary Modules...")
    try:
        extractor = UniversalExtractor()
        anonymizer = LocalAnonymizer()
        analyzer = CVAnalyzer()
        print("[OK] Modules initialized successfully.\n")
    except Exception as e:
        print(f"[ERROR] Initialization failed: {e}")
        return

    # Prepare database session for candidate storage
    session = db_manager.get_session()
    candidate_repo = CandidateRepository(session)

    # Process CV files
    print(f"[INFO] Exploring CV directory: {INPUTS_DIR}")
    try:
        # Use Path.iterdir() to list files, filtering only files (not directories)
        archivos_validos = [f for f in INPUTS_DIR.iterdir() if f.is_file()]
        
        if not archivos_validos:
            print("[INFO] No files found for processing in 'inputs/'.")
        else:
            print(f"[INFO] Found {len(archivos_validos)} files. Processing...")
            
            # Load job description
            # Use Path methods for file reading with explicit encoding
            job_desc_path = BASE_DIR / "job_description.txt"
            if job_desc_path.exists():
                job_description = job_desc_path.read_text(encoding="utf-8")
            else:
                job_description = "We are looking for an Account Executive or B2B Sales Representative with at least 3 years of experience."
                print("[WARNING] job_description.txt not found, using static fallback.")
            print("[INFO] Job Description loaded from file.\n")

            for archivo in archivos_validos:
                print(f"--- Evaluating: {archivo.name} ---")
                
                try:
                    # Pass 1: Text Extraction
                    # Convert Path object to string for compatibility with existing methods
                    cv_text = extractor.extract_text(str(archivo))
                    
                    # Pass 2: Anonymization (PII Protection)
                    cv_anon = anonymizer.anonymize(cv_text)
                    
                    # Pass 3: Semantic Evaluation with Gemini LLM
                    # Only send if text was successfully extracted
                    if cv_anon.strip():
                        resultado = analyzer.analyze(cv_anon, job_description)
                        score = resultado.get('puntuacion', 0)
                        apto = resultado.get('apto', False)
                        
                        print(f"   * Score: {score}/100")
                        print(f"   * Suitable: {apto}")
                        print(f"   * Reason: {resultado.get('motivo')}")
                        
                        # Create candidate record
                        candidate = candidate_repo.create_candidate(
                            first_name=archivo.stem.split('_')[1],  # Assumes filename format like cv_name_role.txt
                            last_name=archivo.stem.split('_')[2] if len(archivo.stem.split('_')) > 2 else '',
                            email=f"{archivo.stem}@example.com"  # Placeholder email
                        )
                        
                        # Add resume to candidate
                        candidate_repo.add_resume(
                            candidate_id=candidate.id,
                            file_path=str(archivo),
                            file_type='text/plain'
                        )
                        
                        # Copy CV to appropriate output folder based on score
                        if apto and score >= 70:
                            # High-scoring CVs go to RECLUTADOS
                            dest_path = RECLUTADOS_DIR / archivo.name
                            dest_path.write_text(archivo.read_text())
                            print(f"   * CV copied to RECLUTADOS: {dest_path}")
                        else:
                            # Low-scoring or unsuitable CVs go to DESCARTADOS
                            dest_path = DESCARTADOS_DIR / archivo.name
                            dest_path.write_text(archivo.read_text())
                            print(f"   * CV copied to DESCARTADOS: {dest_path}")
                    else:
                        print(f"   [WARNING] Could not extract valid text from file {archivo.name}.")
                except Exception as e:
                    print(f"   [ERROR] Processing {archivo.name}: {e}")
                print()
                
    except FileNotFoundError:
        print(f"[ERROR] The directory {INPUTS_DIR} does not exist.")
    finally:
        # Ensure session is closed
        session.close()

if __name__ == "__main__":
    main()
