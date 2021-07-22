# -*- mode: python ; coding: utf-8 -*-
import arabic_reshaper

block_cipher = None

added_files = [
    ('stimuli/', 'stimuli'),
    ('ZL_colors.mat', '.'),
    (arabic_reshaper.__path__[0], 'arabic_reshaper'),
    ('freetype.dll', '.'),
    ('matplotlibrc', 'mpl-data')
    ]
a = Analysis(['visual_memory_precision.py'],
             binaries=[],
             datas=added_files,
             hiddenimports=['psychopy.visual.line'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='visual_memory_precision',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='visual_memory_precision')