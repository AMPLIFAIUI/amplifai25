@echo off
pip install websockets pyinstaller
pyinstaller --onefile --console --name FerroChatServer ferro_server.py
pause