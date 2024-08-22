# -*- mode: python ; coding: utf-8 -*-
import webssh
import os

# 获取 webssh 的安装路径
webssh_path = os.path.dirname(webssh.__file__)

a = Analysis(
    ['WebSSH.Py'],
    pathex=[],
    binaries=[],
    datas=[(os.path.join(webssh_path, 'static'), 'webssh/static'),(os.path.join(webssh_path, 'templates'), 'webssh/templates')],
    hiddenimports=[],
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
    name='wssh',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
