pip install pyinstaller

pip install -r requirements.txt

pyinstaller --onefile --hidden-import 'pystray._win32' --icon=favicon.ico main.py