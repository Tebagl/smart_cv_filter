# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# 1. Definimos qué carpetas extras necesita el programa
# Incluimos el código de src para que el ejecutable encuentre el backend
datas = [
    ('src', 'src'), 
]

binaries = []
hiddenimports = [
    'docx', 
    'odf', 
    'fitz', 
    'requests'
]

# 2. Recolectamos automáticamente lo necesario para CustomTkinter (la interfaz)
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

a = Analysis(
    ['src/frontend/main_gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch', 
        'spacy', 
        'sentence_transformers', 
        'numpy', 
        'matplotlib'
    ], # Excluimos lo pesado que no usamos
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartCVFilter', # Nombre del ejecutable final
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Pon True si quieres ver una terminal de debug al abrirlo
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SmartCVFilter',
)