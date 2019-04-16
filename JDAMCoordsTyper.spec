# -*- mode: python -*-

block_cipher = None


a = Analysis(['JDAMCoordsTyper.py'],
             pathex=['C:\\Windows\\System32\\downlevel', 'C:\\Users\\k9mic\\OneDrive\\Documents\\Git\\F18CoordinateTyper'],
             binaries=[],
             datas=[('HoneyBadgers48.ico', '.'),('HoneyBadgers256.ico', '.')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='JDAMCoordsTyper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='HoneyBadgers256.ico')
