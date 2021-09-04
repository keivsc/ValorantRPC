pip install pyinstaller

pip install -r requirements.txt

pyinstaller --onefile --hidden-import 'pystray' --icon=favicon.ico main.py