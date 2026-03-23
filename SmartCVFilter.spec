# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/home/usuario/proyectos/smart_cv_filter/src/frontend/main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/usuario/proyectos/smart_cv_filter/src/backend', 'backend'), ('/home/usuario/proyectos/smart_cv_filter/src/frontend', 'frontend'), ('/home/usuario/proyectos/smart_cv_filter/src/backend/inputs', 'inputs'), ('/home/usuario/proyectos/smart_cv_filter/src/backend/output', 'output')],
    hiddenimports=['customtkinter', 'sqlalchemy', 'spacy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
