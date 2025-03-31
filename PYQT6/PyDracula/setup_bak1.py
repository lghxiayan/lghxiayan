import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico', 'themes/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

packages_list = ['PySide6', 'ansiconv', 'pynput', 'chardet', 'pygments',
                 'selenium', 'sqlalchemy', 'alembic',
                 'configupdater', 'time', 'logging', 'subprocess', 'threading', 'ctypes',
                 'random', 'win32api', 'win32con', 'win32gui', 'configparser', 're',
                 'datetime', 'platform', 'ast', 'alembic']

try:
    # SETUP CX FREEZE
    setup(
        name="xiayan tools",
        version="1.0",
        description="Modern GUI for Python applications",
        author="Wanderson M. Pimenta",
        options={'build_exe': {'include_files': files, 'packages': packages_list}},
        executables=[target]
    )
except Exception as e:
    print(f'Exception: {e}')
