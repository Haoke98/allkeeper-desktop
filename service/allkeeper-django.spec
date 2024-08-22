# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import get_package_paths
site_packages_path = get_package_paths('django')[0]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 添加 simplepro 的模板路径
        (os.path.join(site_packages_path, 'simplepro/templates'), 'simplepro/templates'),
        # 添加 simplepro 的静态资源路径
        (os.path.join(site_packages_path, 'simplepro/static'), 'simplepro/static'),
        # 添加 simpleui 的静态资源路径
        (os.path.join(site_packages_path, 'simpleui/static'), 'simpleui/static'),
        # 添加 simpleui 的模版路径
        (os.path.join(site_packages_path, 'simpleui/templates'), 'simpleui/templates')
    ],
    hiddenimports=[
        'log_request_id','log_request_id.filters','log_request_id.middleware',
        'middlewares',
        'proj.log','proj.database_router',
        'jumpService.admin',
        'simplepro.templatetags'
        ],
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
    name='allkeeper-django',
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
