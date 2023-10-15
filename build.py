import PyInstaller.__main__


PyInstaller.__main__.run([
    'hero-siege-stats.py',
    '--onefile',
    '--windowed',
    '--add-data',
    'assets;assets/'
])
