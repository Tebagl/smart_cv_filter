import os
import sys
import subprocess

def build_executable():
    """
    Construir ejecutable de Smart CV Filter usando PyInstaller
    """
    # Configuración de rutas
    project_root = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(project_root, 'src', 'frontend', 'main_gui.py')
    pyinstaller_path = os.path.expanduser('~/.local/bin/pyinstaller')
    
    # Comando de PyInstaller
    pyinstaller_cmd = [
        pyinstaller_path,
        '--onefile',           # Un solo archivo ejecutable
        '--noconsole',         # Sin consola de fondo
        '--name', 'SmartCVFilter',
        
        # Añadir recursos adicionales
        '--add-data', f'{project_root}/src/backend:backend',
        '--add-data', f'{project_root}/src/frontend:frontend',
        '--add-data', f'{project_root}/src/backend/inputs:inputs',
        '--add-data', f'{project_root}/src/backend/output:output',
        
        # Hidden imports para dependencias
        '--hidden-import', 'customtkinter',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'spacy',
        
        # Configuraciones adicionales
        '--clean',             # Limpiar caché de PyInstaller
        
        main_script
    ]
    
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