@echo off
pip install websockets pygame numpy pyinstaller
pyinstaller --onefile --windowed --icon=app.ico --name FerroChatClient ferro_client.py
pause
