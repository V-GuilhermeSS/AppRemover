from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app_icon.icns',  # Caminho para o ícone (deve estar em formato .icns)
    'includes': ['PyQt5'],
}

setup(
    app=APP,
    name='AppRemover',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
