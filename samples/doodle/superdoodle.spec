# -*- mode: python -*-
#
# This is a spec file for PyInstaller. To make a binary distribution of the
# superdoodle application run a command like this:
#
#       pyinstaller superdoodle.spec
#
# And then look in the ./dist folder for the results
#

block_cipher = None


a = Analysis(['superdoodle.py'],
             pathex=['.'],
             binaries=[],
             datas=[('mondrian.ico', '.')],
             hiddenimports=[],
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
          name='superdoodle',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='superdoodle')
app = BUNDLE(coll,
             name='superdoodle.app',
             icon='mondrian.icns',
             bundle_identifier=None)
