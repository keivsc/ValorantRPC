pip install -r requirements.txt

pyinstaller main.py --name="ValorantRPC" --onefile --hidden-import 'pystray._win32' --icon=favicon.ico 