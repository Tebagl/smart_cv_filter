# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Recolectamos TODAS las librerías conflictivas de golpe
datas, binaries, hiddenimports = collect_all('customtkinter')
d, b, h = collect_all('spacy')
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('en_core_web_sm') # El modelo de lenguaje
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('sqlalchemy')
datas += d; binaries += b; hiddenimports += h
d, b, h = collect_all('google.generativeai')
datas += d; binaries += b; hiddenimports += h

a = Analysis(
    ['src/frontend/main_gui.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas + [('src', 'src'), ('.env', '.')], # Metemos el código y el .env
    hiddenimports=hiddenimports + ['spacy', 'pdfplumber', 'sqlalchemy', 'google.generativeai'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    console=False, # Sin terminal negra
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)