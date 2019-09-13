# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\Bank_RPA'],
             binaries=[ ( 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\Bank_RPA\\chromedriver_win32\\chromedriver.exe', '.\\3rd_parties\\chromedriver_win32' ),
					('C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\Bank_RPA\\python3.6.6', '.\\3rd_parties\\python3.6.6'),
					('C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\Bank_RPA\\IEDriver', '.\\3rd_parties\\IEDriver')
			 ],
             datas=[ ( 'src', 'src' ),
			 ( 'logger', 'logger' ),
			 ( 'settings', 'settings' )
			 ],
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
          name='main',
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
               name='main')
