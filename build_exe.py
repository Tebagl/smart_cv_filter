import os
import sys
import shutil
import subprocess

def build_executable():
    """
    Construir ejecutable de Smart CV Filter usando PyInstaller
    """
    # Configuración de rutas
    project_root = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(project_root, 'src', 'frontend', 'main_gui.py')
    pyinstaller_path = os.path.join(os.path.expanduser('~'), '.local', 'bin', 'pyinstaller')
    site_packages = os.path.join(os.path.expanduser('~'), '.local', 'lib', 'python3.10', 'site-packages')
    
    # Limpiar directorios anteriores
    for dir_to_clean in ['build', 'dist']:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
    
    # Dependencias a incluir
    dependencies = [
        'python-dotenv', 'pathlib', 'sqlalchemy', 'alembic', 
        'pdfplumber', 'python-docx', 'spacy', 'google-generativeai', 
        'structlog', 'customtkinter', 'typing-extensions'
    ]
    
    # Comando de PyInstaller
    pyinstaller_cmd = [
        pyinstaller_path,
        '--onefile',           # Un solo archivo ejecutable
        '--noconsole',         # Sin consola de fondo
        '--name', 'SmartCVFilter',
        
        # Añadir recursos adicionales
        '--add-data', f'{project_root}/src:src',
        '--add-data', f'{project_root}/src/backend:backend',
        '--add-data', f'{project_root}/src/frontend:frontend',
        '--add-data', f'{project_root}/src/backend/inputs:inputs',
        '--add-data', f'{project_root}/src/backend/output:output',
    ]
    
    # Añadir --collect-all para cada dependencia
    for dep in dependencies:
        pyinstaller_cmd.extend(['--collect-all', dep])
    
    # Hidden imports y configuraciones adicionales
    pyinstaller_cmd.extend([
        # Hidden imports para dependencias
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'sqlalchemy.orm',
        '--hidden-import', 'sqlalchemy.pool',
        '--hidden-import', 'sqlalchemy.sql',
        '--hidden-import', 'sqlalchemy.engine',
        '--hidden-import', 'sqlalchemy.dialects',
        '--hidden-import', 'sqlalchemy.ext',
        '--hidden-import', 'sqlalchemy.types',
        '--hidden-import', 'customtkinter',
        '--hidden-import', 'spacy',
        '--hidden-import', 'google.generativeai',
        
        # Paths adicionales
        '--paths', site_packages,
        
        # Configuraciones adicionales
        '--clean',             # Limpiar caché de PyInstaller
        
        main_script
    ])
    
    print("Construyendo ejecutable de Smart CV Filter...")
    
    try:
        # Ejecutar comando de PyInstaller
        result = subprocess.run(
            pyinstaller_cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        print("Construcción completada exitosamente.")
        print("\nSalida de PyInstaller:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("Error durante la construcción:")
        print(f"Código de error: {e.returncode}")
        print("Salida de error:")
        print(e.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

def main():
    build_executable()

if __name__ == '__main__':
    main()