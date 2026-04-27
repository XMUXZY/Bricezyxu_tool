# -*- mode: python ; coding: utf-8 -*-

import customtkinter
import os

# 获取 customtkinter 包的路径，打包时需要包含其主题/资源文件
ctk_path = os.path.dirname(customtkinter.__file__)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('pages', 'pages'),
        ('calculators', 'calculators'),
        ('utils', 'utils'),
        ('game_data', 'game_data'),
        (ctk_path, 'customtkinter'),
    ],
    hiddenimports=[
        'customtkinter',
        'openpyxl',
        'calculators',
        'calculators.calc_b',
        'calculators.calc_c',
        'calculators.calc_d',
        'calculators.calc_dunjia',
        'calculators.calc_e',
        'calculators.calc_fabao',
        'calculators.calc_feng_shui',
        'calculators.calc_gem_grind',
        'calculators.calc_guardian',
        'calculators.calc_star_map',
        'calculators.calc_zhance',
        'calculators.calc_zhu_ling',
        'calculators.calc_baihu_star',
    ],
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
    name='游戏运营工具合集',
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
