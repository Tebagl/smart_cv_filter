# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all

# Añadir directorio del proyecto al path
project_root = os.path.abspath('.')
sys.path.insert(0, project_root)

# Recolectamos TODAS las librerías conflictivas de golpe
datas, binaries, hiddenimports = collect_all('customtkinter')
d, b, h = collect_all('spacy')
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('en_core_web_sm') # El modelo de lenguaje en inglés
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('es_core_news_md') # Modelo de lenguaje en español
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('sqlalchemy')
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('google.generativeai')
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('typing_extensions')
datas += d; binaries += b; hiddenimports += h

# Incluir archivos de recursos y configuración
extra_datas = [
    ('src', 'src'),
    ('src/backend/inputs', 'src/backend/inputs'),
    ('src/backend/job_description.txt', 'src/backend'),
    ('.env', '.'),
]
datas.extend(extra_datas)

a = Analysis(
    ['src/frontend/main_gui.py'],
    pathex=['.', 'src'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + [
        'spacy', 
        'pdfplumber', 
        'sqlalchemy', 
        'google.generativeai', 
        'es_core_news_md',
        'tkinter',
        'customtkinter',
        'typing_extensions',
        'src.backend.extractor',
        'src.backend.anonymizer',
        'src.backend.analyzer',
        'src.backend.database',
        'src.backend.repositories'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'test', 
        'tests', 
        'pytest', 
        'mypy'
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SmartCVFilter_PRO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin terminal negra
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)