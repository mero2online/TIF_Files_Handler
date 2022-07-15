import PyInstaller.__main__

PyInstaller.__main__.run([
    'TIF_Files_Handler.py',
    '--onefile',
    '--windowed',
    '--add-data', 'src;src',
    '-i', ".\src\\tif.ico",
    '--splash', ".\src\\tif.png",
])
