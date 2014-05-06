# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['C:\\Users\\Vincent\\Downloads\\Programming\\stunJam'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
			 
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
		
pyz = PYZ(a.pure)
exe = EXE(pyz,
          Tree('data', prefix='data', excludes=["goal", "*.blend", "*.svg", "son"]),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PortTales.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon="data/icon_exe.ico")
