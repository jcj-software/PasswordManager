@echo off
python -m pip install pyinstaller
pyinstaller -w --icon assets/icon.ico app.py
pause