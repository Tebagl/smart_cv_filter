# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Solo incluimos el código fuente (src)
datas = [('src', 'src')]
binaries = []
hiddenimports = [
    'docx', 
    'odf', 
    'fitz', 
    'requests',
    'PIL._tkinter_finder'
]

# Recolectamos CustomTkinter (interfaz)
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
    # EXCLUIMOS todo lo pesado que NO usamos
    excludes=['torch', 'sentence_transformers', 'spacy', 'numpy', 'IPython', 'PIL.ImageQt'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartCVFilter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Pon True solo si necesitas ver errores en una terminal negra al abrirlo
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