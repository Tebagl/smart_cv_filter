# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Contenedores para dependencias
datas = [('src', 'src')]  # Incluye todo tu código fuente y la carpeta data
binaries = []

# --- RECOLECCIÓN DE LIBRERÍAS CRÍTICAS ---

# NLP y Anonimización
tmp_ret = collect_all('spacy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# También es recomendable forzar la importación del modelo que usas
hiddenimports += ['es_core_news_md']

# Interfaz Gráfica
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Lectura de PDF
tmp_ret = collect_all('pdfplumber')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Base de Datos
tmp_ret = collect_all('sqlalchemy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# MOTOR DE IA LOCAL (Crucial para que funcione el análisis)
tmp_ret = collect_all('sentence_transformers')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('torch')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

hiddenimports += ['es_core_news_md']


a = Analysis(
    ['src/frontend/main_gui.py'],  # Tu archivo principal
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['google.generativeai', 'notebook', 'setuptools'], # Excluimos lo innecesario
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SmartCVFilter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, # Comprime el ejecutable final
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # False para que NO aparezca la terminal negra
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)