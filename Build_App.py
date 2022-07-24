import PyInstaller.__main__
import os
import shutil
from settings import appVersionNo
from platform import release, architecture

cwd = os.getcwd()
wd = f'{cwd}\\dist'
outputFileName = f'TIF_Files_Handler_v{appVersionNo}-Win_{release()}-{architecture()[0]}'

PyInstaller.__main__.run([
    'TIF_Files_Handler.py',
    f'-n{outputFileName}',
    '--onefile',
    '--windowed',
    '--add-data', 'src;src',
    '-i', ".\src\\tif.ico",
    '--splash', ".\src\\tif.png",
    '--exclude-module', 'matplotlib'
])

dirsToRemove = [f'{cwd}\\build', f'{cwd}\\__pycache__']
for d in dirsToRemove:
    if os.path.exists(d):
        shutil.rmtree(d)

os.remove(f'{cwd}\\{outputFileName}.spec')

os.startfile(wd)
