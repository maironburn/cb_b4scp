# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['generacion_boletos_pdf.py'],
             pathex=['C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos'],
             binaries=[( 'C:\\Users\\mario.diaz.rodriguez\\PycharmProjects\\CitiBank_Boletos\\3rd_parties', '.\\3rd_parties' )],
             datas=[ ( 'src', 'src' ),
			         ( 'logger', 'logger' ),
			         ( '.\\common_config.py', '.\\common_config.py' ),
			         ( 'Boletos descargados', 'Boletos descargados' ),
			        ( 'json_bank', 'json_bank' ),
			        ( 'xls_folder', 'xls_folder' ),
			        ( 'documentacion_usuario', 'documentacion_usuario' )
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
          name='generacion_boletos_pdf',
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
               name='generacion_boletos_pdf')
