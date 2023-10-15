import PyInstaller.__main__


PyInstaller.__main__.run([
    'hero-siege-stats.py',
    '--onefile',
    '--windowed',
    '--icon',
    'assets/icons/logo.ico',
    '--add-data',
    'assets;assets/'
])
